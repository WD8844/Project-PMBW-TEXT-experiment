import array

class binaryreader:
    def __init__(self, string):
        self.s = array.array('H',string)#相当于初始化了一个2Byte字节流读取窗格
        self.ofs = 0
        self.ReadUInt16 = self.read16
        self.ReadUInt32 = self.read32
        self.Seek = self.seek
    def read16(self):#2Byte窗格扫描字节流s 每次调用顺序向后读2Byte（即16bit）
        ret = self.s[self.ofs]
        self.ofs += 1
        return ret
    def read32(self):#4Byte窗格扫描字节流s 每次调用顺序向后读4Byte（即32bit）
        ret = self.s[self.ofs] | (self.s[self.ofs+1]<<16)
        self.ofs += 2
        return ret
    def seek(self, ofs):#返回当前文件指针的位置
        self.ofs = ofs>>1
        
class binarywriter:
    def __init__(self):
        self.s = array.array('H')#相当于初始化了一个2Byte字节流写入窗格
    def write16(self, i):#按2Byte将i作为预写入字节流加入预写入表s
        self.s.append(i)
    def write32(self, i):#按4Byte将i作为预写入字节流加入预写入表s
        self.s.append(i&0xFFFF)
        self.s.append((i>>16)&0xFFFF)
    def writear(self, a):#按2Byte将a作为预写入字节流加入预写入表s
        self.s.extend(a)
    def tobytes(self):
        return self.s.tobytes()#得到预写入的整个字节流
    def toarray(self):#返回整个预写入表s
        return self.s
    def pos(self):#当前文件指针的位置
        return len(self.s)<<1
