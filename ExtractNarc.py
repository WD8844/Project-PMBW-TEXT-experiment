import os
import narc, MakeString
#解析解包目标Narc

def ExtractNarc(filename,dirname,type = 'text'):
    try:
            os.mkdir(dirname)
            print(dirname+" 已创建！")
    except FileExistsError:
            print("对应文件夹{}已存在。".format(dirname))
            pass
    with open(filename, 'rb')as file:
        rawdata = file.read()
        Narc = narc.NARC(rawdata)
        if type == "text":#对于文本，批量导出并解密其中的所有分节
            n = 0
            for f in Narc.gmif.files:
                tfilename = dirname+'/'+filename+'-'+str(n)
                print(tfilename)
                texts = MakeString.gen5get(f)
                with open(tfilename, 'wb')as nf:
                    nf.write(f)
                with open(tfilename + '.txt','w',encoding='utf16') as w:
                    for line in texts:
                        w.writelines(line)
                n += 1
        else:
            n = 0
            for f in Narc.gmif.files:
                tfilename = dirname+'/'+ filename+'-'+str(n)
                print(tfilename)
                with open(tfilename, 'wb')as nf:
                    nf.write(f)
                n += 1


if __name__ =="__main__":
    import sys
    # 检查是否提供了参数

    if len(sys.argv) != 3:
        print("使用方法: ExtractNarc.py <文件名> <处理类型：输入text或file>")
    else:
        filename = sys.argv[1]
        type = sys.argv[2]
        try:
            dirname = filename+'_extr'
            ExtractNarc(filename,dirname,type = type)
        except FileNotFoundError:
            print(f"未找到名为{filename}的文件，请重新操作。")


