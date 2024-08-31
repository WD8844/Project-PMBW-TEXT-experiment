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
    import sys
    encoding = "utf-16"
    if len(sys.argv) not in [2,3]:
        print("使用方法: ExtractNftr.py <文件目錄> <编码：默认是utf-16>")
        exit()
    elif len(sys.argv)==2:
        dirname = sys.argv[1]
    elif len(sys.argv)==3:
        dirname = sys.argv[1]
        encoding = sys.argv[2]
    try:
            InjectNarcFiles_byTXT(dirname,encoding)
    except FileNotFoundError:
            print(f"未找到名为{filename}的文件，请重新操作。")
