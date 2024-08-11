stage=2
stop_stage=2

njob=1
nJOB=4
num_utts_per_shard=1000
#train_set=8k_data
outdir=dataset #16k_cn_en/dataset/
data_type=shard
num_threads=10
dataset=lst
shardsDir=dataset/shards
alignmentTxT=alignment/OriTxT
alignmentLabel=alignment/Label_2434



. ./tools/parse_options.sh
. ./path.sh

#updataToken
if [ ${stage} -le 1 ] && [ ${stop_stage} -ge 1 ]; then
  [ ! -d $alignmentTxT ] && mkdir -p $alignmentTxT
  [ ! -d $alignmentLabel ] && mkdir -p $alignmentLabel
  echo "Prepare data, prepare required format"
  while read line
    do
    echo $line
    {
    cp $outdir/$line/text.Ori $alignmentTxT/$line
    awk 'ARGIND==1{a[$1]} ARGIND==2{if(!($1 in a)){print $0}}' $outdir/$line/Label_2434_EN $outdir/$line/Label_2434 >$outdir/$line/Label_2434_CH
    cat $outdir/$line/Label_2434_CH $outdir/$line/Label_2434_EN >$outdir/$line/Label_2434_New
    cp $outdir/$line/Label_2434_New $alignmentLabel/$line
    cd alignment
    bash run_align.sh OriTxT/$line Label_2434/$line
    cd -
    cp alignment/result/updateFile/$line $outdir/$line/text
    } &
    if [ $njob -lt $nJOB ];then
     njob=$[ njob + 1 ]
    else
     njob=0
     wait
    fi
    done<$dataset
fi


#make_shard_list
if [ ${stage} -le 2 ] && [ ${stop_stage} -ge 2 ]; then
  [ ! -d $alignmentTxT ] && mkdir -p $alignmentTxT
  [ ! -d $alignmentLabel ] && mkdir -p $alignmentLabel
  echo "Prepare data, prepare required format"
  while read line
    do
    echo $line
    {
    bash genutt2spk.sh $outdir/$line
    ./utils/fix_data_dir.sh $outdir/$line
    [ ! -d $shardsDir/$line ] && mkdir -p $shardsDir/$line
    if [ $data_type == "shard" ]; then
      tools/make_shard_list.py --num_utts_per_shard $num_utts_per_shard --prefix $line \
        --num_threads $num_threads $outdir/$line/wav.scp $outdir/$line/text \
        $shardsDir/$line $shardsDir/${line}_data.list
    else
      tools/make_raw_list.py data/$train_set/$line/wav.scp data/$train_set/$line/text \
        data/$x/data.list
    fi
    } &
    if [ $njob -lt $nJOB ];then
     njob=$[ njob + 1 ]
    else
     njob=0
     wait
    fi
    done<$dataset
fi
