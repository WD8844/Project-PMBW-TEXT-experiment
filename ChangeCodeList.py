#由做好的整合码表重新按码替换原始CMAP码表
newchscodefile = 'a023-0_CHS_test.TBL'#所有的3个字库的码表相同
with open('a023-0_CHS_test.TBL',"r",encoding= 'utf-16')as cf:#锁定中文部分的码表字模序
    raws = cf.read().split("\n")
    flag = 0
    for raw in raws:
        trans = raw.split("=")
        if flag == 0 and len(trans[0])==4 and trans[0][0]=="0":
            first = int(trans[0],base=16)
            flag = -1
        elif len(trans[0])>1 and trans[0][0]!="0" and flag == -1:
            flag = 2
            last = int(trans[0])
            break
print(first)
print(last)
for num in range(3):
    filename = "a023_extr/a023-" + str(num)
    new = "_new"
    encoding = "utf16"
    MCodedict = dict()
    with open(newchscodefile,"r",encoding= encoding) as f:
        raw = f.read().split("\n")
        for i in range(len(raw)):
            #print(raw[i])
            if raw[i] != "":
                #print(raw[i])
                trans = raw[i].split("=")
                if len(trans[0]) > 1 and trans[0][0] == "0":#说明是改过的十六进制数编码序
                    id = str(int(trans[0],base = 16))#必须转为10进制，否则下面替换过程key无法对应
                else:
                    id = trans[0]
                if "==" in raw[i]:
                    MCodedict[id] = "="
                else:
                    MCodedict[id] = trans[1]
    #print(MCodedict)
    CMAPdictList = []
    for i in range(8):
        CMAPdict = dict()
        with open(filename +"序码表_"+str(i)+ ".txt","r",encoding=encoding)as f:
            raw = f.read().split("\n")
            for i in range(len(raw)):
                if raw[i] != "":
                    trans = raw[i].split("=")
                    if "==" in raw[i]:
                        CMAPdict[trans[0]] = "="
                    else:
                        CMAPdict[trans[0]] = trans[1]
        #print(len(CMAPdict))
        #print(CMAPdict)
        CMAPdictList.append(CMAPdict)
    for key in MCodedict:
        for i in range(len(CMAPdictList)):
            if key in CMAPdictList[i]:
                #print(key)
                #print(CMAPdictList[i][key],MCodedict[key])
                if CMAPdictList[i][key] != MCodedict[key]:
                    print("将字模序为{}的字符 {} 修改为：{}".format(key,CMAPdictList[i][key],MCodedict[key]))
                    CMAPdictList[i][key] = MCodedict[key]#对码替换
    #print(len(CMAPdictList))
    for i in range(len(CMAPdictList)):
        writelist = []
        for k in CMAPdictList[i]:
            trans = k + "=" + CMAPdictList[i][k] + "\n"
            writelist.append(trans)
        #print(writelist)
        with open(filename +"序码表_"+str(i)+ new +".txt","w",encoding=encoding)as w:
            w.writelines(writelist)
