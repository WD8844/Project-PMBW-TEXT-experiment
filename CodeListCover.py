def Cover_txt(totalCLpath,coverL,newCLpath = "NewCodeList.txt"):
    with open(totalCLpath,"r",encoding='utf-16')as total:
        totalraws = total.read().split("\n")
    totalL = []
    for i in range(len(totalraws)):#已经做好的全码表
        if totalraws[i]!="":
            trans = totalraws[i].split("=")
            #print(trans)
            if "==" in totalraws[i]:
                totalL.append([trans[0],"="])
            else:
                totalL.append([trans[0],trans[1]])
    pos = -1
    for i in range(len(totalL)):
        if pos == -1:
            if totalL[i][1] == coverL[0]:#锁定中文开头
                if len(totalL)-i < len(coverL):
                    raise LookupError(f"超过可覆盖范围！原始码表可覆盖长度为{len(totalL)-i}，实际所需覆盖长度为{len(coverL)}")
                else:
                    pos += 2
                    print(f"预替换的第1个字符为编号{i}的{totalL[i]}，开始替换。")
        elif (pos > 0) and (pos < len(coverL)):
            totalL[i][1] = coverL[pos]
            print(f"已替换编号为{totalL[i][0]}的字符为{coverL[pos]}")
            pos += 1
        else:
            continue
    with open(newCLpath,"w",encoding='utf-16')as w:
        for l in totalL:
            s = l[0] + "=" +l[1] + "\n"
            w.write(s)

if __name__ == "__main__":#Just for the code test.
    from SetCharCounts import *
    totalCLpath = "a023-0_Total.txt"
    coverL = SetCharCounts("./Counts")
    Cover_txt(totalCLpath,coverL,newCLpath = "NewCodeList.txt")
