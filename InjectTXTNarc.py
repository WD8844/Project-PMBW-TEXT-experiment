import MakeString
import os
#批量将txt导入各分节，并加密
def InjectNarcFiles_byTXT(dirpath,encoding = 'utf-16'):
    fileslist = os.listdir(dirpath)
    for filepath in fileslist:
        if '.txt' in filepath or "CMP" in filepath:
            continue
        if dirpath[-1]!='/':
            dirpath += '/'
        aimpath = dirpath + filepath
        with open(aimpath + '.txt', 'r',encoding=encoding)as txtf:
            raw = txtf.readlines()
            texts = MakeString.maketxtput(raw)#将文本处理为gen5put()可处理的entry列表形式
            print(filepath)
            #print(texts)
            inputs = MakeString.gen5put(texts)
        with open(aimpath, 'wb')as f:
            f.write(inputs)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("使用方法: python .\InjectTXTNarc.py <拟定的新Narc文件名>")
        exit()
    else:
        dirpath = sys.argv[1]+"_extr/"
        try:
            InjectNarcFiles_byTXT(dirpath)
        except Exception as e:
            print(f"錯誤: {e}，请重新操作。")
            input("按任意键结束...")
