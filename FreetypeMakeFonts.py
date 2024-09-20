#This model is not completed. Particularly, 8bpp font methods need to improve, tough they are not effect in Projec PMBW.
import freetype,struct
from GlyphEntry import GlyphEntry
#Freetype对于SIMSUN2.TTC这类字体默认生成的字体是1bpp，一行2Byte；拓展为2bpp；拓展为N bpp 后，一行会变成2*N Byte
#Freetype对于其它字体一般是默认生成8bpp字体。
def CharBitmapCreator(char,FONT,fontsize = 12,blod = False):
    #由单字char和字体文件FONT生成width为fontsize的，实际宽度为16的1bpp的bitmap字模，对齐方式为左中（width是多少，生成的扫描阵就有多少行）
    face = freetype.Face(FONT)
    face.set_char_size( fontsize*64 )
    face.load_char(char)
    buffer = []#1bpp字体前加[0,0]就是填充一行
    bitmap = face.glyph.bitmap
    data, rows, width = bitmap.buffer, bitmap.rows, bitmap.width
    #print("默认生成的(宽度，长度)：",width, rows)
    #print(len(data))
    #print(data)
    if fontsize < 11:
        if bitmap.pixel_mode == 1:#Only make operation for 1bpp fonts
            #freetype.FT_PIXEL_MODES
            #{'FT_PIXEL_MODE_NONE': 0,'FT_PIXEL_MODE_MONO'（1bpp）: 1,
            # 'FT_PIXEL_MODE_GRAY'（8bpp）: 2, 'FT_PIXEL_MODE_GRAY2'（2bpp）: 3,
            # 'FT_PIXEL_MODE_GRAY4'（4bpp）: 4,'FT_PIXEL_MODE_LCD': 5,
            # 'FT_PIXEL_MODE_LCD_V': 6, 'FT_PIXEL_MODE_MAX': 7}
            buffer.extend(data[2:])
            buffer.extend(data[:2])
        else:
            buffer.extend(data)
    else:
        buffer.extend(data)
    if blod:
        buffer.extend([0,0])
    glyph = GlyphEntry(width = width, rows= rows,buffer = buffer)
    return glyph

def combineBytes(buffer,bpp):#将单Byte列表合并为扫描行列表（仅用于由1bpp拓展的字体）
    cmb = []
    for i in range(0, len(buffer)-bpp, 2*bpp):#通过实际的1bpp和2bpp处理的规律总结出来的递推公式
        I = 0
        for j in range(2*bpp):
            I = I | (buffer[i+(2*bpp-1 - j)] << 8*j)
        cmb.append(I)
    return cmb

def divedeCmb(cmb,bpp):#将经由combineBytes处理后的列表还原为单Byte列表
    buffer = []
    Bn = 2*bpp
    Bn += 1#保证右移次数
    for i in range(len(cmb)):
        Blist = []
        for j in range(Bn):
            if (Bn - 2 - j) < 0:#到负数就跳出，总右移次数刚好是2*bpp次
                break
            B = (cmb[i] >> 8*(Bn - 2 - j)) & 0xFF#右移8的倍数，最后一次(Bn - 2 - j)是0
            Blist.append(B)
        buffer.extend(Blist)
    return buffer

#经过combineByte处理后的字模数据实现整体右移
def Rightbuffer(rawList,bpp):
    RbufferList = []
    for raw in rawList:
        r = raw >> bpp
        RbufferList.append(r)
    return RbufferList

#经过combineByte处理后的字模数据实现整体下移
def Downbuffer(rawList):
    DbufferList = []
    DbufferList.extend(rawList[-1:])#把最后一行移到开头实现整体字形的下移(是0)
    DbufferList.extend(rawList[:-1])#切片不包括右界
    return DbufferList

#经过combineByte处理后的字模数据实现整体左移
def Leftbuffer(rawList,bpp):
    LbufferList = []
    for raw in rawList:
        r = raw << bpp
        LbufferList.append(r)
    return LbufferList

#经过combineByte处理后的字模数据实现整体上移
def Upbuffer(rawList):
    #print(rawList)
    UbufferList =[]
    UbufferList.extend(rawList[1:])#把第一行移到尾部实现整体自行的上移
    UbufferList.extend(rawList[:1])#extend只能对可迭代序列（列表）进行操作
    return UbufferList

