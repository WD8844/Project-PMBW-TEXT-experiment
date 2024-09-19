import os
import narc, MakeString
#解析解包目标Narc

def ExtractNarc(filepath,dirpath,type = 'text'):
    try:
            os.mkdir(dirpath)
            print(dirpath+" 已创建！")
    except FileExistsError:
            print("对应文件夹{}已存在。".format(dirpath))
            pass
    with open(filepath, 'rb')as file:
        rawdata = file.read()
        Narc = narc.NARC(rawdata)
        if type == "text":#对于文本，批量导出并解密其中的所有分节
            n = 0
            for f in Narc.gmif.files:
                tfilepath = dirpath+'/'+filepath+'-'+str(n)
                print(tfilepath)
                texts = MakeString.gen5get(f)
                with open(tfilepath, 'wb')as nf:
                    nf.write(f)
                with open(tfilepath + '.txt','w',encoding='utf16') as w:
                    for line in texts:
                        w.writelines(line)
                n += 1
        else:
            n = 0
            for f in Narc.gmif.files:
                tfilepath = dirpath+'/'+ filepath+'-'+str(n)
                print(tfilepath)
                with open(tfilepath, 'wb')as nf:
                    nf.write(f)
                n += 1


if __name__ =="__main__":
    import sys
    # 检查是否提供了参数

    if len(sys.argv) != 3:
        print("使用方法: python .\ExtractNarc.py <Narc文件路径> <处理类型：输入text或file>")
    else:
        filepath = sys.argv[1]
        type = sys.argv[2]
        try:
            dirpath = filepath+'_extr'
            ExtractNarc(filepath,dirpath,type = type)
        except FileNotFoundError:
            print(f"未找到路径为{filepath}的文件，请重新操作。")
            input("按任意键结束...")

