---
name: B
description: Use when ending a work session, completing a significant task, or when user asks to record achievements, summarize progress, or save results for the day
---

# 成果记录

## Overview

Records conversation achievements to a dated folder on desktop under a master `成果记录` folder. Creates `桌面/成果记录/YYYY-MM-DD/成果记录.txt` with structured summary of what was accomplished.

## When to Use

- Work session ending
- Significant task completed
- User asks: "记录成果", "保存今天的", "写下来"
- Milestone reached

## Core Pattern

1. **确定日期**: `YYYY-MM-DD` 格式
2. **创建文件夹**: `桌面/成果记录/{日期}/`
3. **写成果文件**: `{日期}/成果记录.txt`
4. **结构化内容**:

```
{日期} 今日成果
==================

## [项目名称1]
- 具体完成内容
- 关键成果/文件路径

## [项目名称2]
...
```

## Quick Reference

| 触发词 | 操作 |
|--------|------|
| "记录成果"、"保存今天的"、"写下来" | 创建文件夹并写入成果记录.txt |

## Implementation

总文件夹: `C:\Users\clown\Desktop\成果记录`
子文件夹: `C:\Users\clown\Desktop\成果记录\{YYYY-MM-DD}\`

**步骤：**
1. `Bash`: `mkdir -p "C:\Users\clown\Desktop\成果记录\{YYYY-MM-DD}"`
2. `Bash/Write`: `成果记录.txt`，内容结构见 Core Pattern

## Common Mistakes

| 错误 | 正确做法 |
|------|----------|
| 只写文件名不加日期 | 文件名 = `{YYYY-MM-DD}/成果记录.txt` |
| 内容写成流水账 | 按结构分 ## 大项，每项列具体成果 |
| 用旧日期 | 始终用当天日期 `YYYY-MM-DD` |
| ## 小节用序号 | ## 小节应为项目名称，不是 "1. xxx" |
