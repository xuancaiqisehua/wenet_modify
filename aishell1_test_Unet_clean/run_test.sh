#testModel=50
#while true
#do
#if [ $lastModel -eq $testModel ];then
#  conda activate wenet
#  bash test.sh &
#  testModel=$[ testModel + 30 ]
#  sleep 480s;
#else
#  echo $lastModel $testModel
#fi
#  sleep 480s;
#done
testDir=exp
avgModelDir=$testDir/conformer/avg_model
testModel=220
if [ ! -d $avgModelDir ]; then
  mkdir -p $avgModelDir
fi
lastModel=`ls -tr $testDir/conformer/ | grep pt | grep -v avg_ | grep -v final | tail -1 | xargs -i basename {} .pt`
lastModel=230
while [ $testModel -le $lastModel ];
do
  
  num=`ls $testDir/conformer/avg_*.pt | wc -l`
  if [ $num -gt 0 ];then
   echo $num
   mv $testDir/conformer/avg_*.pt $avgModelDir
  fi 
  echo $testModel $lastModel
  #bash test.sh $testModel 
  bash test.sh $testModel $testDir 
  testModel=$[ testModel + 30 ]
done
