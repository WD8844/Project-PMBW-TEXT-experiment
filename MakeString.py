import struct, re
from binary16 import binaryreader, binarywriter

# 单块文本解密和加密
subline = '\n------------------------------\n'


def gen5get(f, fillflag = False):
    texts = []
    reader = binaryreader(f)
    # 前12Byte，文件头header的结构[2Byte总分块数,2Byte分节数,4Byte最大块大小,4Byte的0填充]
    numblocks = reader.read16()  # 头第1个2Byte是文本总的版块数
    numentries = reader.read16()  # 第2个2Byte是各版块总的分节数，每个版块各numentries节
    filesize = reader.read32()  # 4Byte表示最大分块的大小
    zero = reader.read32()  # 4Byte的0，无用
    blockoffsets = []

    #print("filesize:",filesize)
    # header后紧跟：各分块地址offset
    for i in range(numblocks):
        blockoffsets.append(reader.read32())  # 每4Byte表示各分块偏移地址（是相对块头部的偏移地址）
    # filesize == len(f)-reader.pos()
    for i in range(numblocks):  # 按分块地址找到块进行操作
        reader.seek(blockoffsets[i])  # 按块，指针移动到分块地址处
        size = reader.read32()  # 分块头部4Byte是当前分块的大小
        tableoffsets = []
        charcounts = []
        textflags = []
        # 分块大小后是当前分块的分节信息排列
        for j in range(numentries):  # 每个分节信息共8Byte
            tableoffsets.append(reader.read32())  # 4Byte表示分节地址
            charcounts.append(reader.read16())  # 2Byte表示对应分节的字数
            textflags.append(reader.read16())  # 2Byte表示对应分节的标识值
            # 分节信息后就是当前各段文本排列
        for j in range(numentries):  # 按分节读取文本
            compressed = False
            encchars = []
            text = ""
            reader.seek(blockoffsets[i] + tableoffsets[j])  # 文件指针定位到当前块的当前节文本段
            # print(charcounts[j])
            for k in range(charcounts[j]):  # 按当前节文本的字数逐字读取
                encchars.append(reader.read16())  # 每个字2Byte
            key = encchars[len(encchars) - 1] ^ 0xFFFF  # 当前分节的最后一个字的码数与0xFFFF的异或，就是当前文本段的初始key
            decchars = []
            # print("enchars:",len(encchars))
            while encchars:  # 逐字解密
                char = encchars.pop() ^ key  # 从最后一个字倒序逐字解密：加密的字码与key异或得到解密后的字码
                key = ((key >> 3) | (key << 13)) & 0xFFFF  # 上一个字的key右移3位同上一个字的key左移13位的或，再同0xFFFF的与，得到下一个字的key
                decchars.insert(0, char)  # 解密后的字符顺序加入dechars表内
            # print("dechars:",len(decchars))
            if decchars[0] == 0xF100:  # 判断是否被压缩
                print("存在压缩。")
                compressed = True  # 文段开头第一个值是0xF100就说明被压缩，压缩标记compressed赋为True
                decchars.pop(0)  # 去掉文段开头的压缩标记
                newstring = []
                container = 0
                bit = 0
                # 进行解压操作
                while decchars:
                    container |= decchars.pop(0) << bit
                    bit += 16
                    while bit >= 9:
                        bit -= 9
                        c = container & 0x1FF
                        if c == 0x1FF:
                            newstring.append(0xFFFF)
                        else:
                            newstring.append(c)
                        container >>= 9
                decchars = newstring

            if fillflag:#调试时使用
                # 块填充检测
                if j != numentries - 1:
                    if tableoffsets[j + 1] - tableoffsets[j] != 2 * charcounts[j]:
                        print('疑似存在填充，位置：', (blockoffsets[i] + tableoffsets[j]) + 2 * charcounts[j])
                        print("填充长度为：", tableoffsets[j + 1] - tableoffsets[j] - 2 * charcounts[j])
                        print("填充内容为：", f[tableoffsets[j] + 2 * charcounts[j]:tableoffsets[j + 1]])
                else:
                    if i != numblocks - 1:
                        if blockoffsets[i + 1] - blockoffsets[i] - tableoffsets[j] != 2 * charcounts[j]:
                            # size - tableoffsets[j] == blockoffsets[i+1]-tableoffsets[j]
                            print("当前分块长度为：", size)
                            print(blockoffsets[i], tableoffsets[j], charcounts[j])
                            print('疑似于块尾部存在填充，位置：', (blockoffsets[i] + tableoffsets[j]) + 2 * charcounts[j])
                            print("填充长度为：", blockoffsets[i + 1] - blockoffsets[i] - tableoffsets[j] - 2 * charcounts[j])
                            print("填充内容为：", f[(blockoffsets[i] + tableoffsets[j]) + 2 * charcounts[j]:blockoffsets[i + 1]])
                        else:
                            print("块尾部没有填充。块长度为：", size)
                    else:
                        if len(f) - (blockoffsets[i] + tableoffsets[j]) != 2 * charcounts[j]:
                            # size - tableoffsets[j] == len(f) - (blockoffsets[i]+tableoffsets[j])
                            print("当前分块长度为：", size)
                            print("文件总长度为：", len(f))
                            print('疑似于文件尾部存在填充，位置：', (blockoffsets[i] + tableoffsets[j]) + 2 * charcounts[j])
                            print("填充长度为：", len(f) - (blockoffsets[i] + tableoffsets[j]) - 2 * charcounts[j])
                            print("填充内容为：", f[(blockoffsets[i] + tableoffsets[j]) + 2 * charcounts[j]:len(f)])
                        else:
                            print("文件尾部没有填充。块长度为：", size)
                            print("文件总长度为：", len(f))

            while decchars:  # 控制符处理
                c = decchars.pop(0)
                if c == 0xFFFF:  # 字符码为0xFFFF时说明已经读到文段，结束处理跳出
                    if fillflag:
                        if decchars:
                            print("第{}块的第{}分节后的填充为：{}".format(i, j, decchars))  # 剩下的都是填充
                            print("分节总长度为：{}，填充长度为：{}".format(charcounts[j], len(decchars)))
                        else:
                            print("第{}块的第{}分节没有填充。".format(i, j))
                            print("分节总长度为：{}".format(charcounts[j]))
                    break
                elif c == 0xFFFE:
                    text += "\n"  # \\n
                elif c < 20 or c > 0xFF60:  # 中文全角标点符号和全角英文码在0xFF00 - 0xFF60之间，必须囊括
                    text += "<" + "x%04X" % c + ">"  # \\x%04X%c
                elif c == 0xF000:
                    try:
                        kind = decchars.pop(0)
                        count = decchars.pop(0)
                        if kind == 0xbe00 and count == 0:
                            text += "<F>\n"  # \\f
                            continue
                        if kind == 0xbe01 and count == 0:
                            text += "<PAGE>\n"  # \\r
                            continue
                        text += "<VAR("
                        args = [kind]
                        for k in range(count):
                            args.append(decchars.pop(0))
                    except IndexError:
                        break
                    text += ", ".join(map(str, args))
                    text += ")>"
                else:
                    text += chr(c)
            e = "%i_%i" % (i, j)  # 文段(版块号，分节号)标记
            flag = ""
            val = textflags[j]  # 从分节标志表取出当前节标志
            c = 65
            while val:
                if val & 1:  # val2进制末位为1时就是章节标记的字符名
                    flag += chr(c)
                c += 1
                val >>= 1
            if compressed:  # 压缩标记
                flag += "c"
            # print([e,text])
            e += flag + subline
            text += subline
            texts.append([e, text])  # 当前文本段处理完毕，加入文本表texts
            # print([e,text])
    return texts


