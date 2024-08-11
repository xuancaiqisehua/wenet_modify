stage=0
stop_stage=0
inFile=$1
result=test

if [ ${stage} -le 0 ] && [ ${stop_stage} -ge 0 ]; then
 [ ! -d $result ] && mkdir -p $result
 echo "generate lexicon_en"
 python script/genDic.py $inFile $result/lexicon.uniq
 subword-nmt apply-bpe -c script/code_file_1000 < $result/lexicon.uniq > $result/lexicon.uniq.out
 paste $result/lexicon.uniq $result/lexicon.uniq.out >$result/lexicon_en
 sed -i "s:\t: :" $result/lexicon_en
 cp $result/lexicon_en dict/lexicon_en

fi

