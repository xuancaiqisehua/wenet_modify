import sys
import re
def main():
    
    textPath = sys.argv[1]
    dictPath = sys.argv[2]
    textOripath =  sys.argv[3]    

    dataDict = {}
    with open(dictPath, "r") as f:
        for line in f:
            line = line.split()
            dataDict[line[1]] = line[0]
  
    txtDic={}
    with open(textOripath, "r") as f:
        for line in f:
            line = re.split("\s+",line,1)
            txtDic[line[0]] = line[1]
    print(len(dataDict))
    with open(textPath, "r"
         ) as fs, open(textPath + ".target", "w"
         ) as ft, open(textPath + ".blank", "w") as fb:
        blankText = []
        for line in fs:
            line = line.split()
            if len(line) < 2:
                 print(line[0], file=fb)
                 blankText.append(line[0])
                 continue
            text = []
            if line[0] in txtDic:
              for i in line[1:]:
                  if i in dataDict:
                      text.append(dataDict[i])
                  else:
                      text.append("1")
              target =" ".join(text)
              print(line[0], target, line[1:],txtDic[line[0]],file=ft)
            else:
               print(line[0])
    print("blank text：", blankText)



if __name__ == "__main__":
    main()
