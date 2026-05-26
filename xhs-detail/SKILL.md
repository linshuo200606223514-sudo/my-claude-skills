---
name: xhs-detail
description: 提取单篇小红书笔记的详情（标题、正文、作者、点赞、收藏、评论、标签）。Use when user wants to 获取小红书笔记详情、提取小红书正文、xhs detail、抓取某篇小红书. Requires Chrome CDP connection.
---

# xhs-detail

提取单篇小红书笔记的详情（标题、正文、作者、点赞、收藏、评论、标签）。

## 触发条件

用户说：获取小红书笔记详情、提取小红书正文、xhs detail、抓取某篇小红书

## 用法

```bash
python "C:/Users/clown/Desktop/小红书工具箱/脚本/xhs_detail.py" <笔记URL> [CDP端口=9223]
```

## 前置条件

- Chrome 已用 `--remote-debugging-port=9223` 启动并登录小红书
- 已安装 playwright：`pip install playwright && playwright install chromium`

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 笔记URL | 完整的小红书笔记链接 | 必填 |
| CDP端口 | Chrome 调试端口 | 9223 |

## 输出

JSON 对象：`title`, `content`, `author`, `likes`, `collects`, `comments`, `tags`

## 示例

```bash
python "C:/Users/clown/Desktop/小红书工具箱/脚本/xhs_detail.py" "https://www.xiaohongshu.com/explore/xxx"
```
