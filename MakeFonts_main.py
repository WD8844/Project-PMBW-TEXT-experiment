from MakeFonts import main_CHS
def MakeFonts_BW_CHS(CHSCodeSource,FONT,narcfilename,bpp=2):
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
        ofilepath = narcfilename+'-'+ num + '-chs'
        main_CHS(CHSCodeSource,FONT,ofilepath,bpp,fontsize = fontsize,reshape = reshape,method = method)
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("使用方法: .\MakeFonts_main.py <码表> <字形文件（*.ttf|*.ttc）> <Nftr对应的原Narc名>")
        exit()
    else:
        CHSCodeSource = sys.argv[1]
        FONT = sys.argv[2]
        narcfilename = sys.argv[3]
        MakeFonts_BW_CHS(CHSCodeSource,FONT,narcfilename)
