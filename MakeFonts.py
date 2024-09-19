import struct
from FreetypeMakeFonts import *
def MakeFont_1bppTo(char,FONT,fontsize,bpp,reshape = (0,0),method = "rightdownShadow"):
    #仅用于Freetype默认生成的是1bpp的字体，例如SIMSUN2
    if method == "blodShadow":
        blod = True
    else:
        blod = False
    font = CharBitmapCreator(char,FONT,fontsize = fontsize,blod=blod)
    bitmapbuffer = font.buffer
    if len(bitmapbuffer)==0:
        raise LookupError(f"生成的bitmapbuffer为0，当前字符为：{char}，生成字体失败！")
    if bpp == 1:
        data = bitmapbuffer
    elif bpp == 2:
        data = trans2bpp(bitmapbuffer)
    else:
        data = []
    if method == "rightdownShadow":
        buffer = rightdownShadow(data,bpp)
    elif method == "blodShadow":
        buffer = blodShadow(data,bpp)
    else:
        buffer = rightdownShadow(data,bpp)
    if reshape:
        width, height = reshape[0],reshape[1]
        buffer = reshape16(buffer,width=width,height=height,bpp=bpp,blod=blod)
    return buffer

def MakeFont_8bppTo(char,FONT,fontsize,bpp,reshape = (0,0)):#未完工
    bitmapbuffer = CharBitmapCreator(char,FONT,fontsize = fontsize).buffer

def main(CodeSource,FONT,ofilepath,bpp,fontsize = 12,reshape = (0,0),method = "rightdownShadow",bitmaps = '1bppTo'):
    Codelist = open(CodeSource,"rt",encoding="utf16")
    Fontlist = []
    for line in Codelist:
        if '==' in line:
            Fontlist.append('=')#防止映射为字符“=”被split处理掉
        else:
            s=line.split("=")
            Fontlist.append(s[1].strip("\n"))
    bufferList = []
    if bitmaps == '1bppTo':
        for char in Fontlist:
            bufferList.extend(MakeFont_1bppTo(char,FONT,fontsize,bpp,reshape,method = method))
    elif bitmaps == "8bppTo":
        for char in Fontlist:
            bufferList.extend(MakeFont_8bppTo(char,FONT,fontsize,bpp,reshape))
    else:
        raise TypeError("未指定正确的bpp转换类型。")
    with open(ofilepath,'wb') as f:
        for i in bufferList:
            f.write(struct.pack('B',i))

def main_CHS(CHSCodeSource,FONT,ofilepath,bpp,fontsize = 12,reshape = (0,0),method = "rightdownShadow",bitmaps = '1bppTo'):
    CHSCodelist = open(CHSCodeSource,"rt",encoding="utf16")
    CHSFontlist = []
    for line in CHSCodelist:
        trans = line.split("=")
        if '==' in line:#全码表会有=，但是中文码不需要
            continue
        s = trans[1].strip("\n")
        bo = (ord(s) >= 0x4E00) and (ord(s) <= 0x9FFF)#中文编码范围
        if bo:
            #print(s)
            CHSFontlist.append(s)
    bufferList = []
    if bitmaps == '1bppTo':
        for char in CHSFontlist:
            bufferList.extend(MakeFont_1bppTo(char,FONT,fontsize,bpp,reshape,method = method))
    elif bitmaps == "8bppTo":
        for char in CHSFontlist:
            bufferList.extend(MakeFont_8bppTo(char,FONT,fontsize,bpp,reshape))
    else:
        raise TypeError("未指定正确的bpp转换类型。")
    with open(ofilepath,'wb') as f:
        for i in bufferList:
            f.write(struct.pack('B',i))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 9:
        print("使用方法: python .\MakeFonts_main.py <中文码表文件> <中文字体文件：例如SIMSUN2.TTC> <bpp：1|2|4|8> \
        <字体大小> <单字模宽width> <单字模高height> <阴影方法：rightdownShadow|blodShadow> <输出文件路径>")
    else:
        CHSCodeSource = sys.argv[1]
        FONT = sys.argv[2]
        bpp = sys.argv[3]
        fontsize = sys.argv[4]
        width = sys.argv[5]
        height = sys.argv[6]
        method = sys.argv[7]
        ofilepath = sys.argv[8]
        reshape = (width,height)
        main_CHS(CHSCodeSource,FONT,ofilepath,bpp,fontsize = fontsize,reshape = reshape,method = method)


