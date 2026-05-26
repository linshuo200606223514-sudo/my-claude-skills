---
name: brainstorming
description: AI驱动的选题策划工具，自动生成月度选题日历。支持多行业、多平台内容规划，基于数据分析生成精准选题。用于用户需要策划内容、生成选题日历、制定内容计划时。
version: 1.0.0
metadata:
  author: Yeluyun AI
  homepage: https://www.yeluyun.com
---

# 选题策划 (Brainstorming)

AI驱动的智能选题策划工具，自动生成月度/周度选题日历。

## 使用场景

- 制定月度内容日历
- 竞品选题分析
- 热点选题挖掘
- 内容规划提案

## 脚本目录

`{baseDir}` = this SKILL.md's directory. Main script: `{baseDir}/scripts/main.js`

## 使用方法

### 基本用法

```bash
node {baseDir}/scripts/main.js --brand "品牌名称" --industry "行业" --platform "小红书,抖音" --month 2026-05
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--brand` | 品牌名称 | `--brand "夜鹭云"` |
| `--industry` | 所属行业 | `--industry "科技"` |
| `--platform` | 目标平台 | `--platform "小红书,抖音,公众号"` |
| `--month` | 规划月份 | `--month 2026-05` |
| `--count` | 生成选题数量 | `--count 30` (默认30) |
| `--output` | 输出文件路径 | `--output ./calendar.md` |

### 输出格式

生成 Markdown 格式的选题日历，包含：
- 每日选题主题
- 内容方向描述
- 适合平台标签
- 预计效果指标

## 示例

```bash
# 生成5月份选题日历
node {baseDir}/scripts/main.js --brand "夜鹭云" --industry "人工智能" --platform "小红书,抖音" --month 2026-05 --count 30

# 输出到指定文件
node {baseDir}/scripts/main.js --brand "某品牌" --industry "美妆" --platform "小红书" --month 2026-05 --output ./output/calendar.md
```

## 技术实现

- 使用 Claude API 进行 AI 选题生成
- 支持多平台内容适配
- 结构化输出 Markdown 格式
- 可自定义选题数量和格式
