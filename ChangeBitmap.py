with open('a023-0_CHS_test.TBL',"r",encoding= 'utf-16')as cf:#'a023-0_CHS_test.TBL' is the file name of Chinese encodelist
    raws = cf.read().split("\n")
    flag = 0
    for raw in raws:
        trans = raw.split("=")
        if flag == 0 and len(trans[0])==4 and trans[0][0]=="0":
            first = int(trans[0],base=16)
            flag = -1
        elif len(trans[0])>1 and trans[0][0]!="0" and flag == -1:
            flag = 2
            last = int(trans[0])
            break
print(first)
print(last)
for num in range(3):
    filenum = str(num)
    file = "a023-" + filenum
    chsfile = file + "-chs"
    filename = "a023_extr/" + file
    sizedict = {"0":45,"1":25,"2":36}
    size = sizedict[filenum]

    def buffersplit(buffer,size):
        sp = []
        for i in range(0,len(buffer),size):
            sp.append(buffer[i:i+size])
        #print(len(sp))
        return sp

    with open(chsfile,"rb")as f:
        chsbuffer = f.read()
        schsbuffer = buffersplit(chsbuffer,size)
    #print(len(schsbuffer[0]))
    #print(schsbuffer)
    with open(filename + ".bitmap","rb")as f:
        buffer = f.read()
        sbuffer = buffersplit(buffer,size)

    #print(len(buffer))
    #print(len(sbuffer))

    with open(filename + "_new.bitmap","wb")as w:
        for i in range(len(schsbuffer)):
            sbuffer[first + i] = schsbuffer[i]
        w.writelines(sbuffer)
