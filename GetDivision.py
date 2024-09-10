import MakeString
import re,os
#将文本按块分片为不同的txt
#mknewdir为True时，会对应块编号在当前目录创建文件夹，并按文件夹导出分块文本
def txtDivision_byBlock(raw ,filepath ,blocknums = 2 ,encoding = 'utf-16',mknewdir = False ):#输入文本文件readlines表
    texts = MakeString.maketxtput(raw)#处理为按节分的文本
    #print(texts)
    for i in range(blocknums):
        writerlist = []
        if "/" in filepath:#在文本文件面前增加标识数方便排序筛选
            finda = re.findall(r'(.*)/(.*)',filepath)#finda[0][0]是文件目录，finda[0][1]是文件名
            if mknewdir:
                dirpath = finda[0][0] + '/' + str(i)
                try:
                    os.mkdir(dirpath)
                    print(dirpath+" 已创建！")
                except FileExistsError:
                    print("对应文件夹{}已存在。".format(dirpath))
                    pass
                output_filepath = dirpath + "/" +str(i)+"_" + finda[0][1]
            else:
                output_filepath = finda[0][0] + '/' + str(i)+"_" + finda[0][1]
        else:
            if mknewdir:
                dirpath = str(i)
                try:
                    os.mkdir(dirpath)
                    print(dirpath+" 已创建！")
                except FileExistsError:
                    print("对应文件夹{}已存在。".format(dirpath))
                    pass
                output_filepath = dirpath + "/" +str(i)+"_"+filepath
            else:
                output_filepath = str(i)+"_"+filepath
        for text in texts:
            #print(text)
            if text[0][0] == str(i):#每块第一个字符必定是块编号
                writerlist.extend(text)
        textsrteam = "".join(writerlist)
        with open(output_filepath,"w",encoding = encoding)as w:
            w.write(textsrteam)

#fmnewdir为True时，当前文件夹下必须有对应块编号的文件夹
def txtCombine_byBlock(filepath, blocknums = 2,encoding = 'utf-16',fmnewdir = False):#将分开的txt重组为导出时的样子
    #输入文本文件流（直接read()）
    writerlist = []
    for i in range(blocknums):
        if "/" in filepath:#在文本文件面前增加标识数方便排序筛选
            finda = re.findall(r'(.*)/(.*)',filepath)
            if fmnewdir:
                dirpath = finda[0][0] + '/' + str(i)
                print(dirpath)
                input_filepath = dirpath + "/" + str(i)+"_" + finda[0][1]
            else:
                input_filepath = finda[0][0] + '/' + str(i)+"_" + finda[0][1]
        else:
            if fmnewdir:
                dirpath = str(i)
                input_filepath = dirpath+"/"+str(i)+"_"+filepath
            else:
                input_filepath = str(i)+"_"+filepath
        print(input_filepath)
        with open(input_filepath,'r',encoding=encoding)as f:
            writerlist.extend(f.read())
            if f.tell() == 0:
                raise KeyError("文本文件{}是空的！".format(input_filepath))
    textsrteam = "".join(writerlist)
    with open(filepath,'w',encoding=encoding)as w:
        w.write(textsrteam)

if __name__ == "__main__":#This is just for code testing
    #分片
    filepath = './testdir/B2_CMP/CMP_B2-44.txt'
    with open(filepath,encoding='utf-16')as f:
        txtDivision_byBlock(f.readlines(), filepath = filepath,mknewdir = True)
    #重新组合复原
    txtCombine_byBlock(filepath,fmnewdir= True)
