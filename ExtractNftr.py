import csv
from nftr import *

def ExtractNftr(filepath):
    with open(filepath,'rb')as f:
        f.seek(0)
        rawdata = f.read()
        print("len(rawdata)",len(rawdata))
        nftr = NFTR(rawdata)
        with open(filepath + "宽度表.csv","w",newline="")as w:
            writer = csv.writer(w)
            writer.writerow(["loc","left","width","advance"])
            for i in range(len(nftr.fontsdata)):
                l = [i]
                l.extend(nftr.fontsdata[i])
                writer.writerow(l)
        with open(filepath + "CWDH.csv","w",newline="")as w:
            writer = csv.writer(w)
            writer.writerow(["loc","width","tag"])
            widthtable = nftr.cwdh.WidthTable
            for i in range(len(widthtable)):
                trans = [i]
                trans.extend(widthtable[i])
                writer.writerow(trans)
        with open(filepath + ".bitmap","wb")as w:
            for bitmap in nftr.bitmaps:
                w.write(bitmap)
        i = 0
        for cmap in nftr.CMAPTable:
            idxs = list(cmap.CodeTableDict.keys())
            codes = list(cmap.CodeTableDict.values())
            with open(filepath +"序码表_"+str(i)+ ".txt","w",encoding="utf16")as w:
                for j in range(len(idxs)):
                    s = str(idxs[j]) + "=" + chr(codes[j])+"\n"
                    w.write(s)
            i += 1



if __name__ =="__main__":
    import sys
    if len(sys.argv) != 2:
        print("使用方法: .\ExtractNftr.py <Nftr文件路径>")
    else:
        filepath = sys.argv[1]
        try:
            ExtractNftr(filepath)
        except FileNotFoundError:
            print(f"未找到路径为{filepath}的文件，请重新操作。")
