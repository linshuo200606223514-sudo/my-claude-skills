---
name: canvas-design
description: AI智能设计工具，自动生成小红书封面、公众号头图、海报等营销素材。支持多种风格、尺寸和文案，输入主题即可生成可用的图片。
version: 1.0.0
metadata:
  author: Yeluyun AI
  homepage: https://www.yeluyun.com
---

# 智能设计 (Canvas Design)

AI驱动的图片生成工具，快速生成各类营销素材。

## 使用场景

- 小红书封面图生成
- 公众号头图制作
- 产品海报设计
- 营销素材配图

## 脚本目录

`{baseDir}` = this SKILL.md's directory. Main script: `{baseDir}/scripts/main.js`

## 使用方法

### 基本用法

```bash
node {baseDir}/scripts/main.js --prompt "AI科技感风格" --platform "小红书" --output ./cover.png
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--prompt` | 图片描述/主题 | `--prompt "科技产品展示"` |
| `--platform` | 目标平台 | `--platform "小红书"` |
| `--style` | 风格要求 | `--style "简约专业"` |
| `--text` | 封面文字 | `--text "AI赋能新媒体"` |
| `--output` | 输出文件路径 | `--output ./cover.png` |
| `--size` | 图片尺寸 | `--size "3:4"` (默认平台自适应) |

### 支持的平台尺寸

| 平台 | 推荐尺寸 | 比例 |
|------|---------|------|
| 小红书 | 1240x1660 | 3:4 |
| 公众号 | 900x383 | 2.35:1 |
| 抖音 | 1080x1920 | 9:16 |
| 微博 | 1600x900 | 16:9 |
| 朋友圈 | 1080x1080 | 1:1 |

### 风格选项

- `简约专业` - 适合知识干货类
- `时尚潮流` - 适合时尚美妆类
- `可爱活泼` - 适合生活娱乐类
- `科技未来` - 适合科技数码类
- `清新自然` - 适合美食旅游类

## 示例

```bash
# 生成小红书封面
node {baseDir}/scripts/main.js \
  --prompt "科技数码产品展示" \
  --platform "小红书" \
  --style "简约专业" \
  --text "2026最新AI工具清单" \
  --output ./xhs_cover.png

# 生成公众号头图
node {baseDir}/scripts/main.js \
  --prompt "数据图表风格" \
  --platform "公众号" \
  --style "简约专业" \
  --text "月入10万的方法" \
  --output ./mp_cover.png
```

## 技术实现

- 使用 MiniMax Jimeng (即梦) API 进行图片生成
- 支持多种尺寸比例
- 支持添加文字水印
- 输出 PNG/JPEG 格式
