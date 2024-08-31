import narc
import re
import os
import struct
#Narc文件打包

def MakeNarc(aimfile, dirname):
    #构造按名称数字排序的文件名列表
    dirlist = os.listdir(dirname)
    namelist = []
    foward = dirlist[0].split('-')[0] + '-'
    for filename in dirlist:
        if '.' in filename:#文件夹内需要打包的文件没有后缀，因此需保证所有没有后缀的文件是打包文件
            continue
        namelist.append(filename.split('-')[1])
    namelist.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))#按数字大小从小到大排序
    for i in range(len(namelist)):
        namelist[i] = foward + namelist[i]
    
    rawdata = []
    offset = 0
    NewNarc = narc.NARC(rawdata)
    for filename in namelist:
        aimfilename = dirname + '/' + filename
        with open(aimfilename, 'rb')as rawfile:
            raw = rawfile.read()
        #print(filename)
        #print(len(raw))
        table = struct.pack('II', offset, offset+len(raw))
        NewNarc.btaf.table.append(table)
        rawdata.append(raw)
        offset += len(raw)
    
    #完善btaf信息
    NewNarc.btaf.header[0] = NewNarc.btaf.header[0] + len(NewNarc.btaf.table)*8 #header长度+btaf大小即偏移地址表总大小
    NewNarc.btaf.header[1] = len(rawdata)#文件数据分节数
    
    #完善gmif信息
    #NewNarc.gmif.size = NewNarc.gmif.size + offset#header长度+文件数据集总长度？？？
    # 虽然narc中的toString写入逻辑会按照gmif长度重新给gmif.size赋值，但为了正确计算narc的header，必须在此处给出gmif.size？？？
    NewNarc.gmif.files = rawdata
    
    #完善narc信息
    NewNarc.header[1] = 16 + NewNarc.btaf.header[0] + NewNarc.btnf.header[0] + len(NewNarc.gmif.toString())#gmif可能存在填充，因此只有写入长度算数
    
    with open('New_'+ aimfile, 'wb')as f:
        NewNarc.toFile(f)

if __name__ == "__main__":
    for num in range(2):
        aimfile = 'B(CH)'+ str(num+2)#文本
        dirname = aimfile + '_extr'
        MakeNarc(aimfile, dirname)

    '''aimfile = 'a023'#字库
    dirname = aimfile + '_extr'
    MakeNarc(aimfile, dirname)'''
