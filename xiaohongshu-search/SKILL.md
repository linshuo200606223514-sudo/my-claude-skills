---
name: xiaohongshu-search
description: "小红书笔记搜索、爬取正文、自动发布。Use when user wants to search Xiaohongshu, 搜小红书, 小红书笔记, 红薯搜索, XHS search, 小红书热门, 爬取小红书, 小红书发布, 自动发布小红书. Capabilities: 关键词搜索笔记列表、逐篇爬取正文、提取单篇详情、自动填写发布内容、Chrome CDP绕过反爬。"
argument-hint: "[search|crawl|publish|detail] [参数...]"
---

# 小红书工具箱

通过 Chrome CDP 远程调试连接真实浏览器，绕过小红书反爬检测。

## 前置条件：启动 Chrome CDP

**每次使用前必须确保 Chrome 以调试模式运行：**

```bash
# 检查 CDP 是否已运行
curl -s http://localhost:9223/json/version > /dev/null 2>&1
if [ $? -ne 0 ]; then
  taskkill /F /IM chrome.exe 2>/dev/null
  sleep 1
  "/c/Program Files/Google/Chrome/Application/chrome.exe" \
    --remote-debugging-port=9223 \
    --user-data-dir="$TEMP/chrome-debug-xhs" \
    "https://www.xiaohongshu.com" &
  echo "Chrome started, please login to xiaohongshu.com, then press Enter"
  read
fi
```

Python 路径：`/c/Users/clown/AppData/Local/Python/bin/python.exe`

脚本目录：`C:/Users/clown/.claude/skills/xiaohongshu-search/scripts/`

---

## 功能一：搜索笔记列表（search）

快速搜索，只提取标题/作者/点赞/链接，不进入笔记详情。

```bash
PY="/c/Users/clown/AppData/Local/Python/bin/python.exe"
SCRIPTS="C:/Users/clown/.claude/skills/xiaohongshu-search/scripts"

$PY "$SCRIPTS/search.py" "母亲节" 25 9223
```

参数：`<关键词> [最大数量=25] [CDP端口=9223]`

输出 JSON 数组，每项：`{title, author, likes, url}`

---

## 功能二：深度爬取正文（crawl）

逐篇点击进入笔记，提取完整正文、标签、互动数据。带人类行为模拟和风控检测。

```bash
$PY "$SCRIPTS/crawl.py" "母亲节" 10 9223 30
```

参数：`<关键词> [最大篇数=10] [CDP端口=9223] [每日上限=30]`

输出 JSON 数组，每项：`{title, content, author, likes, collects, comments, tags, url}`

**注意：** 每日计数存在 `~/.xhs_daily_counter.json`，超出上限自动停止。

---

## 功能三：单篇笔记详情（detail）

提取指定 URL 的笔记详情。

```bash
$PY "$SCRIPTS/detail.py" "https://www.xiaohongshu.com/explore/xxx" 9223
```

参数：`<笔记URL> [CDP端口=9223]`

输出：`{title, content, author, likes, collects, comments, tags}`

---

## 功能四：自动发布（publish）

自动填写标题和正文，最后一步需人工点击「发布」。

```bash
$PY "$SCRIPTS/publish.py" "标题" "正文内容\n第二行" "/path/to/image.png" 9223
```

参数：`<标题> <正文> [图片绝对路径] [CDP端口=9223]`

- 正文用 `\n` 表示换行
- 图片路径可选，不传则跳过上传
- 发布前需先打开 `https://creator.xiaohongshu.com/publish/publish`

---

## 保存结果

搜索/爬取结果保存到文件：

```bash
OUTDIR="C:/Users/clown/Desktop/小红书工具箱/数据"
KEYWORD="母亲节"
DATE=$(date +%Y%m%d)

$PY "$SCRIPTS/search.py" "$KEYWORD" 25 > "$OUTDIR/${KEYWORD}_XHS_${DATE}.json"
# 同时生成 txt 摘要
$PY -c "
import json, sys
data = json.load(open('$OUTDIR/${KEYWORD}_XHS_${DATE}.json', encoding='utf-8'))
for i, n in enumerate(data, 1):
    print(f'{i}. {n[\"title\"]} | {n[\"author\"]} | 点赞:{n[\"likes\"]}')
" > "$OUTDIR/${KEYWORD}_XHS_${DATE}.txt"
```

---

## 关键 DOM 选择器

| 元素 | 选择器 |
|------|--------|
| 笔记卡片 | `section.note-item` |
| 标题 | `.title span` / `.title` |
| 作者 | `.author-wrapper .name` |
| 点赞数 | `.like-wrapper .count` |
| 笔记链接 | `a.cover` / `a[href*="/explore/"]` |
| 模态框正文 | `#detail-desc .note-text` |
| 发布标题输入 | `input[placeholder*="标题"]` |
| 发布正文编辑器 | `.tiptap.ProseMirror` |
| 图片上传 | `input[type="file"].upload-input` |

---

## 已知陷阱

1. **不要截图** — `page.screenshot()` 超时30s+，crawl.py 已改为只在风控时截图
2. **必须等6秒** — 搜索后异步渲染，不等会拿到空数据
3. **UTF-8** — Windows终端中文乱码，所有脚本已内置 `sys.stdout` UTF-8 处理
4. **Python路径** — Windows Store python 是占位符(exit 49)，用 `/c/Users/clown/AppData/Local/Python/bin/python.exe`
5. **Cookie不可迁移** — TLS/JA3指纹绑定，必须CDP连同一Chrome实例
6. **滚动加载** — 懒加载机制，search.py 已内置3次滚动
7. **发布正文** — 必须用 clipboard 粘贴（`navigator.clipboard.writeText` + Ctrl+V），直接 fill 中文会乱
8. **图片上传** — 用 `query_selector` 不用 `wait_for_selector`（hidden input）

## 脚本文件

- `scripts/search.py` — 搜索笔记列表，输出JSON
- `scripts/crawl.py` — 深度爬取正文，带人类行为模拟
- `scripts/detail.py` — 提取单篇笔记详情，输出JSON
- `scripts/publish.py` — 自动填写发布内容（通用版，参数化）
