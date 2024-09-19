import re,os
import MakeString
#由完整的导出文本来构造对照外文/翻译文本
def CMP(jpfilepath, chfilepath,encoding= 'utf-16',mknewdir = False):#输入文件名
    with open(jpfilepath,"r",encoding = encoding)as jpfile:
        with open(chfilepath,"r",encoding = encoding) as cnfile:
            jp_text = jpfile.readlines()
            ch_text = cnfile.readlines()
            #先处理为分节文本
            jp_entrytexts= MakeString.maketxtput(jp_text)
            ch_entrytexts= MakeString.maketxtput(ch_text)
            cmptexts = []
            for i in range(len(jp_entrytexts)):#jp和cn列表的长度必定相同
                match = re.match("([^_]+)_([0-9]+)(.*)", jp_entrytexts[i][0])
                if match:
                    cmptexts.extend(jp_entrytexts[i][0])
                    for j in range(1,len(jp_entrytexts[i])):
                        cmptexts.extend(jp_entrytexts[i][j])
                    for j in range(1,len(jp_entrytexts[i])):
                        cmptexts.extend(ch_entrytexts[i][j])
                else:
                    raise KeyError("当前文本在第{}节处没有分块标识！".format(i))
    if '/' in jpfilepath:
        finda = re.findall(r'(.*)/(.*)',jpfilepath)#finda[0][0]是文件目录，finda[0][1]是文件名
        version = re.findall(r'(.*)\((.*)',finda[0][1])[0][0]
        num = re.findall(r'(.*)\)(.*)',finda[0][1])[0][1]
        cmppath = "CMP_" + version + num

        if mknewdir:
            dirpath = finda[0][0] + '/'+ version + num[0] + "_CMP/"
            try:
                os.mkdir(dirpath)
                print(dirpath+" 已创建！")
            except FileExistsError:
                print("对应文件夹{}已存在。".format(dirpath))
                pass
            output_filepath = dirpath + cmppath
        else:
            output_filepath = finda[0][0] + '/'+ cmppath
    else:
        version = re.findall(r'(.*)\((.*)',jpfilepath)[0][0]
        num = re.findall(r'(.*)\)(.*)',jpfilepath)[0][1]
        cmppath = "CMP_" + version + num

        if mknewdir:
            dirpath = version + num[0] +"_CMP/"
            try:
                os.mkdir(dirpath)
                print(dirpath+" 已创建！")
            except FileExistsError:
                print("对应文件夹{}已存在。".format(dirpath))
                pass
            output_filepath = dirpath + cmppath
        else:
            output_filepath = cmppath
    print(output_filepath)
    textsrteam = "".join(cmptexts)
    with open(output_filepath,'w',encoding=encoding)as w:
        w.write(textsrteam)
    return output_filepath

#将CMP生成的对照文本留下翻译部分（翻译工作完成后使用）
def KeepTH(cmpfilepath,dirpath=None,encoding = 'utf-16',name = None):
    with open(cmpfilepath,'r',encoding=encoding)as cmpfile:
        cmptexts = cmpfile.readlines()
        cmp_entrytexts = MakeString.maketxtput(cmptexts)
        writetexts = []
        subline = '\n------------------------------\n'
        for i in range(len(cmp_entrytexts)):
            match = re.match("([^_]+)_([0-9]+)(.*)", cmp_entrytexts[i][0])
            if match:
                writetexts.extend(cmp_entrytexts[i][0])
                for j in range(1,len(cmp_entrytexts[i])):#锁定并计入翻译部分，分节最后的一定是翻译部分
                    sp = cmp_entrytexts[i][j].split(subline)
                    writetexts.extend(sp[1]+subline)
            else:
                raise KeyError("当前文本在第{}节处没有分块标识！".format(i))
        if '/' in cmpfilepath:
                finda = re.findall(r'(.*)/(.*)',cmpfilepath)
                comb = re.findall(r'(.*)_(.*)',finda[0][1])
                version = comb[0][1][0]
                num = comb[0][1][1:]
        else:
                comb = re.findall(r'(.*)_(.*)',cmpfilepath)
                version = comb[0][1][0]
                num = comb[0][1][1:]
        if dirpath:
            if dirpath[-1]!="/":
                dirpath = dirpath+"/"
        else:
            if '/' in cmpfilepath:
                dirpath = finda[0][0] + '/' + version + num[0] +"_TH/"
            else:
                dirpath = version + num[0] +"_TH/"
            try:
                os.mkdir(dirpath)
                print(dirpath+" 已创建！")
            except FileExistsError:
                print("对应文件夹{}已存在。".format(dirpath))
                pass
        if name:
            output_filepath = dirpath + name + num[1:]
        else:
            output_filepath = dirpath + version + num
        print(output_filepath)
        textsrteam = "".join(writetexts)
        with open(output_filepath,'w',encoding=encoding)as w:
            w.write(textsrteam)
        with open(output_filepath.replace(".txt",""),'w',encoding=encoding):
            pass#For InjectTXTNarc
    return dirpath

if __name__ == "__main__":#This is just for code testing
    jpfilepath = './testdir/B(JP)2-44.txt'
    chfilepath = './testdir/B(CH)2-44.txt'
    cmpfilepath = CMP(jpfilepath,chfilepath,mknewdir=True)
    KeepTH(cmpfilepath)
