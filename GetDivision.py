import MakeString
import re,os
#将文本按块分片为不同的txt
#mknewdir为True时，会对应块编号在当前目录创建文件夹，并按文件夹导出分块文本
def txtDivision_byBlock(raw ,filename ,blocknums = 2 ,encoding = 'utf-16',mknewdir = False ):#输入文本文件readlines表
    texts = MakeString.maketxtput(raw)#处理为按节分的文本
    #print(texts)
    for i in range(blocknums):
        writerlist = []
        if "/" in filename:#在文本文件面前增加标识数方便排序筛选
            finda = re.findall(r'(.*)/(.*)',filename)#finda[0][0]是文件目录，finda[0][1]是文件名
            if mknewdir:
                dirname = finda[0][0] + '/' + str(i)
                try:
                    os.mkdir(dirname)
                    print(dirname+" 已创建！")
                except FileExistsError:
                    print("对应文件夹{}已存在。".format(dirname))
                    pass
                output_filename = dirname + "/" +str(i)+"_" + finda[0][1]
            else:
                output_filename = finda[0][0] + '/' + str(i)+"_" + finda[0][1]
        else:
            if mknewdir:
                dirname = str(i)
                try:
                    os.mkdir(dirname)
                    print(dirname+" 已创建！")
                except FileExistsError:
                    print("对应文件夹{}已存在。".format(dirname))
                    pass
                output_filename = dirname + "/" +str(i)+"_"+filename
            else:
                output_filename = str(i)+"_"+filename
        for text in texts:
            #print(text)
            if text[0][0] == str(i):#每块第一个字符必定是块编号
                writerlist.extend(text)
        textsrteam = "".join(writerlist)
        with open(output_filename,"w",encoding = encoding)as w:
            w.write(textsrteam)

#fmnewdir为True时，当前文件夹下必须有对应块编号的文件夹
def txtCombine_byBlock(filename, blocknums = 2,encoding = 'utf-16',fmnewdir = False):#将分开的txt重组为导出时的样子
    #输入文本文件流（直接read()）
    writerlist = []
    for i in range(blocknums):
        if "/" in filename:#在文本文件面前增加标识数方便排序筛选
            finda = re.findall(r'(.*)/(.*)',filename)
            if fmnewdir:
                dirname = finda[0][0] + '/' + str(i)
                print(dirname)
                input_filename = dirname + "/" + str(i)+"_" + finda[0][1]
            else:
                input_filename = finda[0][0] + '/' + str(i)+"_" + finda[0][1]
        else:
            if fmnewdir:
                dirname = str(i)
                input_filename = dirname+"/"+str(i)+"_"+filename
            else:
                input_filename = str(i)+"_"+filename
        print(input_filename)
        with open(input_filename,'r',encoding=encoding)as f:
            writerlist.extend(f.read())
            if f.tell() == 0:
                raise KeyError("文本文件{}是空的！".format(input_filename))
    textsrteam = "".join(writerlist)
    with open(filename,'w',encoding=encoding)as w:
        w.write(textsrteam)

if __name__ == "__main__":
    #分片
    filename = './testdir/B2_CMP/CMP_B2-44.txt'
    with open(filename,encoding='utf-16')as f:
        txtDivision_byBlock(f.readlines(), filename = filename,mknewdir = True)
    #重新组合复原
    txtCombine_byBlock(filename,fmnewdir= True)
