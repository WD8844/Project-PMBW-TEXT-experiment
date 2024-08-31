import csv
from nftr import *

def ExtractNftr(filename):
    with open(filename,'rb')as f:
        f.seek(0)
        rawdata = f.read()
        print("len(rawdata)",len(rawdata))
        nftr = NFTR(rawdata)
        with open(filename + "宽度表.csv","w",newline="")as w:
            writer = csv.writer(w)
            writer.writerow(["loc","left","width","advance"])
            for i in range(len(nftr.fontsdata)):
                l = [i]
                l.extend(nftr.fontsdata[i])
                writer.writerow(l)
        with open(filename + "CWDH.csv","w",newline="")as w:
            writer = csv.writer(w)
            writer.writerow(["loc","width","tag"])
            widthtable = nftr.cwdh.WidthTable
            for i in range(len(widthtable)):
                trans = [i]
                trans.extend(widthtable[i])
                writer.writerow(trans)
        with open(filename + ".bitmap","wb")as w:
            for bitmap in nftr.bitmaps:
                w.write(bitmap)
        i = 0
        for cmap in nftr.CMAPTable:
            idxs = list(cmap.CodeTableDict.keys())
            codes = list(cmap.CodeTableDict.values())
            with open(filename +"序码表_"+str(i)+ ".txt","w",encoding="utf16")as w:
                for j in range(len(idxs)):
                    s = str(idxs[j]) + "=" + chr(codes[j])+"\n"
                    w.write(s)
            i += 1

import sys

def main():
    # 检查是否提供了参数
    
    if len(sys.argv) != 2:
        print("使用方法: ExtractNftr.py <文件名>")
        return
    
    filename = sys.argv[1]
    
    try:
        dirname = filename+'_extr'
        ExtractNftr(filename,dirname,type = 'text')
    except FileNotFoundError:
        print(f"未找到名为{filename}的文件，请重新操作。")

if __name__ =="__main__":
    main()
    
