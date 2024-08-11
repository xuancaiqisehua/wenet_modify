feat_dir=data
ctc_weight=0.5
reverse_weight=0.0
test_dir=data
dict=data/dict/lang_char.txt

mode=ctc_greedy_search
root=exp
dir=$root/conformer
avg_model="exp/conformer_rnnt/epoch_1_step_10000.pt"
name=`basename $avg_model .pt`
data_type=raw
decoding_chunk_size=-1
. ./path.sh
python wenet/bin/recognize.py --gpu 3\
      --mode $mode \
      --config $dir/train.yaml \
      --data_type $data_type \
      --test_data data/test/wav.scp \
      --checkpoint $avg_model \
      --beam_size 10 \
      --batch_size 1 \
      --penalty 0.0 \
      --dict $dict \
      --ctc_weight $ctc_weight \
      --reverse_weight $reverse_weight \
      --result_dir $root/text_${name} \
      ${decoding_chunk_size:+--decoding_chunk_size $decoding_chunk_size}
    sed -i "s:SIL::g" $root/text_${name}
    python tools/compute-wer.py --char=1 --v=1 \
      data/test/text $root/text_${name} > $root/wer_${name}


