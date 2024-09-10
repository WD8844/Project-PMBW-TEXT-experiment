from struct import unpack,pack
#数值单位：Byte
class FINF:
    def __init__(self,rawdata,FINFoffset):
        if len(rawdata)>0:
            self.magic = rawdata[:4]
            if self.magic != b"FNIF":
                print(self.magic)
                raise NameError("FINF tag not found")
            self.header = unpack("IBBHBBBBIII", rawdata[4:28])
            self.offset = FINFoffset
        else:
            self.magic = b"FNIF"
            self.header = [0 for i in range(11)]
    def getSize(self):
        return self.header[0]
    def getFontType(self):#0x0 - Bitmap, 0x1 - TGLP
        if self.header[1] == 0:
            return 'Bitmap'
        elif self.header[1] == 1:
            return 'TGLP'
        else:
            return self.header[1]
    def getLeft(self):
        #[默认字模宽度，默认字模高度]2Byte大端模式数就右移得到正确的小端模式值
        return self.header[4]
    def getWidth(self):
        return self.header[5]
    def getAdvance(self):#默认字模间距
        return self.header[6]
    def getEncoding(self):#0x0 - UTF-8, 0x1 - UTF-16, 0x2 - ShiftJIS, 0x3 - CP1252
        if self.header[7] == 0:
            return 'utf-8'
        elif self.header[7] == 1:
            return 'utf-16'
        elif self.header[7] == 2:
            return 'shift_jis'
        elif self.header[7] == 3:
            return 'cp1252'
        else:
            return self.header[7]
    def getCDWHinner_offset(self):
        return self.header[-2]
    def getCMAP_offset(self):
        return self.header[-1]
    def toString(self):
        #打包header
        ret = b"FNIF" + pack("IBBHBBBBIII", self.header[0],self.header[1],
                             self.header[2],self.header[3],
                             self.header[4],self.header[5],self.header[6],
                             self.header[7],self.header[8],
                             self.header[9],self.header[10])
        return ret
class CGLP:
    def __init__(self, rawdata, CGLPoffset):
        self.offset = CGLPoffset#CGLP的绝对偏移地址
        if len(rawdata)>0:
            self.magic = rawdata[:4]
            if self.magic != b"PLGC":
                print(self.magic)
                raise NameError("CGLP tag not found")
            self.header = unpack("IBBHBBBB", rawdata[4:16])
            self.bitmapdatasize = 3
        else:
            self.magic = b"PLGC"
            self.header = [0 for i in range(8)]
        self.size = self.header[0]#CGLP段总大小（包括header）
        self.width = self.header[1]#默认字模宽度
        self.height = self.header[2]#默认字模高度
        self.tfontsize = self.header[3]#字模及其数据大小
        self.basline = self.header[4]
        self.Maxwidth = self.header[5]
        self.bpp = self.header[6]#默认颜色位数
        rawdata = rawdata[16:]

        self.fonts = []
        self.fontsdata = []
        self.tfonts = []
        if len(rawdata) > 0:
            pos = 0
            i = 0
            while pos < self.size - 16:
                datafont = rawdata[i*self.tfontsize:i*self.tfontsize + self.tfontsize]
                self.tfonts.append(datafont)
                self.fontsdata.append(unpack('BBB',datafont[:self.bitmapdatasize]))#字模数据
                self.fonts.append(datafont[self.bitmapdatasize:])#字模
                i += 1
                pos += self.tfontsize

    def getCWDH_offset(self):
        offset = self.size + self.offset
        #print(hex(offset))
        return offset#所有字模点阵数据之后就是CWDH
    def getFonts(self):
        return self.fonts
    def getFontsData(self):
        return self.fontsdata
    def toString(self):
        #打包header
        ret = b"PLGC" + pack("IBBHBBBB",self.size,self.width,
                             self.height,self.tfontsize ,
                             self.basline, self.Maxwidth ,self.bpp,
                             self.header[7])
        #打包数据+字模
        for buffer in self.tfonts:
            ret += buffer
        l = len(ret)#对齐4Byte，需补齐时填充0
        while l%4:
                l += 1
                ret += b"\x00"
        return ret

