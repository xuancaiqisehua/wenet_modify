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
import datetime
import logging
import os
import torch
import yaml

import torch.distributed as dist

from torch.distributed.elastic.multiprocessing.errors import record

from wenet.utils.executor import Executor
from wenet.utils.config import override_config
from wenet.utils.init_model import init_model
from wenet.utils.init_tokenizer import init_tokenizer
from wenet.utils.train_utils import (
    add_model_args, add_dataset_args, add_ddp_args, add_deepspeed_args,
    add_trace_args, init_distributed, init_dataset_and_dataloader,
    check_modify_and_save_config, init_optimizer_and_scheduler,
    trace_and_print_model, wrap_cuda_model, init_summarywriter, save_model,
    log_per_epoch)

from wenet.utils.file_utils import read_symbol_table, read_non_lang_symbols

def get_args():
    parser = argparse.ArgumentParser(description='training your network')
    parser.add_argument('--train_engine',
                        default='torch_ddp',
                        choices=['torch_ddp', 'deepspeed'],
                        help='Engine for paralleled training')
    parser = add_model_args(parser)
    parser = add_dataset_args(parser)
    parser = add_ddp_args(parser)
    parser = add_deepspeed_args(parser)
    parser = add_trace_args(parser)
    args = parser.parse_args()
    if args.train_engine == "deepspeed":
        args.deepspeed = True
        assert args.deepspeed_config is not None
    return args


# NOTE(xcsong): On worker errors, this recod tool will summarize the
#   details of the error (e.g. time, rank, host, pid, traceback, etc).
@record
def main():
    args = get_args()
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    # Set random seed
    torch.manual_seed(777)

    # Read config
    with open(args.config, 'r') as fin:
        configs = yaml.load(fin, Loader=yaml.FullLoader)
    if len(args.override_config) > 0:
        configs = override_config(configs, args.override_config)

    token_paths = configs['tokenizer_conf']['symbol_table_path'].split(',')


    symbol_table={}
    
    for token_path in token_paths:
       tokens = read_symbol_table(token_path)
       path = token_path.split('/')[-1]
       for key in tokens:
          if key == '<sos/eos>':
             continue
          if key not in symbol_table:
            symbol_table[key] = len(symbol_table)
    if len(symbol_table)<20000:
       for i in range(len(symbol_table),20000):
         symbol_table[len(symbol_table)]=len(symbol_table)
     
 
    symbol_table['<sos/eos>'] = len(symbol_table)


    configs['tokenizer_conf']['symbol_table_path']=symbol_table
   
    configs['tokenizer_conf']['special_tokens']['<sos>'] = len(symbol_table) 
    configs['tokenizer_conf']['special_tokens']['<eos>'] = len(symbol_table) 
    
    configs['dataset_conf']['symbol_table'] = symbol_table 
 
    # init tokenizer
    tokenizer = init_tokenizer(configs)

    with open('data/dict/lang_char_train.txt','w',encoding='utf-8') as w:
       for key,value in symbol_table.items():
          w.write(f'{key} {str(value)}\n')

    # Init env for ddp OR deepspeed
    #_, _, rank = init_distributed(args)

    # Get dataset & dataloader
    train_dataset, cv_dataset, train_data_loader, cv_data_loader = \
        init_dataset_and_dataloader(args, configs, tokenizer)

    for data in train_dataset:
      print(data)


if __name__=='__main__':
   main()
