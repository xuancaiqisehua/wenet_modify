import sys
import re
import os

#step 1  : 如果没有开源词典 
def genUniqWord(filename,lexicon):
  dic={}
  with open(lexicon,'w',encoding='utf-8') as fw:
    with open(filename,'r',encoding='utf-8') as fr:
      for line in fr:
         try:
           key,content=re.split("\s+",line,1)
           sentence=re.sub('( )-([a-z]+)','\\1\\2',content.lower())
           sentence = re.sub('([a-z]+)\' ','\\1 ',sentence)
           sentence=re.findall('[a-z]+[\'\-][a-z]+|[a-z]+',sentence)
           for word in sentence:
             if word not in dic:
               dic[word]="0"
               fw.write(word+'\n')
               #print(word)
         except Exception as e:
           print("erro ",e)
inFile=sys.argv[1]
lexicon=sys.argv[2]
genUniqWord(inFile,lexicon)
