import sys,os,re
def genLangChar(filename):
  eledic={}
  fw=open(os.path.join('dict','lang_char_new'),'w',encoding='utf-8')
  with open(filename,'r',encoding='utf-8') as fr:
    for line in fr:
      try:
        key=line.strip()
        if key not in eledic:
          eledic[key]='0'
      except Exception as e:
        print(line,e)
  eledicSort=sorted(eledic.items(),key=lambda x : x[1],reverse=True)
  fw.write("SP 0\nUNK 1\nSIL 2\n")
  #print("SP 0\nUNK 1\nSIL 2")
  i=3
  for key,value in eledicSort:
    #print(key,i)
    fw.write(key+' '+str(i)+'\n')
    i+=1
  #print("<sos/eos> {}".format(i))
  fw.write("<sos/eos> {}".format(i)+'\n')
  fw.close()
filename=sys.argv[1]
genLangChar(filename)
