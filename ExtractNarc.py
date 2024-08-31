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
    #导出文本
    for num in range(2):
        filename = 'B(JP)' + str(num+2)
        dirname = filename+'_extr'
        ExtractNarc(filename,dirname,type = 'text')

    '''#尝试其他Narc
    filename = 'a023'#字库
    dirname = filename+'_extr'
    ExtractNarc(filename,dirname,type = '')'''

