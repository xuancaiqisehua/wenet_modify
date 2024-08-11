import os,sys,time,re
def readfile(filename):
    try:
         with open(filename,'r',encoding='gbk') as r:
           lines=r.readlines()
    except:
       with open(filename,'r',encoding='utf-8') as r:
          lines=r.readlines()
    return lines
# oldword,newword
def get_worddic(filename):
   lines=readfile(filename)
   worddic={}
   for line in lines:
     #print(line)
     try:
       splitline=re.split('\s+',line,1)
       oldword=splitline[0].strip()
       newword=splitline[1].strip()
       if oldword not in worddic:
           worddic[oldword]=newword
     except:
       print(line)
   return worddic
def worddic(filename):
   lines=readfile(filename)
   worddic={}
   for line in lines:
     line=line.strip()
     if line not in worddic:
         worddic[line]='0'
   return worddic
#worddic=get_worddic(dicfile)
def get_newline(line):
   for olddic in worddic:
     line=line.replace(olddic,worddic[olddic])
# single file
def get_replaceline(dicfile,in_file,outfile):
    starttime=time.time()
    worddic=get_worddic(dicfile)
    dirs,name=os.path.split(in_file)
    with open(in_file,'r',encoding='utf-8') as f:
       with open(outfile,'w') as w:
          for line in f:
             key,content=re.split('\s+',line,1)
             for olddic in worddic:
               content=re.sub('([\u4E00-\u9FA5]+)\s+([\u4E00-\u9FA5]+)','\\1\\2',content)
               content=content.replace(olddic,worddic[olddic])
             w.write('{} {}'.format(key,content))
    endtime=time.time()
    print('totle time : {}'.format(endtime-starttime))
# if word in line then get line
def get_multiline(dicfile,in_file):
    worddic=(dicfile)
    lines=readfile(in_file)
    dirs,name=os.path.split(in_file)
    newfile=os.path.join(dirs,'tmp_'+name)
    print(newfile)
    with open(newfile,'w') as w:
      for i in range(0,len(lines),6):
         flag=0
         for word in worddic:
            if flag==0:
               if word in lines[i]:
                  flag=1
         if flag==1:
           w.write(lines[i]+lines[i+1]+lines[i+4]+lines[i+5])
if len(sys.argv)<3:
   print('useage python in_file dicfile out_file')
else:
   in_file=sys.argv[1]
   dicfile=sys.argv[2]
   outfile=sys.argv[3]
   get_replaceline(dicfile,in_file,outfile)
   #replace_multifile(dicfile,in_file)
   #get_multiline(dicfile,in_file)