def gen5put(texts):  # 加密导入单文本文件
    textofs = {}
    sizes = {}
    comments = {}
    textflags = {}
    blockwriters = {}
    for entry in texts:
        # print(entry)
        for num in range(len(entry)):  # 去掉参考线
            entry[num] = entry[num].replace(subline, '')
        # print(entry)

        match = re.match("([^_]+)_([0-9]+)(.*)", entry[0])
        if not match:
            continue
        blockid = match.group(1)
        textid = int(match.group(2))
        flags = match.group(3)
        # print(blockid,textid,flags)
        text = entry[1]
        if blockid.lower() == "comment":
            comments[textid] = text
            continue
        blockid = int(blockid)
        if blockid not in blockwriters:
            blockwriters[blockid] = binarywriter()
            textofs[blockid] = {}
            sizes[blockid] = {}
            textflags[blockid] = {}
        textofs[blockid][textid] = blockwriters[blockid].pos()
        dec = []
        while text:
            c = text[0]
            if c == '\n':  # 补上隐藏的换行符（导出时直接用\n是为了方便翻译，导入时为了方便批量处理就重新加上）
                text = '<n>' + text
                c = text[0]
            text = text[1:]
            if c == '<':
                c = text[0]
                text = text[1:]

                dr = text.find('>')  # 去掉导出时加入的控制符的尾部>
                ltext = list(text)  ###xxxxxx
                ltext.pop(dr)
                # print(ltext)
                try:
                    if c != "V":#VAR控制符后面可能出现自带"\n"的状况
                        if len(ltext) != 0 and ltext[dr] == '\n':
                            ltext.pop(dr)  # 去掉'>'后的'\n'
                except IndexError:
                    pass  # 说明'>'在最后且没有‘\n’，是x控制符
                # print(ltext)
                text = ''.join(ltext)

                if c == 'x':
                    n = int(text[:4], 16)
                    # print("n:",n)
                    # print("text:",text)
                    text = text[4:]
                    # print("text:",text)
                elif c == 'n':
                    n = 0xFFFE
                elif c == 'P' and text[:3] == 'AGE':
                    dec.append(0xF000)
                    dec.append(0xbe01)
                    dec.append(0)
                    # print("text:",text)
                    text = text[3:]
                    # print("text:",text)
                    continue
                elif c == 'F':
                    dec.append(0xF000)
                    dec.append(0xbe00)
                    dec.append(0)
                    continue
                elif c == 'V':
                    if text[:2] == "AR":
                        text = text[3:]
                        eov = text.find(")")
                        args = list(map(int, text[:eov].split(",")))
                        text = text[eov + 1:]
                        dec.append(0xF000)
                        dec.append(args.pop(0))
                        dec.append(len(args))
                        for a in args:
                            dec.append(a)
                    else:
                        dec.append(ord('V'))
                    continue
                else:
                    n = 1
                dec.append(n)

            else:
                dec.append(ord(c))
        # print("dec:",len(dec))
        flag = 0
        for i in range(16):
            if chr(65 + i) in flags:
                flag |= 1 << i
        textflags[blockid][textid] = flag
        if "c" in flags:
            print("存在压缩。")
            comp = [0xF100]
            container = 0
            bit = 0
            while dec:
                c = dec.pop(0)
                if c >> 9:
                    print("非法压缩字符： %i" % c)
                container |= c << bit
                bit += 9
                while bit >= 16:
                    bit -= 16
                    comp.append(container & 0xFFFF)
                    container >>= 16
            container |= 0xFFFF << bit
            comp.append(container & 0xFFFF)
            dec = comp[:]

        key = (0x7C89 + textid * 0x2983) & 0xFFFF  # 必须&0FFFF保证数值限定在2Byte内#key的初始值不可为0，否则不会加密
        enc = []
        # 逐字加密
        while dec:
            char = dec.pop(0) ^ key
            # print("key:",key)
            key = ((key << 3) | (key >> 13)) & 0xFFFF
            enc.append(char)
        fills = [0xFFFF for num in range(len(enc))]  # 制造没有加密的填充
        enc.append(key ^ 0xFFFF)  # 文段末尾一定有一个停止符0xFFFF
        while fills:  # 给填充加密然后放进末尾
            key = ((key << 3) | (key >> 13)) & 0xFFFF
            fill = fills.pop() ^ key
            enc.append(fill)

        sizes[blockid][textid] = len(enc)
        # print("enc:",len(enc))
        for e in enc:  # 将加密的每个字加入预写入列表
            blockwriters[blockid].write16(e)
    numblocks = max(blockwriters) + 1
    if numblocks != len(blockwriters):
        raise KeyError
    numentries = 0
    for block in blockwriters:
        numentries = max(numentries, max(textofs[block]) + 1)
    offsets = []
    baseofs = 12 + 4 * numblocks
    textblock = binarywriter()
    blocksizelist = []
    for i in range(numblocks):
        data = blockwriters[i].toarray()
        offsets.append(baseofs + textblock.pos())
        relofs = numentries * 8 + 4
        blocksize = len(data) * 2 + relofs
        print("blocksize：", blocksize)
        if blocksize % 4:  # 如果blocksize%16不为0，则执行下面的语句
            print("4除块长度的余数为：", blocksize % 4)
            # 块长度无法整除4，需要在其后填0xFFFF
            fnum = blocksize % 4
            key = ((key << 3) | (key >> 13)) & 0xFFFF
            data.extend([key ^ 0xFFFF for num in range(int(fnum / 2))])
            blocksize = blocksize + fnum
            print("填充{}个0xFFFF后，块长度与4的余数为：{}".format(int(fnum / 2), blocksize % 4))
        print("blocksize：", blocksize)
        blocksizelist.append(blocksize)
        textblock.write32(blocksize)  # 对应块的大小
        for j in range(numentries):  # 每组8Byte的块的分节信息表
            textblock.write32(textofs[i][j] + relofs)  # 对应分节的偏移地址4Byte
            textblock.write16(sizes[i][j])  # 对应分节的字数2Byte
            textblock.write16(textflags[i][j])  # 对应分节的标识值2Byte
        textblock.writear(data)
    writer = binarywriter()  # 构造文件头
    writer.write16(numblocks)  # 2Byte总分块数
    writer.write16(numentries)  # 2Byte分节数
    print(blocksizelist)
    print("max(blocksizelist):", max(blocksizelist))
    writer.write32(max(blocksizelist))  # 4Byte最大块大小（用于游戏中分配内存）
    writer.write32(0)  # 4Byte的0填充
    for i in range(numblocks):
        writer.write32(offsets[i])
    writer.writear(textblock.toarray())
    return writer.tobytes()


