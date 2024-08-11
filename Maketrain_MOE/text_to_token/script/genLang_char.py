import sys
import random
def readFile(inFile,outFile):
  dic={}
  with open(inFile,'r',encoding='utf-8') as r:
   lines = r.readlines()
  random.shuffle(lines) 
  random.shuffle(lines) 
  index=2
  with open(outFile,'w',encoding='utf-8') as w:
     w.write('<blank> 0\n<unk> 1\n')
     for line in lines:
        spline = line.strip().split(" ")
        word = spline[0]
        if word not in dic:
          dic[word]=index
          w.write(word+' '+str(index)+'\n')
          index+=1
     w.write("<sos/eos> {}".format(index)+'\n')
inFile,outFile=sys.argv[1],sys.argv[2]
readFile(inFile,outFile)