def ByteDivToInt(Byte,keep,divnum = 1):#此处包括后续继承依赖此函数结果的方法仅能处理1bpp拓展字体
    #把1Byte拆成int(8/divnum)个【能拆成的个数只会是1,2,4】并只保留keep个2进制位的int
            bits = []
            if divnum > 4:#此时int(8/divnum)==1
                return Byte#相当于没拆
            if divnum == 1:#把Byte分成8个int，每个int是1位bit
                for i in range(8):
                    bit = (Byte >> (7-i)) & keep
                    bits.append(bit)
            elif divnum in [2,4]:#把Byte分成4个int，每个int是2位bit
                flag = 0
                mask = 2**divnum-1#保留的二进制位→2bpp就是1Byte拆成4份，各用0x3保留2个位
                while Byte:
                    #print(B & mask)
                    bits.insert(0,Byte & mask)#必须用insert保证顺序（上下保持一致）
                    Byte = Byte >> divnum
                    flag += 1
                if 8 - flag*divnum:#没有用到前面的int((8 - flag*bpp)/bpp)个2进制位，补0
                    #print(int((8 - flag*bpp)/bpp))
                    for i in range(int((8 - flag*divnum)/divnum)):
                        bits.insert(0,0)
            else:
                raise TypeError("无法将Byte平均拆成{}个。".format(divnum))
            return bits
def combinebpp(pixel,bpp):#输入被ByteDivToInt拆开的Byte列表（也可是已经按bpp分开的bits列表），将其按照bpp重组为新的Byte构成列表
    Bytelist = []
    flag = 0
    B = 0
    if bpp == 1:#其实实现逻辑和下方的bpp==n相同，只不过使用的程序表达方法不同
        for i in range(len(pixel)):
            if flag == 7:
                    B = B | pixel[i]
                    Bytelist.append(B)
                    B = 0
                    flag = 0
            else:
                    pixel[i] = pixel[i] << (7 - flag)
                    B = B | pixel[i]
                    flag += 1
    else:
        for i in range(0, len(pixel)-(2*bpp-1), 2*bpp):
            B = 0
            for j in range(2*bpp):
                B = B | pixel[i+j] << ((2*bpp-1)-j)*bpp
            Bytelist.append(B)
    return Bytelist

def debpp(buffer,width,bpp = 8, dbpp = 4,method = 'gamma'):#将高bpp的字模降级为低bpp的字模（一般用于8bpp字体）
    Bytes = []
    pixels = []
    def linear_scale(value):
        return int(value/(2**bpp-1)*(2**dbpp-1))
    import math
    def log_scale(value):
        return int((2**dbpp-1) * (math.log(value + 1) / math.log((2**bpp))))
    def gamma_correct(value,gamma=2.2):
        normalized = value / (2**bpp-1)
        corrected = normalized ** (1.0 / gamma)
        return int(corrected * (2**dbpp-1))
    if bpp == 8 and bpp % 2 == 0:
        divnum = int(bpp/dbpp)#Byte分成divnum个dbpp的Byte
        for B in buffer:
            if method == 'gamma':
                value = gamma_correct(B)
            elif method == 'linear':
                value = linear_scale(B)
            elif method == "log":
                value = log_scale(B)
            else:
                value = gamma_correct(B)

            pixel = value & 0xFF
            Bytes.append(pixel)
        if width%int(8/divnum):#是奇数，每行都要填充
            NBytes = []
            for i in range(0,len(Bytes),width):
                NBytes.extend(Bytes[i:i+width])
                NBytes.append(0)#填充
            Bytes = NBytes
        for i in range(0,len(Bytes),divnum):#按Byte组合
            NB = 0
            for j in range(divnum):
                NB = NB | (Bytes[i+(divnum-1-j)] << dbpp*j) & 0xFF
            pixels.append(NB)
    else:
        print("还未有定义8bpp字体之外的降级方法。")
        pixels = []
    return pixels