class CWDH:
    def __init__(self,rawdata,CWDHoffset):
        self.offset = CWDHoffset
        self.widthtableComb = []#没有拆成2bit的原始Byte表1
        self.widthtable = []
        self.cycletable = []
        self.arraytable =[]
        if len(rawdata) > 0:
            self.magic = rawdata[:4]
            if self.magic != b"HDWC":
                print(self.magic)
                raise NameError("CWDH tag not found")
            self.header = unpack('IBBBBIII',rawdata[4:24])
        else:
            self.magic = b"HDWC"
            self.header = [0 for i in range(8)]
        self.size = self.header[0]#CWDH段总长度（包括header）
        self.width0123dict = {0:self.header[1],1:self.header[2],2:self.header[3],3:self.header[4]}#表1宽度索引表的索引0，1，2对应的宽度，3表示查表2周期化的宽度表
        self.widthtable8offset = self.offset + self.header[5] + 8#表1宽度索引表的起始地址
        self.cycletable8offset = self.offset + self.header[6] + 8#表2周期化的宽度表的起始地址
        self.arraytable8offset = self.offset + self.header[7] + 8#表3宽度检索表的起始地址
        print("widthtable8offset:",hex(self.widthtable8offset))
        print("cycletable8offset:",hex(self.cycletable8offset))
        print("arraytable8offset",hex(self.arraytable8offset))
        #只有表1和表3是直接可得的，表2依赖字模序，字模序依表1

        rawdata = rawdata[24:]#此时就是表1开头

        widthtableSize = self.cycletable8offset - self.widthtable8offset
        cycletableSize = self.arraytable8offset - self.cycletable8offset
        arraytableSize = self.size - (self.header[7] + 8)
        #print(widthtableSize)
        #print(cycletableSize)
        #print(arraytableSize)
        if len(rawdata)>0:
                for i in range(widthtableSize):#提取表1
                    k = 4
                    B = rawdata[i]
                    self.widthtableComb.append(B)
                    #print(B)
                    for j in range(k):#2bit一个宽度索引
                        self.widthtable.append(B >> (2 * (k-j-1)) & 3)
        print("len(self.widthtable):",len(self.widthtable))
        #print(self.widthtable)
        rawdata = rawdata[widthtableSize:]
        if len(rawdata)>0:#提取表2
                for i in range(cycletableSize):
                    self.cycletable.append(rawdata[i])

        rawdata = rawdata[cycletableSize:]
        print("len(self.cycletable):",len(self.cycletable))
        if len(rawdata)>0:#提取表3
                i = 0
                while arraytableSize - i -1 > 0:
                    arrays = []
                    kvnum = rawdata[i]
                    arrays.append(kvnum)
                    i += 1
                    key_value = dict()
                    while kvnum > 0:
                        loc = unpack('>H', rawdata[i:i+2])[0]#索引数是大端模式
                        i += 2
                        width = rawdata[i]
                        i += 1
                        key_value[loc] = width
                        kvnum -= 1
                    arrays.append(key_value)
                    self.arraytable.append(arrays)
                #print(arrays)
        print("len(self.arraytable):",len(self.arraytable))
        #print(self.arraytable)
        self.WidthTable = []#翻译表1-2-3得到的真宽度表（按字模序排列）
        if self.arraytable and self.widthtable and self.cycletable:
                for i in range(len(self.widthtable)):
                    #print(self.widthtable[i])
                    widthid = self.width0123dict[self.widthtable[i]]
                    tag = 1
                    if widthid == 0:#计算周期表2的索引
                        glyphidx = i#宽度表1元素按字模序排序，widthid等于3时的序数就是字模序
                        cycleid = glyphidx & 0x1FF ^ (8
                                       * (((glyphidx >> 9) ^ (glyphidx >> 11) ^ (glyphidx >> 12) ^ (glyphidx >> 10)) & 1)) & 0x1FF
                        #print(cycleid)
                        cid = self.cycletable[cycleid]
                        if cid > 128:#转换大数表示的有符号负数2^7 == 128用一个Byte表示数字的范围是0~128
                            cid -= 256
                        if cid > 0:#是宽度
                            tag = 2
                            self.WidthTable.append([cid,tag])
                        elif cid < 0:#说明需要查表3
                            tag = 3
                            #print(cid)
                            #print(abs(cid))
                            arr = self.arraytable[abs(cid)-1]#必须-1，第一项的下标是0
                            flag = -1
                            for k in arr[1]:
                                if k == glyphidx:#说明查表3找到了对应字模的宽度
                                    self.WidthTable.append([arr[1][glyphidx],tag])
                                    flag = 0
                                    break
                            if flag == -1:
                                print("存在不可查值，字模序为：{}".format(glyphidx))
                        else:
                            raise NameError("疑似出现字符宽度为0的状况")
                    else:#0，1，2的情形，直接字典映射得到宽度
                        self.WidthTable.append([widthid,tag])
                print("len(self.WidthTable):",len(self.WidthTable))

    def getSize(self):
        return self.header[0]
    def getWidthIDtable(self):
        return self.widthtable
    def getArrayIDtable(self):
        return self.arraytable
    def getWidthTable(self):
        return self.WidthTable
    def toString(self):
        #打包header
        ret = b"HDWC" + pack('IBBBBIII',self.size,self.header[1],
                             self.header[2],self.header[3],
                             self.header[4],self.header[5],
                             self.header[6],self.header[7])
        #打包三个表
        for B in self.widthtableComb:
            ret += pack('B',B)
        for B in self.cycletable:
            ret += pack('B',B)
        for arr in self.arraytable:
            trans = pack("B",arr[0])
            for k in arr[1]:
                trans = trans + pack(">H",k) + pack('B',arr[1][k])
            ret += trans
        l = len(ret)#对齐4Byte，需补齐时填充0
        while l%4:
                l += 1
                ret += b"\x00"
        return ret

