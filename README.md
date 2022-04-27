# 中英文文本去除空格与换行符

## 描述

使用场景：图片文字识别、在 PDF 中拷贝文本，等等

作用：
1. 去除中文文字之间的空格
2. 去除被换行的大段文本的换行符，恢复为一整段文字
3. 连续换行的情况会保留换两行
4. MAC 地址格式转换

## 运行环境

- Python环境：Python 3.9.0
- Qt Designer: 5.11.1

## 引用的库

- PyQt5: 5.15.4
- 中英文混排补空格：[pangu.py](https://github.com/vinta/pangu.py) (Python)

## 食用方法

1. 运行脚本
2. 复制待处理的文本
3. 点击按钮即可，处理结果会自动覆盖剪贴板内容，同时显示在文本框中

### 示例 #1

原文本：

```
   Encapsulation Methods for Transport of Ethernet over MPLS Networks

Status of This Memo

   This document specifies an Internet standards track protocol for the
   Internet community, and requests discussion and suggestions for
   improvements.  Please refer to the current edition of the "Internet
   Official Protocol Standards" (STD 1) for the standardization state
   and status of this protocol.  Distribution of this memo is unlimited.

Copyright Notice

   Copyright (C) The Internet Society (2006).

```

处理结果：

```
Encapsulation Methods for Transport of Ethernet over MPLS Networks

Status of This Memo

This document specifies an Internet standards track protocol for the Internet community, and requests discussion and suggestions for improvements. Please refer to the current edition of the "Internet Official Protocol Standards" (STD 1) for the standardization state and status of this protocol. Distribution of this memo is unlimited.

Copyright Notice

Copyright (C) The Internet Society (2006).
```

### 示例 #2

原文本：

```
相关命令

asbr-summary not-advertise（OSPF）

asbr-summary not-advertise（OSPF）命令和filter-policy export
（OSPF）命令作用一样，但是asbr-summary not-advertise（OSPF）
命令可以在NSSA 区域的ABR 上对7 转5 的LSA 做过滤，阻止本路
由器根据nssa 产生符合特定条件的ase，从而对NSSA LSA 实现在
ASBR 过滤之后的二次过滤。
```

处理结果：

```
相关命令

asbr-summary not-advertise（OSPF）

asbr-summary not-advertise（OSPF）命令和 filter-policy export （OSPF）命令作用一样，但是 asbr-summary not-advertise（OSPF）命令可以在 NSSA 区域的 ABR 上对 7 转 5 的 LSA 做过滤，阻止本路由器根据 nssa 产生符合特定条件的 ase，从而对 NSSA LSA 实现在 ASBR 过滤之后的二次过滤。
```