def trans2bpp(buffer,keep = 1):#仅用于将1bpp字体拓展为2bpp字体
        converted_data = []# 创建一个新的列表，用于存储转换后的 2bpp 索引数据
        # 遍历原始列表中的每个数值
        for value in buffer:
            # 提取每个像素的索引
            pixel = ByteDivToInt(value, keep)#keep == 1是无阴影，keep == 3就是带右阴影

            for i in range(8):
                if pixel[i] == 3:#字库字模没有用到3索引对应的颜色
                    pixel[i] = 1

            ByteList = combinebpp(pixel,2)

            # 将像素索引添加到新的列表中
            converted_data.extend(ByteList)
        #print(converted_data)
        return converted_data

def changecolor(rawList,bpp=2):#输入combineBytes生成的点阵扫描行列表，输出变色后的Bytes列表
    buffer = divedeCmb(rawList,bpp)#还原为Byte列表
    pixels = []
    mask = 2**bpp-1#保留的二进制位→2bpp就是用0x3保留2个位
    for B in buffer:#按bpp分离bit
        pixels.extend(ByteDivToInt(B,bpp,bpp))
    for i in range(len(pixels)):#变色
        if pixels[i] != 0:
            #print(pixels[i])
            pixels[i] = (pixels[i] + 1) & mask #不为零的像素索引+1，&mask实现限定数值范围在bpp位内，是索引顺序循环，由此实现变色
    #还原为Bytes列表
    Newbuffer = combinebpp(pixels,2)
    return Newbuffer#输出的是Bytes列表

def combShadow2bpp(sbuffer1,sbuffer2):#输入字模Bytes列表制造组合阴影，例如右下阴影：buffer1右阴影，sbuffer2下阴影
    pixels1 = []
    pixels2 = []
    resultpixels = []
    for i in range(len(sbuffer1)):
        pixels1.extend(ByteDivToInt(sbuffer1[i],2,2))
        pixels2.extend(ByteDivToInt(sbuffer2[i],2,2))
    for i in range(len(pixels1)):
        trans = pixels1[i] | pixels2[i]
        resultpixels.append(trans)
    Newbuffer = combinebpp(resultpixels,2)
    return Newbuffer

def fillShadow2bpp(buffer,shadowbuffer):#输入字模的Byte_buffer列表和阴影对应的shawdownbuffer_Byte列表，两列表的长度应一致
    pixels = []
    shadowpixels = []
    resultpixels = []
    for i in range(len(buffer)):
        pixels.extend(ByteDivToInt(buffer[i],2,2))
        shadowpixels.extend(ByteDivToInt(shadowbuffer[i],2,2))
    for i in range(len(pixels)):
        if pixels[i] and shadowpixels[i]:
            trans = (pixels[i] ^ shadowpixels[i]) >> 1#异或后左移只保留1
        else:
            trans = pixels[i] ^ shadowpixels[i]#异或只保留不为0的部分
        resultpixels.append(trans)
    Newbuffer = combinebpp(resultpixels,2)
    return Newbuffer
def full_Q(buffer,width,height,Awidth,bpp):
    #输入宽度小于等于width的字模Bytes列表，将其填充到长宽为Awidth的方形字模Bytes列表
    # 规定Awidth>=原始width和height，由此填充（用于一般的8bpp字体）
    addh = Awidth - height#需填充的扫描行数字模高度与宽度变化无关，先得出
    if bpp < 8:#说明降过bpp
        if width%(8 / bpp):#宽度不是偶数就需要补齐，输入的buffer是经过debpp已经补齐过的
            width += int(width%(8 / bpp))
        ColoBytesNum = int(width /(8 / bpp))#构成一个扫描行的Byte数
        Awidth = int(Awidth/(8 / bpp))
    else:
        ColoBytesNum = width
    addw = Awidth - ColoBytesNum#每行需填充的Byte数
    AddRow = [0 for i in range(Awidth)]
    Newbuffer = []
    #增宽
    for i in range(0,height):#每行填充addw个值为0的Byte实现增宽
        Newbuffer.extend(buffer[ColoBytesNum*i:ColoBytesNum*i+ColoBytesNum])
        Newbuffer.extend([0 for j in range(addw)])
    #增高
    if addh % 2:#除不尽头部少加
        fnum = int(addh/2)#加在头部的行数
        lnum = int(addh/2)+1#加在尾部的行数
    else:
        fnum = int(addh/2)
        lnum = fnum
    transbuffer = []
    for i in range(fnum):
        transbuffer.extend(AddRow)
    for i in range(lnum):
        Newbuffer.extend(AddRow)
    Newbuffer = transbuffer + Newbuffer

    return Newbuffer

