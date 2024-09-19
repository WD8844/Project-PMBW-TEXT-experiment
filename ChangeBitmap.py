def ChangeBitmap(newCodeListpath,narcFilename,Fnum=3,encoding= 'utf-16'):
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
    print(f"修改字模序号范围为：{first}~{last}")
    for num in range(Fnum):
        filenum = str(num)
        file = narcFilename+"-" + filenum
        chsfile = file + "-chs"
        filepath = narcFilename+"_extr/" + file
        sizedict = {"0":45,"1":25,"2":36}
        size = sizedict[filenum]

        def buffersplit(buffer,size):
            sp = []
            for i in range(0,len(buffer),size):
                sp.append(buffer[i:i+size])
            #print(len(sp))
            return sp

        with open(chsfile,"rb")as f:
            chsbuffer = f.read()
            schsbuffer = buffersplit(chsbuffer,size)
        #print(len(schsbuffer[0]))
        #print(schsbuffer)
        with open(filepath + ".bitmap","rb")as f:
            buffer = f.read()
            sbuffer = buffersplit(buffer,size)

        #print(len(buffer))
        #print(len(sbuffer))

        with open(filepath + "_new.bitmap","wb")as w:
            for i in range(len(schsbuffer)):
                sbuffer[first + i] = schsbuffer[i]
            w.writelines(sbuffer)
if __name__ =="__main__":
    import sys,os
    if len(sys.argv) != 3:
        print("使用方法: python .\ChangeBitmap.py <新码表> <Nftr对应的原Narc名>")
    else:
        NCpath = sys.argv[1]
        narcname = sys.argv[2]
        extrpath = narcname+"_extr/"
        try:
            if os.path.exists(extrpath):
                ChangeBitmap(NCpath,narcname)
            else:
                raise FileExistsError(f"{extrpath}不存在，请确认是否已利用ExtractNarc.py从目标Narc中正确提取了Nftr文件")
        except Exception as e:
            print(f"錯誤: {e}，请重新操作。")
            input("按任意键结束...")
