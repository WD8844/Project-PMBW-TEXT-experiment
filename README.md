# 准备工作
## 从ROM中导出Narc
使用[tinke](https://github.com/pleonex/tinke)读取*.nds导出a/0/0/2、a/0/0/3和a/0/2/3
其中：
a/0/0/2 系统文本集
a/0/0/3 剧情文本集
a/0/2/3 字体集（字库）
## 分解Narc

# 文本处理
## 整体流程
改文本→做码表→改字库→文本和字库都导入narc打包→tinke导入对应New

## 文本导入打包流程
用CMP_Div_main.py组合文本
→将CH批量移动到CH目录覆盖
→用InjectTXTNarc.py批量导入分片
→用MakeNarc.py打包文本Narc生成对应New_a002和New_a003

## 做码表的流程
将所有CH复制到Counts目录
→用WQSG对照组合的原始全码表，指定起始编码为025B，统计Counts目录的全文生成CHS.TBL的中文码表
→用覆盖重做码表.py重做新码表得到_test.TBL，即为最新码表。

## 修改重做字库调用流程
用MakeFonts_main.py参照CHS.TBL做中文字库
→用Change三件套修改Width、Bitmap和CodeList
→InjectNftr.py导入分片→MakeNarc.py打包字库生成New_a023
