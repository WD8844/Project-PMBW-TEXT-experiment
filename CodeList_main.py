import CodeListCover,CodeListTotal,os
from SetCharCounts import *
if __name__ == "__main__":
    print("注：此脚本仅用于处理Pokemon Black and White（宝可梦黑白）Nftr的3个中文字库的制作，\n仅执行常用中文部分（0x4E00~0x9FFF）的覆盖操作。\n")
    nftrfile = input("请输入Nftr对应的原Narc文件名：")#a023
    dirpath = nftrfile+'_extr/'
    c = input("是否已有完整的原始码表？输入Y为是，N为否：")
    try:
        if os.path.exists(dirpath):
            if c == "Y":
                totalCLpath = input("请输入原始码表的文件路径：")
            elif c == "N":
                    tlist = []
                    for i in range(3):
                        nftrfilepath = nftrfile + "-" + str(i)
                        totalpath = CodeListTotal.Total_txt(nftrfilepath,dirpath = dirpath)
                        tlist.append(totalpath)
                    i = input(f"已在程式脚本同目录下生成3个字库对应的全码表\n{tlist[0]}\n{tlist[1]}\n{tlist[2]}\n这3个码表的内容应当完全相同。"
                              f"\n确认无误后，请任选一个码表作为原始码表（输入0，1，2中的任意一个数字）：")
                    totalCLpath = tlist[int(i)]
            else:
                input("未给出正确指令，请按任意键结束...")
                exit()
            textspath = input("请输入翻译后的文本*.txt所在的文件夹路径：")
            coverL = SetCharCounts(textspath)
            tbl= "CHS.TBL"
            with open(tbl,"w",encoding='utf-16')as w:
                for i in range(len(coverL)):
                    s = str(i) + "=" +coverL[i]+"\n"
                    w.write(s)
            input(f"已在程式脚本同目录下生成了名为{tbl}的中文编码表，专用于制作中文字库。\n确认无误后，请按任意键继续后续操作：")
            nclname = "NewCodeList.txt"
            CodeListCover.Cover_txt(totalCLpath,coverL,newCLpath = nclname)
            input(f"已在程式脚本同目录下生成了名为{nclname}的新码表。\n全操作完毕，请按任意键结束...")
        else:
            raise FileExistsError(f"{dirpath}不存在，请确认是否已利用ExtractNarc.py从目标Narc中正确提取了Nftr文件")
    except Exception as e:
        print(f"錯誤: {e}，请重新操作。")
        input("按任意键结束...")

