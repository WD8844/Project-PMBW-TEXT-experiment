from ChangeCodeList import *
from ChangeWidth import *
from ChangeBitmap import *
import os
if __name__ == "__main__":
    try:
        filename = input("请输入已经导出的Nftr的原Narc文件名：")#（一般命名为a023）
        dirpath = filename + '_extr/'
        if os.path.exists(dirpath):
            NCpath = input("请输入码表路径：")
            ChangeCodeList(NCpath,filename)
            ChangeWidth(NCpath,filename)
            ChangeBitmap(NCpath,filename)
        else:
            raise FileExistsError(f"{dirpath}不存在，请确认是否已利用ExtractNarc.py从目标Narc中正确提取了Nftr文件")
    except Exception as e:
        print(f"錯誤: {e}，请重新操作。")
