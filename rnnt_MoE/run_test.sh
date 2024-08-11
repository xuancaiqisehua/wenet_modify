#!/bin/bash

# Copyright 2019 Mobvoi Inc. All Rights Reserved.
#           2022 Binbin Zhang(binbizha@qq.com)

. ./path.sh || exit 1;


export CUDA_VISIBLE_DEVICES="0,1,2,3"
stage=4 # start from 0 if you need to start from data preparation
stop_stage=4

# You should change the following two parameters for multiple machine training,
# see https://pytorch.org/docs/stable/elastic/run.html
HOST_NODE_ADDR="localhost:0"
num_nodes=1

# The aishell dataset location, please change this to your own path
# make sure of using absolute path. DO-NOT-USE relatvie path!
data="/data/asr_data/aishell/"
data_url=www.openslr.org/resources/33

nj=16
dict=data/dict/lang_char.txt

data_type=raw
num_utts_per_shard=1000

train_set=train
train_config="conf/conformer_u2pp_rnnt.yaml"
dir="exp/conformer_rnnt"

# use average_checkpoint will get better result
average_checkpoint=true
decode_checkpoint="exp/conformer_rnnt/epoch_6.pt"
average_num=30
#decode_modes="ctc_greedy_search"
decode_modes="attention_rescoring"

train_engine=torch_ddp

deepspeed_config=../../aishell/s0/conf/ds_stage2.json
deepspeed_save_states="model_only"

. tools/parse_options.sh || exit 1;


stage=5
stop_stage=5


if [ ${stage} -le 5 ] && [ ${stop_stage} -ge 5 ]; then
  # Test model, please specify the model you want to test by --checkpoint
  if [ ${average_checkpoint} == true ]; then
    decode_checkpoint=$dir/avg_${average_num}.pt
    echo "do model average and final checkpoint is $decode_checkpoint"
    python wenet/bin/average_model.py \
      --dst_model $decode_checkpoint \
      --src_path $dir  \
      --num ${average_num} 
  fi
  # Please specify decoding_chunk_size for unified streaming and
  # non-streaming model. The default value is -1, which is full chunk
  # for non-streaming inference.
  decoding_chunk_size=16
  # only used in rescore mode for weighting different scores
  rescore_ctc_weight=0.5
  rescore_transducer_weight=0.5
  rescore_attn_weight=0.5
  # only used in beam search, either pure beam search mode OR beam search inside rescoring
  search_ctc_weight=0.3
  search_transducer_weight=0.7

  reverse_weight=0.0

  while read line
  do
  {
  wavpath=${line}.lst
  textpath=${line}.txt
  name=`basename $line`
  python wenet/bin/recognize.py  --gpu 3\
    --modes $decode_modes \
    --config $dir/train.yaml \
    --data_type $data_type \
    --test_data $wavpath \
    --checkpoint $decode_checkpoint \
    --beam_size 10 \
    --batch_size 10 \
    --penalty 0.0 \
    --ctc_weight $rescore_ctc_weight \
    --transducer_weight $rescore_transducer_weight \
    --attn_weight $rescore_attn_weight \
    --search_ctc_weight $search_ctc_weight \
    --search_transducer_weight $search_transducer_weight \
    --reverse_weight $reverse_weight \
    --result_dir $dir \
    ${decoding_chunk_size:+--decoding_chunk_size $decoding_chunk_size}
  for mode in ${decode_modes}; do
    python tools/compute-wer.py --char=1 --v=1 \
      $textpath $dir/$mode/${name}.txt > $dir/$mode/${name}.wer
  done
  }
 done<$1
fi
