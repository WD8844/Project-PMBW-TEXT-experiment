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

if __name__ == "__main__":
    dirname = 'a023_extr/'
    for i in range(3):
        filename = dirname + "a023-" + str(i)
        ExtractNftr(filename)