def maketxtput(raw):  # raw是file.readlines()
    # 将文本处理为gen5put()可处理的entry列表形式
    flag = -1
    entry = []
    texts = []
    s = ''
    for i in range(len(raw)):
        match = re.match("([^_]+)_([0-9]+)(.*)", raw[i])
        if match:  # 说明遇到了节标记
            if s != '':  # 说明当前遇到的节标记是下一节的
                entry.append(s)  # 上一节的第二部分内容完成
                texts.append(entry)  # 把完成的上一节加入列表
                entry = []  # 清空预备给下一节
            s = raw[i]
            flag = 0
        elif flag == 0:  # 说明上一个是节标记
            s = s + raw[i]  # 加上subline
            entry.append(s)  # 当前节的第一部分完成
            s = ''
            flag = 1
        elif flag == 1:
            s = s + raw[i]
        # 只有上面的逻辑会丢失最后一节
        if i == len(raw) - 1:
            entry.append(s)  # 最后一节的第二部分内容完成
            texts.append(entry)  # 把最后一节的内容加入列表
    return texts


if __name__ == "__main__":#Just for code testing
    # 导出单个分片文本
    filepath = 'B(JP)2-13'
    with open(filepath, 'rb') as f:
        texts = gen5get(f.read(),fillflag=True)
        with open(filepath + '.txt', 'w', encoding='utf16') as w:
            for line in texts:
                w.writelines(line)
    print(texts)
    # 导入单个分片文本
    ifilepath = filepath + '.test'
    with open(filepath + '.txt', 'r', encoding='utf16') as txtf:
        raw = txtf.readlines()
        texts = maketxtput(raw)
    with open(ifilepath, 'wb') as f:
        f.write(gen5put(texts))

    # 再导出看和导出的原文本是否相同
    with open(ifilepath, 'rb') as f:
        texts = gen5get(f.read(),fillflag=True)
        with open(ifilepath + '.txt', 'w', encoding='utf16') as w:
            for line in texts:
                w.writelines(line)
