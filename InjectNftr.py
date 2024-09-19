import csv
from struct import pack
from nftr import *
#把导出的字库文件导入各Nftr分片中
def InjectNftr(narcfilename):
    nftrpath = narcfilename+"_extr/"
    for i in range(3):
        filepath = nftrpath+narcfilename +"-"+ str(i)
        new = "_new"#修改
        #new = ""#复原
        with open(filepath,"rb")as f:
            rawdata = f.read()
            nftr = NFTR(rawdata)
            cdict = nftr.cwdh.width0123dict
            values = list(cdict.values())
            keys =list(cdict.keys())
            cdict_inv = {values[i]:keys[i] for i in range(len(keys))}
    
        #制造cwdh的新宽度表1
        csvfile = filepath + 'CWDH'+new+'.csv'
        with open(csvfile,"r") as r:
            reader = csv.DictReader(r)
            locs = []
            widths = []
            tags = []
            combs = []#cwdh的新宽度表1
            for row in reader:
                locs.append(int(row['loc']))#csv表全都是默认为str字串型
                widths.append(int(row['width']))
                tags.append(int(row['tag']))
        widthtable = []#还原表1拆开为2bit的样子
        for i in range(0,len(locs),4):
            k = 4
            comb = 0
            v = 0
            for j in range(k):
                if tags[i+j] == 1:
                    v = cdict_inv[widths[i+j]]
                    widthtable.append(v)
                else:
                    v = cdict_inv[0]
                    widthtable.append(v)
                comb = comb + (v << (2 * (k-j-1)))
            combs.append(comb)
    
        if combs == nftr.cwdh.widthtableComb:
            print("CWDH原封不动",True)
        else:
            print("已修改CWDH.")
        nftr.cwdh.widthtableComb = combs#替换掉原来的原始表1，待写入
    
        #修改周期表2和数组表3
        for i in locs:
            #print(widthtable[i])
            widthid = cdict[widthtable[i]]
            if widthid == 0:#计算周期表2的索引
                glyphidx = i#宽度表1元素按字模序排序，widthid等于3时的序数就是字模序
                cycleid = glyphidx & 0x1FF ^ (8
                               * (((glyphidx >> 9) ^ (glyphidx >> 11) ^ (glyphidx >> 12) ^ (glyphidx >> 10)) & 1)) & 0x1FF
                #print(cycleid)
    
                cid = nftr.cwdh.cycletable[cycleid]
                if cid > 128:#转换大数表示的有符号负数2^7 == 128用一个Byte表示数字的范围是0~128
                    cid -= 256
                if cid > 0:#是宽度
                    if cid != widths[glyphidx]:#新宽度和原宽度不同就替换
                        nftr.cwdh.cycletable[cycleid] = widths[glyphidx]
                        print("已修改第{}字符于 表2 的宽度值为：{}".format(glyphidx,widths[glyphidx]))
                elif cid < 0:#说明需要查表3
                    #print(cid)
                    #print(abs(cid))
                    arr = nftr.cwdh.arraytable[abs(cid)-1]#必须-1，第一项的下标是0
                    flag = -1
                    for k in arr[1]:
                        if k == glyphidx:#说明查表3找到了对应字模的宽度
                            if arr[1][glyphidx] != widths[glyphidx]:#新宽度和原宽度不同就替换
                                nftr.cwdh.arraytable[abs(cid)-1][1][glyphidx] = widths[glyphidx]
                                print("已修改第{}字符于 表3 的宽度值为：{}".format(glyphidx,widths[glyphidx]))
                            flag = 0
                            break
                    if flag == -1:
                        print("存在不可查值，字模序为：{}".format(glyphidx))
                else:
                    raise NameError("疑似出现字符宽度为0的状况")
            else:#0，1，2的情形，直接字典映射得到宽度，直接用combs替换表1不需要在此修改
                pass
        #print(len(combs))
        #print(combs)
    
        #替换码表
        i = 0
        for cmap in nftr.CMAPTable:
            idxs = list(cmap.CodeTableDict.keys())
            codes = list(cmap.CodeTableDict.values())
            with open(filepath +"序码表_"+str(i)+ new +".txt","r",encoding="utf16")as txt:
                lines = txt.readlines()
                if len(lines) > len(idxs):
                    raise LookupError("超出原始CMAP {}的可覆盖范围！".format(i))
                else:
                    nCodeTableDict = dict()
                    for j in range(len(lines)):
                        line = lines[j].replace("\n","")
                        if line[-1] == "=":#排除是=的情况
                            idx = line.split("=")[0]
                            char = "="
                        else:
                            idx, char = line.split("=")
                        #print(idx,idxs[j])
                        if "NULL" in idx:
                            if idx == idxs[j]:
                                nCodeTableDict[idx] = 0xFFFF
                        else:
                            if int(idx) == int(idxs[j]):
                                if codes[j] != ord(char):
                                    nCodeTableDict[int(idx)] = ord(char)
                                    print("已修改第{}个CMAP的第{}字符为：{}".format(i,idx,char))
                                else:
                                    nCodeTableDict[int(idx)] = codes[j]
                            else:
                                print(idx,idxs[j])
                                raise KeyError("对应第{}个CMAP的字模序发生改变！".format(i))
                    nftr.CMAPTable[i].CodeTableDict = nCodeTableDict
            i += 1
    
        #重组数据+字模
        csvfile = filepath + "宽度表"+new+".csv"
        with open(csvfile,"r",newline="")as f:
            datas = []
            reader = csv.reader(f)
            pos = 0
            for row in reader:
                if pos == 0:#csv标题不要
                    pos += 1
                    continue
                trans = list(map(int,row[1:]))#字模序不要
                datas.append(trans)
                pos += 1
        fontsize = nftr.cglp.tfontsize - 3#a023-0单字模大小为45Byte，a023-1单字模大小为25Byte，a023-2单字模大小为36Byte
        with open(filepath + new +".bitmap","rb")as f:
            buffer = f.read()
        if len(nftr.bitmaps) < len(datas):
            raise LookupError("超出字模序列可覆盖范围！")
        #print(nftr.cglp.fontsdata)
        #print(datas)
        for j in range(len(datas)):
            if nftr.cglp.fontsdata[j] != tuple(datas[j]):
                trans = b""
                for data in datas[j]:
                    trans += pack('B',data)
                nftr.cglp.tfonts[j] = trans + nftr.bitmaps[j]
                print("已修改第{}个字模的数据为：{}".format(j,datas[j]))
            if nftr.bitmaps[j] != buffer[j*fontsize:j*fontsize+fontsize]:#不要忘记*fontsize实现跨块读
                trans = b""
                for data in datas[j]:
                    trans += pack('B',data)
                nftr.cglp.tfonts[j] = trans + buffer[j*fontsize:j*fontsize+fontsize]
                print("已修改第{}个字模。".format(j))
    
        nfilepath = filepath#因为打包逻辑只认无后缀文件，必须直接导入原文件
        with open(nfilepath,"wb")as f:
            nftr.toFile(f)

if __name__ == "__main__":
    import sys,os
    #检查是否提供了参数
    if len(sys.argv) != 2:
        print("使用方法: python .\InjectNftr.py <原Narc的文件名>")
    else:
        narcname = sys.argv[1]
        extrpath = narcname+"_extr/"
        try:
            if os.path.exists(extrpath):
                InjectNftr(narcname)
            else:
                raise FileExistsError(f"{extrpath}不存在，请确认是否已利用ExtractNarc.py从目标Narc中正确提取了Nftr文件")
        except Exception as e:
            print(f"錯誤: {e}，请重新操作。")

