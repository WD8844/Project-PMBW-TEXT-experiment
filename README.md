# 1.准备工作
## 从ROM中导出Narc
使用[tinke](https://github.com/pleonex/tinke)读取*.nds导出a/0/0/2、a/0/0/3和a/0/2/3这三个Narc文件
其中：

a/0/0/2 系统文本集

a/0/0/3 剧情文本集

a/0/2/3 字体集（字库）

## 分解Narc
為了方便後續操作，建议将上述通过tinke提取出来的文件重命名，以日版(JP)的Narc文件为例：

a/0/0/2 重命名为 B(JP)2

a/0/0/3 重命名为 B(JP)3

a/0/2/3 重命名为 a023

将这些Narc文件与*.py放在同级目录下，在控制台Command Line(CMD)中按

ExtractNarc.py <文件名> <处理类型：输入text（文本）或file（其它）>执行语句：

>>ExtractNarc.py B(JP)2 text

>>ExtractNarc.py B(JP)3 text

>>ExtractNarc.py a023 file

由此就创建了：

B(JP)2_extr、B(JP)3_extr和a023_extr这三个分别对应B(JP)2、B(JP)3和a023的子文件夹，其中包含其解包后按照编号命名的文件块。

# 2.文本处理
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
