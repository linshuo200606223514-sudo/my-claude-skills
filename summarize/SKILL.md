---
name: summarize
description: AI批量内容总结工具，自动抓取并总结文章/视频内容。支持网页文章、B站视频、小红书笔记等多种内容源的批量分析。用于竞品调研、内容分析、资料整理等场景。
version: 1.0.0
metadata:
  author: Yeluyun AI
  homepage: https://www.yeluyun.com
---

# 内容总结 (Summarize)

AI批量内容总结工具，自动抓取并总结多种格式的内容。

## 使用场景

- 竞品文章批量分析
- B站/小红书视频内容提取
- 行业报告快速阅读
- 内容素材收集整理

## 脚本目录

`{baseDir}` = this SKILL.md's directory. Main script: `{baseDir}/scripts/main.js`

## 使用方法

### 基本用法

```bash
# 单个URL
node {baseDir}/scripts/main.js --url "https://example.com/article"

# 批量URL（txt文件，每行一个）
node {baseDir}/scripts/main.js --file urls.txt

# 关键词搜索
node {baseDir}/scripts/main.js --keyword "人工智能趋势" --count 10
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--url` | 单个内容URL | `--url "https://bilibili.com/video/..."` |
| `--file` | URL列表文件 | `--file ./urls.txt` |
| `--keyword` | 搜索关键词 | `--keyword "竞品分析"` |
| `--count` | 搜索结果数量 | `--count 10` (默认10) |
| `--output` | 输出文件路径 | `--output ./summary.md` |
| `--format` | 输出格式 | `--format markdown` (默认markdown) |

### 支持的内容源

| 平台 | 支持类型 | 说明 |
|------|---------|------|
| B站 | 视频 | 自动提取视频简介和字幕 |
| 小红书 | 笔记 | 提取笔记正文和标签 |
| 微信公众号 | 文章 | 提取文章全文 |
| 普通网页 | 文章 | 提取正文内容 |
| 知乎 | 回答/文章 | 提取内容 |

### 输出格式

生成 Markdown 格式的总结报告，包含：
- 原始链接
- 内容摘要
- 关键要点
- 适用场景标签

## 示例

```bash
# 总结单个B站视频
node {baseDir}/scripts/main.js --url "https://www.bilibili.com/video/BV1xx411c7D"

# 批量总结文章
node {baseDir}/scripts/main.js --file competitor_urls.txt --output ./analysis/summary.md

# 关键词搜索总结
node {baseDir}/scripts/main.js --keyword "AI工具评测" --count 20 --output ./research/ai_tools.md
```

## 技术实现

- 使用crawl4ai/firecrawl进行网页内容抓取
- 使用bilibili-transcript提取B站字幕
- 使用Claude API进行AI内容总结
- 支持批量处理和并发控制
