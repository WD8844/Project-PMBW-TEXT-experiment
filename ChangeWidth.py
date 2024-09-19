import csv
def ChangeWidth(newCodeListpath,narcFilename,encoding='utf-16'):
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
    nftrExtrpath = narcFilename+'_extr/'
    for num in range(3):
        filepath = nftrExtrpath + narcFilename +"-"+str(num)
        csvfile = filepath + 'CWDH.csv'
        ncsvfile = filepath + 'CWDH_new.csv'

        transl = []
        with open(csvfile,"r") as r:
            reader = csv.DictReader(r)
            locs = []
            widths = []
            tags = []
            for row in reader:
                locs.append(int(row['loc']))#csv表全都是默认为str字串型
                widths.append(int(row['width']))
                tags.append(int(row['tag']))
            for i in range(len(tags)):
                if tags[i] == 1:
                    #print(widths[i])
                    transl.append(widths[i])
            transl = list(set(transl))
            transl.sort()
            print(f"CWDH：{transl}")
            nwidth = []
            for i in range(len(locs)):
                if (locs[i] >= first and locs[i] <= last) or  locs[i] == 4932 or locs[i] == 336 or locs[i]== 207\
                       or locs[i] == 208 or locs[i] == 4904 or locs[i] == 4913 :#？！“”，。全角字母
                    nwidth.append(transl[1])#选择适中的宽度
                elif(locs[i] >= 4934 and locs[i] <= 4959) or (locs[i] >= 4966 and locs[i] <= 4991):
                    nwidth.append(transl[0])#最小可选宽度
                else:
                    nwidth.append(widths[i])
        with open(ncsvfile,"w",newline="") as w:
            writer = csv.writer(w)
            writer.writerow(["loc","width","tag"])
            for i in range(len(locs)):
                writer.writerow([locs[i],nwidth[i],tags[i]])

        csvfile = filepath + "宽度表.csv"
        ncsvfile = filepath + "宽度表_new.csv"
        with open(csvfile,"r",newline="")as r:
            reader = csv.DictReader(r)
            locs = []
            lefts = []
            widths = []
            advances = []
            for row in reader:
                locs.append(int(row['loc']))#csv表全都是默认为str字串型
                lefts.append(int(row['left']))
                widths.append(int(row['width']))
                advances.append(int(row['advance']))
            nwidth = []
            nleft = []
            nadvance = []
            for i in range(len(locs)):
                if (locs[i] >= first and locs[i] <= last):#中文
                    if num < 2:
                        nwidth.append(max(widths))
                        nadvance.append(max(advances)-1)
                        nleft.append(0)
                    else:
                        nwidth.append(max(widths))
                        nadvance.append(max(advances))
                        nleft.append(0)
                elif locs[i] == 4932 or locs[i] == 336 or locs[i]== 207\
                       or locs[i] == 208 or locs[i] == 4904 or locs[i] == 4913\
                        or locs[i] == 4927 or locs[i] == 4928:#？！“”，。;:
                    nwidth.append(max(widths)-3)
                    nadvance.append(max(advances)-2)
                    nleft.append(2)
                elif (locs[i] >= 4934 and locs[i] <= 4959) or (locs[i] >= 4966 and locs[i] <= 4991):#全角字母
                    nwidth.append(widths[i])
                    if advances[i] < max(advances):
                        nadvance.append(advances[i]+1)
                    else:
                        nadvance.append(advances[i])
                    nleft.append(lefts[i])
                else:
                    nwidth.append(widths[i])
                    nadvance.append(advances[i])
                    if lefts[i]-1 > 0:
                        nleft.append(lefts[i]-1)
                    else:
                        nleft.append(lefts[i])

        with open(ncsvfile,"w",newline="") as w:
            writer = csv.writer(w)
            writer.writerow(["loc","left","width","advance"])
            for i in range(len(locs)):
                writer.writerow([locs[i],nleft[i],nwidth[i],nadvance[i]])
if __name__ =="__main__":
    import sys,os
    if len(sys.argv) != 3:
        print("使用方法: python .\ChangeWidth.py <新码表> <Nftr对应的原Narc名>")
    else:
        NCpath = sys.argv[1]
        narcname = sys.argv[2]
        extrpath = narcname+"_extr/"
        try:
            if os.path.exists(extrpath):
                ChangeWidth(NCpath,narcname)
            else:
                raise FileExistsError(f"{extrpath}不存在，请确认是否已利用ExtractNarc.py从目标Narc中正确提取了Nftr文件")
        except Exception as e:
            print(f"錯誤: {e}，请重新操作。")
            input("按任意键结束...")
