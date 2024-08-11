tools/compute_cmvn_stats.py --num_workers 16 --train_config $train_config \
   --in_scp data/${train_set}/wav.scp \
   --out_cmvn data/$train_set/global_cmvn