class CMAP:
    def __init__(self, rawdata):
        if len(rawdata) > 0:
            self.magic = rawdata[:4]
            if self.magic != b'PAMC':
                raise NameError("CMAP tag not found")
            self.header = unpack("IHHHHI",rawdata[4:20])
        else:
            self.magic = b'PAMC'
            self.header = [0 for i in range(6)]
        self.size = self.header[0]
        self.codeBegin = self.header[1]
        self.codeEnd = self.header[2]
        self.mapMethod = self.header[3]
        self.resever = self.header[4]
        self.nextCMAP8offset = self.header[5]
        #导出码表
        rawdata = rawdata[20:]
        self.CodeTableDict = dict()
        if self.mapMethod == 0x0:#由起始、终止编码和起始字模序导出码表
                glyphidx = unpack('I', rawdata[:4])[0]
                interval = self.codeEnd - self.codeBegin
                for i in range(interval+1):
                    code = self.codeBegin + i
                    self.CodeTableDict[glyphidx] = code
                    glyphidx += 0x1
        elif self.mapMethod == 1:#由起始、终止编码和表内的字模序导出码表
                interval = self.codeEnd - self.codeBegin
                i = 0
                while i <= interval :
                    glyphidx = unpack('H',rawdata[i*2:i*2+2])[0]
                    if glyphidx != 0xFFFF:
                        code = self.codeBegin + i
                        self.CodeTableDict[glyphidx] = code
                    else:
                        self.CodeTableDict["NULL"+str(i)] = 8251#※
                    i += 1
        elif self.mapMethod == 0x2:#直接扫描[字符编码，字模序]对导出码表
                if self.codeBegin!=0x0000 or self.codeEnd!=0xffff:
                    raise NameError("起始和终止码不是0x0000和0xFFFF:{},{}".format(self.codeBegin,self.codeEnd))
                totalnum = unpack("H",rawdata[:2])[0]
                rawdata = rawdata[2:]
                i = 0
                while i < totalnum:
                    codeidx = unpack("HH",rawdata[i*4:i*4+4])
                    self.CodeTableDict[codeidx[1]] = codeidx[0]
                    i += 1
        else:
                raise NameError("mapMethod not defined")

    def getSize(self):
        return self.size
    def getBegin_FontCode(self):
        return self.codeBegin
    def getEnd_FontCode(self):
        return self.codeEnd
    def getNextCMAP_offset(self):
        return self.nextCMAP8offset - 8
    def toString(self):
        ret = b'PAMC' + pack("IHHHHI",self.size,self.codeBegin,
        self.codeEnd,self.mapMethod,
        self.resever,self.nextCMAP8offset)
        if self.mapMethod == 0x0:
            #打包起始字模序
            fglyphidx = list(self.CodeTableDict.keys())[0]
            ret += pack('I',fglyphidx)
        elif self.mapMethod == 0x1:
            #打包字模序码表
            for idx in self.CodeTableDict:
                if self.CodeTableDict[idx] == 0xffff:
                    ret += pack('H',0xFFFF)
                else:
                    ret += pack('H',idx)
        elif self.mapMethod == 0x2:
            #打包序对数量
            ret += pack("H",len(self.CodeTableDict))
            #打包[编码,字模序]码表
            for idx in self.CodeTableDict:
                trans = pack('H',self.CodeTableDict[idx]) + pack('H',idx)
                ret += trans
        else:
            raise NameError("mapMethod not defined")
        l = len(ret)#对齐4Byte，需补齐时填充0
        while l%4:
                l += 1
                ret += b"\x00"
        return  ret
