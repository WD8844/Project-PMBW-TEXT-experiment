from MakeCMP_Div import *
def main(jpdir,chdir,nstr,opath = None,method = None,path = None,blocknums = 2,encoding = 'utf-16',newdir = True,name = None):
    jpdirpath = jpdir + nstr
    chdirpath = chdir + nstr
    if method == "CMP":
        CMPdirpath = MakeCMP(jpdirpath,chdirpath,encoding = encoding,mknewdir = newdir)
        DivCMP(CMPdirpath,blocknums = blocknums,encoding = encoding,mknewdir = newdir)
    elif method == "Restore":
        CMPdirpath = path
        Div_Restore(CMPdirpath,blocknums = blocknums,encoding = encoding,fmnewdir = newdir)
        path = MakeCMP_TH(CMPdirpath,dirpath = opath,encoding = encoding,name = name)
        return path

if __name__ == "__main__":
    import os
    print("注：此脚本仅用于处理Pokemon Black and White（宝可梦黑白）的文本。\n")
    try:
        jpdir = input("※由命名规则，源Narc文件名应当是：版本(语言)编号，例如B(JP)2\n请输入当前目录下已利用ExtractNarc.py导出的文本对应的源Narc文件名：")
        nstr = '_extr'
        ft = jpdir[0] + jpdir[-1] + "_CMP"
        CMPdirpath = jpdir + nstr+"/" + ft
        c = input("\n※分片制造对照文本请输入：CMP\n※由已经制造的对照文本合并复原请输入：Restore\n请选择操作：")
        if os.path.exists(jpdir+nstr):
            if c == "CMP":
                main(jpdir,jpdir,nstr,method = "CMP",path = None,blocknums = 2,encoding = 'utf-16',newdir = True)
                print(f"已完成对比文本的制造，在{CMPdirpath}内各分块文件夹下。\n※请无视{CMPdirpath}下的txt文本，这些文本是没有分块的对照文本，属于程式处理的中间产物，请不要动它。※\n如欲做文本翻译，请对同级目录分块文件夹下的txt做后续处理。")
                input("按任意键结束...")
            elif c == "Restore":
                chdir = input("\n※由命名规则，建议是：版本(语言)编号，例如B(CH)2\n请输入拟定创造的新Narc文件名：")
                opath = chdir+nstr
                if os.path.exists(opath):
                    print(f"{opath}已存在。")
                else:
                    os.mkdir(opath)
                newpath = main(jpdir,chdir,nstr,opath=opath,method = "Restore",path = CMPdirpath,blocknums = 2,encoding = 'utf-16',newdir = True,name=chdir)
                print(f"已对{CMPdirpath}下的所有翻译文本完成格式还原。\n还原格式后的新文本在{newpath}文件夹下。\n请用InjectTXTNarc.py做后续处理。")
                input("按任意键结束...")
            else:
                c = input("未指定正确操作类型，请按任意键结束。")
                exit()
        else:
                raise FileExistsError(f"{jpdir+nstr}不存在，请确认是否已利用ExtractNarc.py正确导出了文本。")
    except Exception as e:
        print(f"錯誤: {e}，请重新操作。")
        input("按任意键结束...")
    '''#Just for the code test.
    for num in range(2):
        nstr = str(num+2) + '_extr'
        jpdir = 'B(JP)'
        chdir = 'B(CH)'
        #divide
        #main(jpdir,chdir,nstr,method = "CMP",path = None,blocknums = 2,encoding = 'utf-16',newdir = True)
        #combine
        ft = jpdir[0] + nstr[0] + "_CMP"
        CMPdirpath = jpdir + nstr+"/" + ft
        main(jpdir,chdir,nstr,method = "Restore",path = CMPdirpath,blocknums = 2,encoding = 'utf-16',newdir = True)'''
