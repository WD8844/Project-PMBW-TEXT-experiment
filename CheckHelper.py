import re,os,MakeString
from SetCharCounts import *
def controlChecker():
    for num in range(2, 4):
        num = str(num)
        dirpath = "B(JP)"+num+"_extr/B"+num+"_CMP/"

        def chscounts(trans):
            pos = 0
            for c in trans:
                if (ord(c) >= 0x4E00) and (ord(c) <= 0x9FFF):
                    pos += 1
            return pos

        for n in range(2):#0,1
            filelist = os.listdir(dirpath+str(n)+"/")
            for filepath in filelist:
                path = dirpath+str(n)+"/"+filepath
                with open(path,'r',encoding="utf-16")as cmpfile:
                    cmptexts = cmpfile.readlines()
                    cmp_entrytexts = MakeString.maketxtput(cmptexts)
                    subline = '\n------------------------------\n'
                    for i in range(len(cmp_entrytexts)):
                        match = re.match("([^_]+)_([0-9]+)(.*)", cmp_entrytexts[i][0])
                        if match:
                            for j in range(1,len(cmp_entrytexts[i])):#锁定并计入翻译部分，分节最后的一定是翻译部分
                                sp = cmp_entrytexts[i][j].split(subline)
                                trans = sp[1].split("\n")
                                if len(trans) >= 2:
                                    flag = 0#上一行的末尾标记
                                    pos = 0#上一个控制符后经过的行数
                                    for k in range(len(trans)):

                                        if trans[k] == "":
                                            continue
                                        elif chscounts(trans[k]) > 17:
                                                print(f"在{filepath}的：\n{trans[k]}")
                                                print("疑似发现行过长")
                                                txt = "".join(sp[1])
                                                print(txt)
                                        else:
                                            if flag == 0:
                                                if pos < 2:
                                                    if "<PAGE>" in trans[k]:
                                                        flag = 1
                                                        pos = 0
                                                    elif "<F>" in trans[k]:
                                                        flag = 2
                                                        pos = 0
                                                    else:# 是换行符\n
                                                        flag = 3
                                                else:
                                                    print(f"在{filepath}的：\n{trans[k]}")
                                                    print("疑似发现控制符错误：超过3行没有控制符")
                                                    txt = "".join(sp[1])
                                                    print(txt)
                                                    break
                                            elif flag == 1:#说明上一行末尾是<PAGE>
                                                if pos == 0:
                                                    if "<F>" in trans[k]:
                                                        print(f"在{filepath}的：\n{trans[k]}")
                                                        print("疑似发现控制符错误：<PAGE>后紧随<F>")
                                                        txt = "".join(sp[1])
                                                        print(txt)
                                                        break
                                                    else:
                                                        pos += 1
                                                        flag = 0
                                                elif pos == 1:#<PAGE>后的第二行
                                                    if trans[k-1]!="":#第一行是\n可以多一行
                                                        if "<" not in trans[k]:
                                                            print(f"在{filepath}的：\n{trans[k]}")
                                                            print("疑似发现控制符错误：<PAGE>后两行没有控制符")
                                                            txt = "".join(sp[1])
                                                            print(txt)
                                                            break
                                                        else:
                                                            if "<PAGE>" in trans[k]:
                                                                flag =1
                                                            elif "<F>" in trans[k]:
                                                                flag =2
                                                            pos = 0
                                                    else:
                                                        continue
                                                else:
                                                    print("<PAGE>逻辑，是否存在逻辑错误？")
                                            elif flag == 2:#说明上一行末尾是<F>
                                                if pos == 0:
                                                    if trans[k-1] != "":#第一行是\n可以多一行
                                                        if "<" not in trans[k]:
                                                            if trans[k+1:]:#<F>后最多只能有一句结尾句，能往下说明不是结尾句
                                                                #print(f"pos {pos},flag {flag}")
                                                                print(f"在{filepath}的：\n{trans[k]}")
                                                                print("疑似发现控制符错误：<F>后缺少控制符")
                                                                txt = "".join(sp[1])
                                                                print(txt)
                                                                break

                                                        else:#除了结尾句，<F>后一行末尾不是<F>就是<PAGE>
                                                            if "<PAGE>" in trans[k]:
                                                                flag =1
                                                            elif "<F>" in trans[k]:
                                                                flag =2
                                                            pos = 0
                                                    else:
                                                        continue
                                                else:
                                                    print("<F>逻辑，是否存在逻辑错误？")
                                            else:
                                                if trans[k] != "":
                                                    if pos > 1:
                                                        print(f"在{filepath}的：\n{trans[k]}")
                                                        print("疑似发现控制符错误：超过2行换行后没有控制符")
                                                        txt = "".join(sp[1])
                                                        print(txt)
                                                        break
def charCodeChecker(dirpath):
    def get_simplified_chinese_chars_mapping():
        # 使用 GBK 编码构建简体中文字符的 Unicode 映射
        simplified_chinese_chars = set()
        for code in range(0x4E00, 0x9FA5 + 1):  # 常用汉字范围
            try:
                char = chr(code)
                # 尝试将字符编码为 GBK，成功则为简体中文字符
                char.encode('gbk')
                simplified_chinese_chars.add(char)
            except UnicodeEncodeError:
                continue  # 不是简体中文字符

        return simplified_chinese_chars
    simplified_chinese_chars = get_simplified_chinese_chars_mapping()
    charl = SetCharCounts(dirpath)
    for char in charl:
        if char not in simplified_chinese_chars:
            print(char)

if __name__ == "__main__":
    controlChecker()
    #charCodeChecker(['./B(CH)2_extr','./B(CH)3_extr'])



