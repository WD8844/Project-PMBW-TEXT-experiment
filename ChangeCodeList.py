#Replace the original CMAP table with the newly integrated code table
# All three font library have the same code table. I have pathd my Chinese code table as 'NewCodeList.txt'
def ChangeCodeList(newCodeListpath,narcFilename,filenum = 3,encoding= 'utf-16'):
    with open(newCodeListpath,"r",encoding= encoding)as cf:# Make sure the first and the last code of Chinese characters in codelist
        raws = cf.read().split("\n")
        flag = 0
        for raw in raws:
            if "==" in raw:
                continue
            trans = raw.split("=")
            bo = (ord(trans[1]) >= 0x4E00) and (ord(trans[1]) <= 0x9FFF)#中文编码范围
            if flag == 0 and bo:
                first = int(trans[0])
                flag = -1
            elif not bo and flag == -1:
                last = int(trans[0])-1#上一个才是最后
                break
    #print(first)
    #print(last)
    nftrExtrpath = narcFilename+'_extr/'
    for num in range(int(filenum)):
        filepath = nftrExtrpath + narcFilename+"-"+ str(num)#the location  of font narc in the ROM of BW  is a/0/2/3;
        #I have repathd the font narc as "a023" and export it at ./a023_extr/
        new = "_new"
        MCodedict = dict()
        with open(newCodeListpath,"r",encoding= encoding) as f:
            raw = f.read().split("\n")
            for i in range(len(raw)):
                #print(raw[i])
                if raw[i] != "":
                    #print(raw[i])
                    trans = raw[i].split("=")
                    id = trans[0]
                    if "==" in raw[i]:
                        MCodedict[id] = "="
                    else:
                        MCodedict[id] = trans[1]
        #print(MCodedict)
        CMAPdictList = []
        for i in range(8):
            CMAPdict = dict()
            with open(filepath +"序码表_"+str(i)+ ".txt","r",encoding=encoding)as f:
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
                        CMAPdictList[i][key] = MCodedict[key]# One-to-one replacement
        #print(len(CMAPdictList))
        for i in range(len(CMAPdictList)):
            writelist = []
            for k in CMAPdictList[i]:
                trans = k + "=" + CMAPdictList[i][k] + "\n"
                writelist.append(trans)
            #print(writelist)
            with open(filepath +"序码表_"+str(i)+ new +".txt","w",encoding=encoding)as w:
                w.writelines(writelist)
if __name__ =="__main__":
    import sys,os
    if len(sys.argv) != 3:
        print("使用方法: .\ChangeCodeList.py <新码表> <Nftr对应的原Narc名>")
    else:
        NCpath = sys.argv[1]
        narcname = sys.argv[2]
        extrpath = narcname+"_extr/"
        try:
            if os.path.exists(extrpath):
                ChangeCodeList(NCpath,narcname)
            else:
                raise FileExistsError(f"{extrpath}不存在，请确认是否已利用ExtractNarc.py从目标Narc中正确提取了Nftr文件")
        except Exception as e:
            print(f"錯誤: {e}，请重新操作。")

