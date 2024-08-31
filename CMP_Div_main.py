from MakeCMP_Div import *
def main(jpdir,chdir,nstr,method = None,path = None,blocknums = 2,encoding = 'utf-16',newdir = True):
    jpdirname = jpdir + nstr
    chdirname = chdir + nstr
    if method == "CMP":
        CMPdirpath = MakeCMP(jpdirname,chdirname,encoding = encoding,mknewdir = newdir)
        DivCMP(CMPdirpath,blocknums = blocknums,encoding = encoding,mknewdir = newdir)
    elif method == "Restore":
        CMPdirpath = path
        Div_Restore(CMPdirpath,blocknums = blocknums,encoding = encoding,fmnewdir = newdir)
        MakeCMP_TH(CMPdirpath,encoding = encoding,mknewdir = newdir)

if __name__ == "__main__":
    for num in range(2):
        nstr = str(num+2) + '_extr'
        jpdir = 'B(JP)'
        chdir = 'B(CH)'
        #分
        #main(jpdir,chdir,nstr,method = "CMP",path = None,blocknums = 2,encoding = 'utf-16',newdir = True)
        #合
        ft = jpdir[0] + nstr[0] + "_CMP"
        CMPdirpath = jpdir + nstr+"/" + ft
        main(jpdir,chdir,nstr,method = "Restore",path = CMPdirpath,blocknums = 2,encoding = 'utf-16',newdir = True)
