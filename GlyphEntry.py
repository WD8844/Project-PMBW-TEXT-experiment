class GlyphEntry:#字模类
    def __init__(self, offset = 0, width = 0 ,rows = 0, charCode = None, buffer = None):
        self.offset = offset#字模地址
        self.width = width#字模宽度（单扫描行的长度）
        self.rows = rows#字模的扫描行总数（高度）
        self.charCode = charCode#字符编码
        self.buffer = buffer#字模数据

if __name__ == "__main__":
    test = GlyphEntry
    test.offset = 24
    print(test.offset)
