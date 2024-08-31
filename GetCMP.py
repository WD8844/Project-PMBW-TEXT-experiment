import re,os
import MakeString
#由完整的导出文本来构造对照外文/翻译文本
def CMP(jpfilename, chfilename,encoding= 'utf-16',mknewdir = False):#输入文件名
    with open(jpfilename,"r",encoding = encoding)as jpfile:
        with open(chfilename,"r",encoding = encoding) as cnfile:
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
    if '/' in jpfilename:
        finda = re.findall(r'(.*)/(.*)',jpfilename)#finda[0][0]是文件目录，finda[0][1]是文件名
        version = re.findall(r'(.*)\((.*)',finda[0][1])[0][0]
        num = re.findall(r'(.*)\)(.*)',finda[0][1])[0][1]
        cmpname = "CMP_" + version + num

        if mknewdir:
            dirname = finda[0][0] + '/'+ version + num[0] + "_CMP/"
            try:
                os.mkdir(dirname)
                print(dirname+" 已创建！")
            except FileExistsError:
                print("对应文件夹{}已存在。".format(dirname))
                pass
            output_filename = dirname + cmpname
        else:
            output_filename = finda[0][0] + '/'+ cmpname
    else:
        version = re.findall(r'(.*)\((.*)',jpfilename)[0][0]
        num = re.findall(r'(.*)\)(.*)',jpfilename)[0][1]
        cmpname = "CMP_" + version + num

        if mknewdir:
            dirname = version + num[0] +"_CMP/"
            try:
                os.mkdir(dirname)
                print(dirname+" 已创建！")
            except FileExistsError:
                print("对应文件夹{}已存在。".format(dirname))
                pass
            output_filename = dirname + cmpname
        else:
            output_filename = cmpname
    print(output_filename)
    textsrteam = "".join(cmptexts)
    with open(output_filename,'w',encoding=encoding)as w:
        w.write(textsrteam)
    return output_filename

#将CMP生成的对照文本留下翻译部分（翻译工作完成后使用）
def KeepTH(cmpfilename,encoding = 'utf-16',mknewdir = False):
    with open(cmpfilename,'r',encoding=encoding)as cmpfile:
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

        if '/' in cmpfilename:
            finda = re.findall(r'(.*)/(.*)',cmpfilename)
            comb = re.findall(r'(.*)_(.*)',finda[0][1])
            version = comb[0][1][0]
            num = comb[0][1][1:]
            transname = version +"(CH)"+ num
            if mknewdir:
                dirname = finda[0][0] + '/' + version + num[0] +"_TH/"
                try:
                    os.mkdir(dirname)
                    print(dirname+" 已创建！")
                except FileExistsError:
                    print("对应文件夹{}已存在。".format(dirname))
                    pass
                output_filename = dirname + transname
            else:
                output_filename = finda[0][0] + '/' + transname
        else:
            comb = re.findall(r'(.*)_(.*)',cmpfilename)
            version = comb[0][1][0]
            num = comb[0][1][1:]
            if mknewdir:
                dirname = version + num[0] +"_TH/"
                try:
                    os.mkdir(dirname)
                    print(dirname+" 已创建！")
                except FileExistsError:
                    print("对应文件夹{}已存在。".format(dirname))
                    pass
                output_filename = dirname + version +"(CH)"+ num
            else:
                output_filename= version +"(CH)"+ num
        print(output_filename)
        textsrteam = "".join(writetexts)
        with open(output_filename,'w',encoding=encoding)as w:
            w.write(textsrteam)

if __name__ == "__main__":#This is just for code testing
    jpfilename = './testdir/B(JP)2-44.txt'
    chfilename = './testdir/B(CH)2-44.txt'
    cmpfilename = CMP(jpfilename,chfilename,mknewdir=True)
    KeepTH(cmpfilename,mknewdir=True)