class NFTR:
    def __init__(self, rawdata):
        self.size = len(rawdata)
        if len(rawdata)>0:
            self.magic = rawdata[:4]
            self.header = unpack("IIHH", rawdata[4:16])
            self.FINFoffset = self.header[2]
            if self.magic != b"RTFN":
                print(self.magic)
                raise NameError("NFTR tag not found")
        else:
            self.magic = b"RTFN"
            self.header = [0 for i in range(4)]
        rawdata = rawdata[16:]
        self.finf = FINF(rawdata, self.FINFoffset)
        CGLPoffset = self.FINFoffset + self.finf.getSize()
        rawdata = rawdata[self.finf.getSize():]
        self.cglp = CGLP(rawdata, CGLPoffset)
        self.fontsdata = self.cglp.getFontsData()
        self.bitmaps = self.cglp.getFonts()
        CWDHoffset = self.cglp.getCWDH_offset()
        rawdata = rawdata[self.cglp.size:]
        self.cwdh = CWDH(rawdata,CWDHoffset)
        self.WidthTable = self.cwdh.WidthTable
        rawdata = rawdata[self.cwdh.getSize():]
        cmap = CMAP(rawdata)
        self.CMAPTable = [cmap]
        rawdata = rawdata[cmap.getSize():]
        while cmap.getNextCMAP_offset() < self.size:
            cmap = CMAP(rawdata)
            self.CMAPTable.append(cmap)
            rawdata = rawdata[cmap.getSize():]
            if len(rawdata) == 0:
                print("nftr文件的全部数据处理完毕。")
                break
    def toString(self):
        #打包header
        ret = b"RTFN" +pack("IIHH",self.header[0],self.header[1],self.FINFoffset,self.header[3])
        #按顺序打包FINF+CGLP+CWDH+CMAPs
        ret += self.finf.toString() + self.cglp.toString() + self.cwdh.toString()
        for cmap in self.CMAPTable:
            ret += cmap.toString()
        return ret
    def toFile(self, f):
        f.write(self.toString())

if __name__ =="__main__":#Just for code testing
    import csv
    filepath = 'a023_extr/a023-0'
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