def reshape16(buffer,width,height,bpp,blod = False):
    #输入宽度小于等于16的没有填充的字模Bytes列表，规定>=原始width和height，由此填充（仅用于1bpp拓展的字体）
    if (width * width)*bpp/8 > len(buffer):
        raise KeyError(f"指定的width：{width}与字模大小不匹配，width * height应该小于{len(buffer)}")
    transbuffer = combineBytes(buffer,bpp)
    addh= height-len(transbuffer)
    pixelnum = 16
    for i in range(addh):
        if i == 0:
            transbuffer.insert(0,0)#只在第一个扫描行前增加一行黑色填充
        else:
            transbuffer.append(0)#其它填充扫描行加在尾部
    if blod:#有加粗就让字体顶格
        ntbuffer = transbuffer[1:]
        ntbuffer.extend(transbuffer[:1])
        transbuffer = ntbuffer
    for i in range(len(transbuffer)):
        transbuffer[i] = transbuffer[i] >> (16 - width)*bpp#生成的字体默认宽度永远都是16
    transbuffer = divedeCmb(transbuffer,bpp)#复原为Bytes列表
    bitsbuffer = []
    for i in range(len(transbuffer)):#按bpp拆成对应的bits列表
        bitsbuffer.extend(ByteDivToInt(transbuffer[i],keep=bpp,divnum=bpp))
    delnum = pixelnum - width
    if pixelnum - delnum < 1:
        raise ValueError("预裁剪部分超出可裁剪范围！")

    #按bit裁剪
    bits = []
    if delnum:#裁剪掉多余的bit
        for i in range(0,len(bitsbuffer),pixelnum):
            for j in range(delnum):
                bitsbuffer[i+j] = "NULL"
        for b in bitsbuffer:
            if b != "NULL":
                bits.append(b)
        #print(len(bits))
        if (len(bits)*bpp) % 8:
            for i in range(int((len(bits)*bpp) % 8/bpp)):
                bits.append(0)#向上取整
        #print(len(bits))
    Newbuffer = combinebpp(bits,bpp)
    return Newbuffer

def blodShadow(buffer,bpp):#输入字模Byte数据，输出对应字模的加边后的Byte数据。默认字模是最靠左的
    raw = combineBytes(buffer,bpp)
    rraw = Rightbuffer(raw,bpp)
    rrraw = Rightbuffer(rraw,bpp)
    draw = Downbuffer(raw)
    ddraw = Downbuffer(draw)
    rdraw = Downbuffer(rraw)
    rdlraw = Leftbuffer(rdraw,bpp)
    rdrraw = Rightbuffer(rdraw,bpp)
    rddraw = Downbuffer(rdraw)
    rrdraw = Downbuffer(rrraw)
    rrddraw = Downbuffer(rrdraw)
    rdbuffer = divedeCmb(rdraw,bpp)
    cbuffer = changecolor(raw,bpp)#变色操作只能在移动后才能使用
    crbuffer = changecolor(rraw,bpp)
    cddbuffer = changecolor(ddraw,bpp)
    crddbuffer = changecolor(rddraw,bpp)
    crrbuffer = changecolor(rrraw,bpp)
    crrddbuffer = changecolor(rrddraw,bpp)
    crdrbuffer = changecolor(rdrraw,bpp)
    crdlbuffer = changecolor(rdlraw,bpp)

    shalist = [cbuffer,crbuffer,cddbuffer,crddbuffer,crrbuffer,crrddbuffer,crdrbuffer,crdlbuffer]
    blodbuffer = cbuffer
    if bpp == 2:
        for i in range(len(shalist)):
            blodbuffer = combShadow2bpp(blodbuffer,shalist[i])#生成全方位阴影
    blodbuffer = fillShadow2bpp(rdbuffer,blodbuffer)#将全方位阴影应用于右下移过的字模实现加边
    return blodbuffer

