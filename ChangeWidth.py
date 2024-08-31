import csv
with open('a023-0_CHS_test.TBL',"r",encoding= 'utf-16')as cf:#锁定中文部分的码表字模序
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
    filename = "a023_extr/a023-"+str(num)
    csvfile = filename + 'CWDH.csv'
    ncsvfile = filename + 'CWDH_new.csv'

    twdict = dict()
    transl = []
    with open(csvfile,"r") as r:
        reader = csv.DictReader(r)
        locs = []
        widths = []
        tags = []
        for row in reader:
            locs.append(int(row['loc']))#csv表全都是默认为str字串型
            widths.append(int(row['width']))
            tags.append(int(row['tag']))
        for i in range(len(tags)):
            if tags[i] == 1:
                #print(widths[i])
                transl.append(widths[i])
        transl = list(set(transl))
        transl.sort()
        print(transl)
        nwidth = []
        for i in range(len(locs)):
            if (locs[i] >= first and locs[i] <= last) or  locs[i] == 4932 or locs[i] == 336 or locs[i]== 207\
                   or locs[i] == 208 or locs[i] == 4904 or locs[i] == 4913 :#？！“”，。全角字母
                nwidth.append(transl[1])#选择适中的宽度
            elif(locs[i] >= 4934 and locs[i] <= 4959) or (locs[i] >= 4966 and locs[i] <= 4991):
                nwidth.append(transl[0])#最小可选宽度
            else:
                nwidth.append(widths[i])
    with open(ncsvfile,"w",newline="") as w:
        writer = csv.writer(w)
        writer.writerow(["loc","width","tag"])
        for i in range(len(locs)):
            writer.writerow([locs[i],nwidth[i],tags[i]])

    csvfile = filename + "宽度表.csv"
    ncsvfile = filename + "宽度表_new.csv"
    with open(csvfile,"r",newline="")as r:
        reader = csv.DictReader(r)
        locs = []
        lefts = []
        widths = []
        advances = []
        for row in reader:
            locs.append(int(row['loc']))#csv表全都是默认为str字串型
            lefts.append(int(row['left']))
            widths.append(int(row['width']))
            advances.append(int(row['advance']))
        nwidth = []
        nleft = []
        nadvance = []
        for i in range(len(locs)):
            if (locs[i] >= first and locs[i] <= last):#中文
                if num < 2:
                    nwidth.append(max(widths))
                    nadvance.append(max(advances)-1)
                    nleft.append(0)
                else:
                    nwidth.append(max(widths))
                    nadvance.append(max(advances))
                    nleft.append(0)
            elif locs[i] == 4932 or locs[i] == 336 or locs[i]== 207\
                   or locs[i] == 208 or locs[i] == 4904 or locs[i] == 4913\
                    or locs[i] == 4927 or locs[i] == 4928:#？！“”，。;:
                nwidth.append(max(widths)-3)
                nadvance.append(max(advances)-2)
                nleft.append(2)
            elif (locs[i] >= 4934 and locs[i] <= 4959) or (locs[i] >= 4966 and locs[i] <= 4991):#全角字母
                nwidth.append(widths[i])
                if advances[i] < max(advances):
                    nadvance.append(advances[i]+1)
                else:
                    nadvance.append(advances[i])
                nleft.append(lefts[i])
            else:
                nwidth.append(widths[i])
                nadvance.append(advances[i])
                if lefts[i]-1 > 0:
                    nleft.append(lefts[i]-1)
                else:
                    nleft.append(lefts[i])

    with open(ncsvfile,"w",newline="") as w:
        writer = csv.writer(w)
        writer.writerow(["loc","left","width","advance"])
        for i in range(len(locs)):
            writer.writerow([locs[i],nleft[i],nwidth[i],nadvance[i]])
