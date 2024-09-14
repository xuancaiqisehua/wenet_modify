#your dir
ansdir="test"
wenetTrain="/data/gepenghua/train_env/asr_train_8k/"
avgMoldeDir=${wenetTrain}/avg_model
avgModelNum=10
exp="exp/conformer"


#outfile
root=model_result
resultdir=$root/result_decoder
werdir=$root/wer_decoder
modellog=$root/model.log

stage=1
stop_stage=1

if [ $# != 2 ] ;then
 echo "USAGE: bash $0 <modellst> <datasetLst>"
 exit 1;
fi
modellst=$1
datasetLst=$2
tmpfile=tmppack
. export.sh
[ ! -d $resultdir ] && mkdir -p $resultdir
[ ! -d $werdir ] && mkdir -p $werdir

function autoTest(){
  # date param
  date=`date | awk '{print $2""$3}'`
  outfile=$root/model.result.full_${date}
  outfileChunk16=$root/model.result.Chunk16_${date}
  if [ ${stage} -le -1 ] && [ ${stop_stage} -ge -1 ]; then
    cd ${wenetTrain}
    source ~/.bashrc
    conda activate wenet10
    . ./path.sh
    #python wenet/bin/average_model.py --dst_model avg_5.pt --src_path exp/conformer/ --num 5 >${tmpfile}
    python wenet/bin/average_model.py --dst_model avg_5.pt --src_path $exp --num $avgModelNum >${tmpfile}
    s=`grep "Processing" ${tmpfile} | head -1 | xargs -i basename {} .pt`
    e=`grep "Processing" ${tmpfile} | tail -1 | xargs -i basename {} .pt`
    python wenet/bin/export_jit.py --config $exp/train.yaml --checkpoint avg_5.pt --output_file test_${s}-${e}.zip --output_quant_file test_${s}-${e}.zip
    [ ! -d $avgMoldeDir ] && mkdir -p $avgMoldeDir
    mv avg_5.pt ${avgMoldeDir}/avg_${s}-${e}.pt
    mv test_${s}-${e}.zip ${avgMoldeDir}
    realpath ${avgMoldeDir}/test_${s}-${e}.zip >$modellst
    cd -
    mv ${wenetTrain}/$modellst ./
  fi
  # full chunk
  if [ ${stage} -le 2 ] && [ ${stop_stage} -ge 2 ]; then
    sed  -i "s:CHUNK_SIZE=16:CHUNK_SIZE=-1:" conf/ams.conf
    sed  -i "s:CHUNK_SIZE=16:CHUNK_SIZE=-1:" conf/asr_cmd.conf
    echo "start full chunk" >$modellog
    grep CHUNK_SIZE conf/ams.conf >>$modellog
    while read line;
    do
       echo $line >>$modellog
       cd conf/model
       ln -sf $line test.zip
       cd -
       while read line
        do
         name=`basename $line`
         echo $name
         ./dynamic_wfst_offline1213 conf/asr_cmd.conf ${line}.lst $resultdir/${name}.result
         ./wer ${ansdir}/${name}.txt $resultdir/${name}.result $werdir/${name}.wer
        done<$datasetLst
       tail $werdir/*.wer >>$modellog
    done<$modellst
    egrep "zip|CHAR" $modellog >tmp.log
    python get_testresult.py tmp.log $outfile
    #[  -d ${root}_full/$root ] && rm -r ${root}_full/$root
    #mv $root ${root}_full
  fi
  # chunk_size 16
  if [ ${stage} -le 1 ] && [ ${stop_stage} -ge 1 ];then
    sed  -i "s:CHUNK_SIZE=-1:CHUNK_SIZE=16:" conf/ams.conf
    sed  -i "s:CHUNK_SIZE=-1:CHUNK_SIZE=16:" conf/asr_cmd.conf
    echo "start chunk 16" >$modellog
    grep CHUNK_SIZE conf/ams.conf >>$modellog
    while read line;
    do
       echo $line >>$modellog
       cd conf/model
       ln -sf $line test.zip
       cd -
       model_name=$(basename "$line")
       while read line
        do
         name=`basename $line`
         echo $name
         #./dynamic_wfst_offline1213 conf/asr_cmd.conf ${line}.lst $resultdir/${name}.result
         ./dynamic_wfst_offline_20240710 conf/asr_cmd.conf ${line}.lst $resultdir/${name}.result
         ./wer ${ansdir}/${name}.txt $resultdir/${name}.result $werdir/${name}.wer
        done<$datasetLst
       tail $werdir/*.wer >>$modellog
    done<$modellst
    egrep "zip|CHAR" $modellog >tmp.log
    grep CHUNK_SIZE conf/ams.conf >>tmp.log
    python get_testresult.py tmp.log $outfileChunk16
    #[  -d ${root}_chunk/$root ] && rm -r ${root}_chunk/$root
    #mv $root ${root}_chunk
  fi
}
autoTest
exit

while true 
 do

 ## on time
 #sta_time=`date | awk '{print $5}'`
 #stime=8
 #if [ $stime -lt 10 ]
 #then
 #ytime=0${stime}
 #else
 #ytime=${stime}
 #fi
 #if [ $sta_time = ${ytime}":30:00" ];then
 # echo start autoTest
 # autoTest 
 #fi

 ## spleep

 autoTest
 sleep 54000

 done
echo finish