def rightdownShadow(buffer,bpp):
    raw = combineBytes(buffer,bpp)
    rraw = Rightbuffer(raw,bpp)
    draw = Downbuffer(raw)
    rdraw = Downbuffer(rraw)
    crbuffer = changecolor(rraw,bpp)#变色操作只能在移动后才能使用
    cdbuffer = changecolor(draw,bpp)
    crdbuffer = changecolor(rdraw,bpp)
    shalist = [crbuffer,cdbuffer,crdbuffer]
    rdbuffer = crbuffer
    if bpp == 2:
        for i in range(len(shalist)):
            rdbuffer = combShadow2bpp(rdbuffer,shalist[i])
    rdbuffer = fillShadow2bpp(buffer,rdbuffer)
    return rdbuffer



if __name__ == "__main__":#This is just for code testing
    def bpp1To2test():#1bpp拓展到2bpp的SIMSUN2字体一条龙测试
        char = "白"
        FONT = 'SIMSUN2.TTC'
        fontsize = 10
        bitmapbuffer = CharBitmapCreator(char,FONT,fontsize = fontsize).buffer
        data = trans2bpp(bitmapbuffer,1)
        reshapdata = reshape16(data,width=fontsize+1,height=fontsize+3,bpp=2)
        mainbuffer = combineBytes(data,2)
        rraw = Rightbuffer(mainbuffer,2)
        draw = Downbuffer(mainbuffer)
        rdraw = Downbuffer(rraw)
        rdlraw = Leftbuffer(rdraw,2)
        rdluraw = Upbuffer(rdlraw)
        rbuffer = divedeCmb(rraw,2)
        dbuffer = divedeCmb(draw,2)
        rdbuffer = divedeCmb(rdraw,2)
        rdlbuffer = divedeCmb(rdlraw,2)
        rdlubuffer = divedeCmb(rdluraw,2)
        rcolorbuffer = changecolor(rraw,2)#变色操作只能在移动后才能使用
        dcolorbuffer = changecolor(draw,2)
        rdclorbuffer = changecolor(rdraw,2)
        rdshabuffer = combShadow2bpp(rcolorbuffer,dcolorbuffer)
        rdshabuffer = combShadow2bpp(rdshabuffer,rdclorbuffer)
        rd_buffer = rightdownShadow(data,2)
        bloddata = trans2bpp(CharBitmapCreator(char,FONT,fontsize = fontsize,blod=True).buffer,1)
        blod_buffer = blodShadow(bloddata,2)

        reshapebuffer = reshape16(blod_buffer,width=fontsize+1,height=fontsize+3,bpp=2,blod=True)
        buffer = fillShadow2bpp(data,rdshabuffer)
        datas = [data,rbuffer,dbuffer,rdlbuffer,rdlubuffer,
                 rcolorbuffer,dcolorbuffer,rdshabuffer,buffer,rd_buffer,blod_buffer]
        with open('testfont.bin','wb')as f:
            for data in datas:
                for i in data:
                    f.write(struct.pack('B',i))
        reshapelist = [reshapdata,reshapebuffer]
        with open("testfont",'wb') as f:
            for d in reshapelist:
                for i in d:
                    f.write(struct.pack('B',i))
        '''with open("testfont",'wb') as f:
            for I in combineBytes(data,2):
                f.write(struct.pack('>I',I))#由于是正向扫描点阵长字节必须大端写
        with open("testfont",'wb') as f:
            for I in combineBytes(bitmapbuffer,1):
                f.write(struct.pack('>H',I))
        with open("testfont",'wb') as f:
            for I in divedeCmb(combineBytes(bitmapbuffer,1),1):
                f.write(struct.pack('B',I))'''
    def bpp8To4test():#8bpp到4bpp的字体降级测试
        char = "_"
        FONT = 'FZKT_GBK.ttf'
        fontsize = 24
        font = CharBitmapCreator(char,FONT,fontsize = fontsize)
        bitmapbuffer = font.buffer
        print(font.width,font.rows)
        sourcebuffer = debpp(bitmapbuffer,width=font.width, bpp = 8, dbpp = 4,method = 'gamma')
        qbuffer = full_Q(sourcebuffer,font.width,font.rows,fontsize,4)
        with open('testfont_8to4bpp','wb')as f:
            for data in sourcebuffer:
                    f.write(struct.pack('B',data))
        with open('testfont_8to4bpp_Q',"wb")as f:
            for data in qbuffer:
                    f.write(struct.pack('B',data))
    bpp1To2test()
    #bpp8To4test()
