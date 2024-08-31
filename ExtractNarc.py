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
import sys

def main():
    # 检查是否提供了参数
    
    if len(sys.argv) != 2:
        print("使用方法: ExtractNarc.py <文件名>")
        return
    
    filename = sys.argv[1]
    
    # 在这里对文件进行操作
    try:
        dirname = filename+'_extr'
        ExtractNarc(filename,dirname,type = 'text')
    except FileNotFoundError:
        print(f"File {filename} not found.")

if __name__ =="__main__":
    main()

