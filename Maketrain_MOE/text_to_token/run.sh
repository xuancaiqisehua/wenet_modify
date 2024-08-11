outdir=$2
if [ ! -d $outdir ]; then
   mkdir -p $outdir
fi
while read line
do
  name=`basename $line`
  echo $name
  bash genLexicon.sh $line
  python script/text2token.py $line $outdir/$name
  python script/token2text.py $outdir/$name dict/lang_char.txt $line
done<$1
