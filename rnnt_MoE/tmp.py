import sentencepiece as spm
sp = spm.SentencePieceProcessor()
sp.Load('./unigram_500.model')
new_lines = []
#with open('recover.txt','r',encoding='utf-8') as file:
#    for line in file:
#        line = line.strip()
#        print(line)
#        #对字符串去掉换行
#        line = line.replace('\n','')
#        print(line)
#        new_lines.append(smart_byte_decode(sp.decode(line))+'\n')
#print(type(new_lines))
#with open('recover_ori1.txt','w',encoding='utf-8') as file1:
#    file1.writelines(new_lines) 
#with open('recover_ori1.txt','w',encoding='utf-8') as file1:
#    file1.writelines(new_lines)     
