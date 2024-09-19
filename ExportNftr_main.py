from ExtractNftr import *
import os
if __name__ == "__main__":
    try:
        filename = input("请输入预导出Nftr的原Narc文件名：")#（一般命名为a023）
        dirpath = filename + '_extr/'
        if os.path.exists(dirpath):
            num = input("请输入需要导出的Nftr文件总数（例：BW只需要修改前3个字库，输入3）：")#（BW只需要修改前3个字库，输入3）
            if len(os.listdir(dirpath)) > int(num):
                for i in range(int(num)):
                    filepath = dirpath +filename+"-" + str(i)
                    ExtractNftr(filepath)
            else:
                raise LookupError(f"预处理文件数超过{dirpath}内的总文件数")
        else:
            raise FileExistsError(f"{dirpath}不存在，请确认是否已利用ExtractNarc.py从目标Narc中正确提取了Nftr文件")
    except Exception as e:
        print(f"錯誤: {e}，请重新操作。")
        input("按任意键结束...")
