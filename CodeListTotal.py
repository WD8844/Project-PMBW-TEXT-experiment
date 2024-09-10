#从nftr导出的所有序码表按顺序整合为一个码表
def Total_txt(nftrfilepath,dirpath = "./"):
    if dirpath != "./":
        if dirpath[-1]!="/":
            dirpath += "/"
    llists = []#将所有序码表中的[字模序，字符]读入
    for i in range(8):#每个字库都有8个序码表
        lpath =dirpath + nftrfilepath + '序码表_' + str(i) + '.txt'
        with open(lpath,"r",encoding='utf-16') as lfile:
            raw = lfile.read().split("\n")
        for c in raw:
            if c != "":
                if "==" in c:
                    llists.append([c.split("=")[0],"="])
                elif "NULL" in c:
                    pass
                else:
                    llists.append(c.split("="))
    llists = sorted(llists, key=lambda x: int(x[0]))
    totalpath = nftrfilepath + '_Total.txt'
    with open(totalpath,"w",encoding='utf-16')as w:
        for l in llists:
            s = l[0] + "=" +l[1] + "\n"
            w.write(s)

if __name__ == "__main__":
    nftrfile = 'a023'
    dirpath = 'a023_extr/'
    for i in range(3):
        nftrfilepath = nftrfile + "-" + str(i)
        Total_txt(nftrfilepath,dirpath = dirpath)
#中文部分覆盖在603~3724即：025b~0e8b
