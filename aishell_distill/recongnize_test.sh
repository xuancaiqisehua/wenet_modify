feat_dir=data
ctc_weight=0.5
reverse_weight=0.0
test_dir=data
dict=data/dict/lang_char.txt

mode=ctc_greedy_search
root="exp"
#dir=teacher_model
dir="exp/conformer"
avg_model="avg_551-559.pt"
textDir="data/test"
name=`basename $avg_model .pt`
data_type=raw
decoding_chunk_size=16

. tools/parse_options.sh || exit 1;
. ./path.sh
python wenet/bin/recognize.py --gpu 0 \
      --mode $mode \
      --config $dir/train.yaml \
      --data_type $data_type \
      --test_data ${textDir}/wav.scp \
      --checkpoint $avg_model \
      --beam_size 5 \
      --batch_size 10 \
      --penalty 0.0 \
      --dict $dict \
      --ctc_weight $ctc_weight \
      --reverse_weight $reverse_weight \
      --result_file $root/text_${name} \
      --connect_symbol " " \
      ${decoding_chunk_size:+--decoding_chunk_size $decoding_chunk_size}
    sed -i "s:SIL::g" $root/text_${name}
    python tools/compute-wer.py --char=1 --v=1 \
      ${textDir}/text $root/text_${name} > $root/wer_${name}
