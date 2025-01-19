dict=data/dict/lang_char.txt
stage=7
stop_stage=7
dict=data/dict/lang_char.txt
data=aishell
if [ ${stage} -le 7 ] && [ ${stop_stage} -ge 7 ]; then
  # 7.1 Prepare dict
  unit_file=$dict
  mkdir -p data/local/dict
  cp $unit_file data/local/dict/units.txt
  tools/fst/prepare_dict.py $unit_file ${data}/resource_aishell/lexicon.txt \
    data/local/dict/lexicon.txt
  # 7.2 Train lm
  #lm=data/local/lm
  #mkdir -p $lm
  #tools/filter_scp.pl $data/data_aishell/transcript/aishell_transcript_v0.8.txt > $lm/text
  #local/aishell_train_lms.sh
  ## 7.3 Build decoding TLG
  #tools/fst/compile_lexicon_token_fst.sh \
  #  data/local/dict data/local/tmp data/local/lang
  #tools/fst/make_tlg.sh data/local/lm data/local/lang data/lang_test || exit 1;
  
  ## 7.4 Decoding with runtime
  #chunk_size=-1
  #./tools/decode.sh --nj 16 \
  #  --beam 15.0 --lattice_beam 7.5 --max_active 7000 \
  #  --blank_skip_thresh 0.98 --ctc_weight 0.5 --rescoring_weight 1.0 \
  #  --chunk_size $chunk_size \
  #  --fst_path data/lang_test/TLG.fst \
  #  --dict_path data/lang_test/words.txt \
  #  data/test/wav.scp data/test/text $dir/final.zip \
  #  data/lang_test/units.txt $dir/lm_with_runtime
  ## Please see $dir/lm_with_runtime for wer


fi
