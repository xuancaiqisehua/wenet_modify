# Copyright (c) 2021 Mobvoi Inc. (authors: Binbin Zhang)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import argparse
import copy
import logging
import os

import torch
import torch.distributed as dist
import torch.optim as optim
import yaml
from tensorboardX import SummaryWriter
from torch.utils.data import DataLoader

from wenet.utils.init_model import init_model
from wenet.utils.file_utils import read_symbol_table, read_non_lang_symbols
from wenet.utils.checkpoint import (load_checkpoint,save_checkpoint,
                                    load_trained_modules)



def get_args():
    parser = argparse.ArgumentParser(description='training your network')
    parser.add_argument('--config', required=True, help='config file')
    parser.add_argument('--checkpoint', required=True, help='checkpoint')
    parser.add_argument('--cmvn', default=None, help='global cmvn file')
    parser.add_argument('--model_layer', type=int,default=12, help='model layer')
    parser.add_argument('--out_layer',type=int, default=8, help='out layer')
    parser.add_argument('--save_model',type=str, default="save_model.py", help='save model')
    parser.add_argument('--symbol_table',
                        required=True,
                        help='model unit symbol table for training')


    args = parser.parse_args()
    return args


def main():
    args = get_args()
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    # Set random seed
    with open(args.config, 'r') as fin:
        configs = yaml.load(fin, Loader=yaml.FullLoader)


    if 'fbank_conf' in configs['dataset_conf']:
        input_dim = configs['dataset_conf']['fbank_conf']['num_mel_bins']
    else:
        input_dim = configs['dataset_conf']['mfcc_conf']['num_mel_bins']
    symbol_table = read_symbol_table(args.symbol_table)
    vocab_size = len(symbol_table)

    # Save configs to model_dir/train.yaml for inference and export
    configs['input_dim'] = input_dim
    configs['output_dim'] = vocab_size
    configs['cmvn_file'] = args.cmvn
    configs['is_json_cmvn'] = True
    cur_layer = configs['encoder_conf']['num_blocks']
    if args.model_layer != cur_layer:
       print(f"加载模型层数 {args.model_layer} 与配置文件中模型层数 {cur_layer} 不一致")
       exit()

    train_conf = configs['dataset_conf']

    model_cur = init_model(configs)
    cur_config = configs
    cur_config ['encoder_conf']['num_blocks'] = args.out_layer
    model_out = init_model(cur_config)
   

    if torch.cuda.is_available():
        logging.info('Checkpoint: loading from checkpoint %s for GPU' % args.checkpoint)
        checkpoint = torch.load(args.checkpoint)
    else:
        logging.info('Checkpoint: loading from checkpoint %s for CPU' % args.checkpoint)
        checkpoint = torch.load(args.checkpoint, map_location='cpu')
    del_layer = []
    del_layer_dic = {}
    new_layer = args.out_layer
    cut_layer = cur_layer - new_layer
    for i in range(cut_layer):
       del_layer.append(f"encoder.encoders.{i}")
    del checkpoint["encoder.encoders.0.self_attn.pos_bias_u"]
    save_state = {}
    for del_name in del_layer:
       for name in list(checkpoint):
          del_name_model = ".".join(name.split('.')[:3])
          if del_name == del_name_model :
              del checkpoint[name]
    for name in checkpoint:
       if "encoder.encoders" in name:
          split_name = name.split('.')
          new_name = ".".join(split_name[:2]+[str(int(split_name[2])-cut_layer)]+split_name[3:])
          del_layer_dic[name] = new_name
       
    for name,new_name in del_layer_dic.items():
         checkpoint[new_name] = checkpoint.pop(name)
    model_out.load_state_dict(checkpoint, strict=False) 
    torch.save(model_out.state_dict(),args.save_model)
if __name__ == '__main__':
    main()
