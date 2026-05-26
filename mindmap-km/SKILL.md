---
name: mindmap-km
description: "生成 WPS 思维导图 .km 文件。Use when user wants to create a mind map, 写思维导图, 生成脑图, 做思维导图, KityMinder, WPS 思维导图."
argument-hint: "<主题> [文件名]"
---

# WPS 思维导图生成器

生成 KityMinder `.km` 格式文件，可直接在 WPS 思维导图中导入使用。

## 规则

1. 节点文字只写**功能/用途描述**，不写技术词（不写命令、代码、参数）
2. 需要链接时用 `hyperlink` + `hyperlinkTitle` 字段
3. 用父节点做分组（如"已完成"、"待办"、"工具类"等）
4. 默认保存到 `C:/Users/clown/Desktop/Skills资料/<文件名>.km`

## .km 文件格式

```json
{
  "root": {
    "data": {
      "text": "根节点标题",
      "hyperlink": "https://...",        // 可选
      "hyperlinkTitle": "链接说明"        // 可选
    },
    "children": [
      {
        "data": {
          "text": "分组或子节点",
          "hyperlink": "https://...",    // 可选
          "hyperlinkTitle": "链接说明"   // 可选
        },
        "children": [
          { "data": { "text": "叶子节点" } }
        ]
      }
    ]
  },
  "template": "default",
  "theme": "fresh-red",
  "version": "1.4.43"
}
```

## 可用主题

| theme 值 | 效果 |
|----------|------|
| `fresh-red` | 红色清新（默认） |
| `fresh-blue` | 蓝色清新 |
| `fresh-green` | 绿色清新 |
| `classic` | 经典黑白 |
| `snow` | 简洁白色 |

## 工作流程

1. 理解用户要做什么内容的思维导图
2. 如需要链接，先确认链接来源（本地文件 or 网页）
3. 用 Write 工具生成 `.km` 文件到桌面
4. 告知用户文件路径，提示在 WPS 思维导图中「导入」

## 示例

用户说：「把这 3 个工具做成思维导图，加上官网链接」

```json
{
  "root": {
    "data": { "text": "工具概览" },
    "children": [
      {
        "data": {
          "text": "工具A",
          "hyperlink": "https://tool-a.com",
          "hyperlinkTitle": "工具A 官网"
        },
        "children": [
          { "data": { "text": "能做什么事情1" } },
          { "data": { "text": "能做什么事情2" } }
        ]
      }
    ]
  },
  "template": "default",
  "theme": "fresh-red",
  "version": "1.4.43"
}
```
