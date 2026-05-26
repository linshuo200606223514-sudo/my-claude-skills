---
name: docx-layout
description: 对 Word 文档（.docx）进行专业排版重排。Use when 用户要排版 docx、美化 Word 文档、图文教程重排版。自动提取原文本和图片，按章节步骤重新组织，输出带标题/步骤/代码块/图片的排版版文档。
---

# docx-layout

对 .docx 文件进行专业排版，保留原始图片，重新组织结构。

## 工作流程

1. **提取内容** — 用 `scripts/extract.py` 从源文件提取文本和图片
2. **分析结构** — 理解原文内容，规划章节划分和步骤顺序
3. **生成文档** — 用 `scripts/layout.py` 中的排版工具函数生成新 docx

## 使用方式

用户提供 .docx 路径，执行：

```bash
python scripts/extract.py <源文件路径> <图片输出目录>
```

然后根据提取的内容，编写排版脚本调用 `scripts/layout.py` 的工具函数生成新文档。

## 注意事项

- 源文件含中文路径时，先用 `shutil.copy2` 复制到 ASCII 临时路径再处理
- 图片顺序：按 rId 数字顺序对应步骤顺序（image1.png → 步骤1）
- 输出文件名：原文件名 + `（排版版）`，保存到同目录
- 排版工具函数见 `scripts/layout.py`

## 排版风格

- 标题：居中，18pt，深色 `#1A1A2E`
- 章节：13pt 粗体，深色
- 步骤编号：12pt 粗体，红色 `#E84A5F`
- 代码/指令块：10pt Courier New，蓝色 `#2E86AB`，灰底 `#F0F4F8`
- 提示文字：10pt，灰色 `#888888`
- 图片：居中，宽度 5.2 英寸
- 章节间加分隔线
