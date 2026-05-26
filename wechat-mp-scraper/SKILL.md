---
name: wechat-mp-scraper
description: "微信公众号文章爬取工具。Use when user wants to scrape WeChat official account articles, 爬取微信公众号, 微信文章采集, 公众号内容抓取, wechat mp scraper, 微信爬虫. Capabilities: 单篇文章全文提取、搜狗微信关键词搜索、公众号历史文章列表、批量URL采集。"
argument-hint: "[article|search|account|batch] [参数...]"
---

# 微信公众号文章爬取工具

## 方案选择

| 场景 | 方案 | 是否需要登录 |
|------|------|------------|
| 单篇文章（已有链接） | 直接 HTTP 请求 | 否 |
| 关键词搜索文章 | 搜狗微信搜索 | 否（有频率限制） |
| 指定公众号文章列表 | 搜狗公众号搜索 | 否（有频率限制） |
| 批量采集多篇文章 | 直接 HTTP 请求 | 否 |
| 搜狗触发验证码 | Chrome CDP 绕过 | 需要手动过验证码 |

**NEVER 使用以下方式：**
- 微信 PC 客户端自动化（无公开 API）
- 直接调用微信内部 API（需 access_token，封号风险）
- 高频请求（间隔 < 3 秒）

---

## 功能一：单篇文章爬取（article）

给定 `mp.weixin.qq.com/s/xxx` 链接，提取标题、公众号、作者、发布时间、正文。

```bash
PY="/c/Users/clown/AppData/Local/Python/bin/python.exe"
SCRIPTS="C:/Users/clown/.claude/skills/wechat-mp-scraper/scripts"

$PY "$SCRIPTS/article.py" "https://mp.weixin.qq.com/s/xxxxxx" "C:/Users/clown/Desktop/微信文章"
```

参数：`<url> [output_dir=当前目录]`

输出 JSON：`{title, account, author, pub_time, content, images, url, scraped_at}`

---

## 功能二：关键词搜索（search）

通过搜狗微信搜索关键词，返回文章列表（标题、公众号、日期、摘要、链接）。

```bash
$PY "$SCRIPTS/search.py" "人工智能" 30
```

参数：`<keyword> [max_count=20] [cdp_port=9223]`

输出 JSON 数组：`[{title, account, date, snippet, url}]`

**注意：** 搜狗有频率限制，触发验证码时自动切换 CDP 模式（需先启动 Chrome）。

---

## 功能三：公众号文章列表（account）

搜索指定公众号，获取其历史文章列表。

```bash
$PY "$SCRIPTS/account.py" "人民日报" 30
```

参数：`<account_name> [max_count=20] [cdp_port=9223]`

输出 JSON 数组：`[{title, date, snippet, url, account}]`

---

## 功能四：批量采集（batch）

从文件或命令行读取多个 URL，批量爬取全文，保存为 JSON + TXT。

```bash
# 从文件读取 URL（每行一个）
$PY "$SCRIPTS/batch.py" urls.txt "C:/Users/clown/Desktop/微信文章"

# 直接传 URL 列表
$PY "$SCRIPTS/batch.py" - "C:/Users/clown/Desktop/微信文章" \
  "https://mp.weixin.qq.com/s/aaa" \
  "https://mp.weixin.qq.com/s/bbb"
```

参数：`<urls_file|-> <output_dir> [url1 url2 ...]`

间隔 3-6 秒随机，避免触发限流。

---

## Chrome CDP 模式（搜狗验证码时使用）

```bash
# 先关闭 Chrome，再以调试模式启动
taskkill /F /IM chrome.exe
"/c/Program Files/Google/Chrome/Application/chrome.exe" \
  --remote-debugging-port=9223 \
  --user-data-dir="$TEMP/chrome-debug-wx" \
  "https://weixin.sogou.com" &
```

Python 路径：`/c/Users/clown/AppData/Local/Python/bin/python.exe`

---

## 关键 DOM 选择器

| 元素 | 选择器 |
|------|--------|
| 文章标题 | `#activity-name`, `h1.rich_media_title` |
| 公众号名称 | `#js_name`, `.rich_media_meta_nickname` |
| 作者 | `#js_author_name` |
| 发布时间 | `#publish_time`, `em#publish_time` |
| 正文内容 | `#js_content` |
| 图片（懒加载） | `#js_content img[data-src]` |
| 阅读数 | `#js_read_count` （动态加载，常为空） |
| 搜狗文章卡片 | `.news-list li` |
| 搜狗标题 | `h3 a` |
| 搜狗公众号名 | `.account` |
| 搜狗日期 | `.s2` |
| 搜狗摘要 | `p.txt` |

---

## 已知陷阱

1. **图片懒加载** — 真实 URL 在 `data-src`，不在 `src`，article.py 已处理
2. **阅读数动态加载** — JS 渲染，直接 HTTP 拿不到，通常为空
3. **搜狗验证码** — 频繁请求触发，脚本自动检测并提示切换 CDP
4. **文章过期/删除** — 返回 "该内容已被发布者删除"，脚本会返回 `{error: "deleted"}`
5. **付费/仅粉丝可见** — 正文为空，需登录微信账号（暂不支持）
6. **UTF-8** — 所有脚本已内置 `sys.stdout` UTF-8 处理
7. **搜狗跳转链接** — search.py 返回的 URL 是搜狗 `/link?url=...` 格式，直接 HTTP 跟进会被反爬拦截。需在浏览器中打开，从地址栏复制最终的 `mp.weixin.qq.com/s/xxx` 链接，再传给 article.py

## 脚本文件

- `scripts/article.py` — 单篇文章全文提取
- `scripts/search.py` — 搜狗微信关键词搜索
- `scripts/account.py` — 公众号历史文章列表
- `scripts/batch.py` — 批量 URL 采集
