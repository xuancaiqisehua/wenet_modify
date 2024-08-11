inDir=$1
awk '{print $1,$1}' $inDir/text >$inDir/spk2utt
cp $inDir/spk2utt $inDir/utt2spk
