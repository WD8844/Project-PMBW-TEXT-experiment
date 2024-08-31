import GetCMP, GetDivision
import os,re

#批量构造CMP整体对比文本
def MakeCMP(jpdirname,chdirname,encoding = 'utf-16',mknewdir = False):
    jpfileslist = os.listdir(jpdirname)
    chfileslist = os.listdir(chdirname)
    jptxtfilelist = []
    chtxtfilelist = []
    for filename in jpfileslist:
        if '.txt' in filename:
            jptxtfilelist.append(filename)
    for filename in chfileslist:
        if '.txt' in filename:
            chtxtfilelist.append(filename)
    jp_ch_dict = {jptxtfilelist[i]:chtxtfilelist[i] for i in range(len(jptxtfilelist))}#方便批量构造CMP
    for jpfilename in jp_ch_dict:
        chfilename = chdirname + "/"+ jp_ch_dict[jpfilename]
        jpfilename = jpdirname + "/" + jpfilename
        cmpfilename = GetCMP.CMP(jpfilename,chfilename,encoding=encoding,mknewdir=mknewdir)
    finda = re.findall(r'(.*)/(.*)',cmpfilename)
    CMP_path = finda[0][0]
    return CMP_path

#批量分片经由CPM处理过后的整体文本
def DivCMP(CMPdirpath,blocknums = 2,encoding = 'utf-16',mknewdir = False):
    if CMPdirpath[-1]!="/":#补充路径尾部缺失的/方便后续拼接操作
        CMPdirpath += "/"
    filelist = os.listdir(CMPdirpath)
    CMPlist = []
    for filename in filelist:
        if ".txt" in filename:
            if "CMP" in filename:
                try:
                    int(filename[0])
                except ValueError:#按命名规则，必须开头是CMP的才是可分片的整体文本
                    CMPlist.append(filename)
    for CMPname in CMPlist:
        CMPname = CMPdirpath + CMPname
        with open(CMPname,"r",encoding='utf-16')as f:
            GetDivision.txtDivision_byBlock(f.readlines(), CMPname, blocknums = blocknums,
                                            encoding=encoding,mknewdir = mknewdir)

#批量将分块文本重新组合复原
def Div_Restore(CMPdirpath,blocknums = 2,encoding = 'utf-16',fmnewdir = False):
    if CMPdirpath[-1]!="/":#补充路径尾部缺失的/方便后续拼接操作
        CMPdirpath += "/"
    filelist = os.listdir(CMPdirpath)
    CMPlist = []
    for filename in filelist:
        if ".txt" in filename:
            if "CMP" in filename:
                try:
                    int(filename[0])
                except ValueError:#按命名规则，必须开头是CMP的才是可分片的整体文本
                    CMPlist.append(filename)
    for CMPname in CMPlist:
        CMPname = CMPdirpath + CMPname
        GetDivision.txtCombine_byBlock(CMPname,blocknums = blocknums,encoding = encoding,fmnewdir = fmnewdir)

#批量将CMP文本只保留翻译部分
def MakeCMP_TH(CMPdirpath,encoding = 'utf-16',mknewdir = False):
    if CMPdirpath[-1]!="/":#补充路径尾部缺失的/方便后续拼接操作
        CMPdirpath += "/"
    filelist = os.listdir(CMPdirpath)
    CMPlist = []
    for filename in filelist:
        if ".txt" in filename:
            if "CMP" in filename:
                try:
                    int(filename[0])
                except ValueError:#按命名规则，必须开头是CMP的才是可分片的整体文本
                    CMPlist.append(filename)
    for CMPname in CMPlist:
        CMPname = CMPdirpath + CMPname
        GetCMP.KeepTH(CMPname,encoding = encoding,mknewdir = mknewdir)

if __name__ == "__main__":#This is just for code testing
    for i in range(2,4):
        num = str(i)
        nstr = num + '_extr'
        jpdir = 'B(JP)'
        chdir = 'B(CH)'
        jpdirname = jpdir + nstr
        chdirname = chdir + nstr
        blocknums = 2
        encoding = 'utf-16'
        CMPdirpath = MakeCMP(jpdirname,chdirname,encoding = encoding,mknewdir = True)
        DivCMP(CMPdirpath,blocknums = blocknums,encoding = encoding,mknewdir = True)
        Div_Restore(CMPdirpath,blocknums = blocknums,encoding = encoding,fmnewdir = True)
        MakeCMP_TH(CMPdirpath,encoding = encoding,mknewdir = True)
