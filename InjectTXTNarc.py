import MakeString
import os
#批量将txt导入各分节，并加密
def InjectNarcFiles_byTXT(dirname,encoding = 'utf-16'):
    fileslist = os.listdir(dirname)
    for filename in fileslist:
        if '.txt' in filename or "CMP" in filename:
            continue
        aimname = dirname + '/' + filename
        with open(aimname + '.txt', 'r',encoding=encoding)as txtf:
            raw = txtf.readlines()
            texts = MakeString.maketxtput(raw)#将文本处理为gen5put()可处理的entry列表形式
            print(filename)
            #print(texts)
            inputs = MakeString.gen5put(texts)
        with open(aimname, 'wb')as f:
            f.write(inputs)

if __name__ == "__main__":
    for num in range(2):
        dirname = 'B(CH)' + str(num+2) + '_extr'
        #dirname = 'testdir'
        InjectNarcFiles_byTXT(dirname)
