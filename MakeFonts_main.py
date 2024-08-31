import struct
from FreetypeMakeFonts import *
def MakeFont_1bppTo(char,FONT,fontsize,bpp,reshape = (0,0),method = "rightdownShadow"):
    #仅用于Freetype默认生成的是1bpp的字体，例如SIMSUN2
    if method == "blodShadow":
        blod = True
    else:
        blod = False
    bitmapbuffer = CharBitmapCreator(char,FONT,fontsize = fontsize,blod=blod)
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

def MakeFont_8bppTo(char,FONT,fontsize,bpp,reshape = (0,0)):
    bitmapbuffer = CharBitmapCreator(char,FONT,fontsize = fontsize)

def main(CHSCodeSource,FONT,ofilename,bpp,fontsize = 12,reshape = (0,0),method = "rightdownShadow",bitmaps = '1bppTo'):
    CHSCodelist = open(CHSCodeSource,"rt",encoding="utf16")
    CHSFontlist = []
    for line in CHSCodelist:
        if '==' in line:
            CHSFontlist.append('=')#防止映射为字符“=”被split处理掉
        else:
            s=line.split("=")
            CHSFontlist.append(s[1].strip("\n"))
    bufferList = []
    if bitmaps == '1bppTo':
        for char in CHSFontlist:
            bufferList.extend(MakeFont_1bppTo(char,FONT,fontsize,bpp,reshape,method = method))
    elif bitmaps == "8bppTo":
        for char in CHSFontlist:
            bufferList.extend(MakeFont_8bppTo(char,FONT,fontsize,bpp,reshape))
    else:
        raise TypeError("未指定正确的bpp转换类型。")
    with open(ofilename,'wb') as f:
        for i in bufferList:
            f.write(struct.pack('B',i))

if __name__ == "__main__":
    CHSCodeSource = "CHS.TBL"
    FONT = 'SIMSUN2.TTC'
    bpp = 2
    for num in range(3):
        if num == 0:
            fontsize = 12
            width = fontsize
            height = fontsize + 3
            method = "rightdownShadow"
        elif num == 1:
            fontsize = 10
            width = fontsize
            height = fontsize
            method = "rightdownShadow"
        else:
            fontsize = 10
            width = fontsize + 1
            height = fontsize + 3
            method = "blodShadow"

        num = str(num)
        reshape = (width,height)

        ofilename = 'a023-'+ num + '-chs'
        main(CHSCodeSource,FONT,ofilename,bpp,fontsize = fontsize,reshape = reshape,method = method)

