import os
#统计出现的目标字符
def SetCharCounts(dirpath, chrange = "CHS"):
    subline = '\n------------------------------\n'
    fileslist = os.listdir(dirpath)
    chl = []
    if dirpath[-1] != "/":
        dirpath += "/"
    for filepath in fileslist:
        if ".txt" in filepath:#只统计*.txt
            with open(dirpath+filepath,"r",encoding="utf-16") as r:
                t = r.read()
                texts = t.split(subline)
                for i in range(len(texts)):
                    #print(texts[i])
                    if "_" in texts[i]:
                        continue
                    else:
                        cl = list(set(texts[i]))#利用set分字且去掉重复的字
                        #print(cl)
                        chl.extend(cl)
    chl = list(set(chl))#合并去掉与之前的文本中相重复的字
    #print(chl)
    #转换为字符码并排序
    chol = []
    charl = []
    for j in range(len(chl)):
        chol.append(ord(chl[j]))
    chol.sort()#默认按字符码升序排列
    if chrange == "CHS":#统计出现的所有常用中文字
        for o in chol:
            if (o >= 0x4E00) and (o <= 0x9FFF):#只要中文部分
                charl.append(chr(o))
    else:
        pass#待开发
    return charl#返回统计好的按字符码升序排列的目标字符列表
if __name__ == "__main__":#Just for the code test.
    print(SetCharCounts("./Counts"))
