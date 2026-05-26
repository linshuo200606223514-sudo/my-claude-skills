---
name: bilibili-search
description: "B站视频搜索并提取内容。Use when user wants to 搜索B站, 在B站找视频, bilibili search, 搜索bilibili视频内容, 查找B站相关视频."
---

# B站视频搜索与内容提取

## 工作流程

### 第一步：用 B站搜索 API 获取视频列表

用 `mcp__plugin_playwright_playwright__browser_navigate` 打开任意 B站页面（确保 cookie 生效），然后用 `mcp__plugin_playwright_playwright__browser_evaluate` 调用搜索 API：

```js
async () => {
  const keyword = encodeURIComponent('YOUR_KEYWORD');
  const res = await fetch(
    `https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword=${keyword}&order=totalrank&page=1`,
    {credentials: 'include'}
  );
  const data = await res.json();
  return JSON.stringify(data?.data?.result?.slice(0, 10).map(v => ({
    title: v.title?.replace(/<[^>]+>/g, ''),
    bvid: v.bvid,
    play: v.play,
    author: v.author,
    description: v.description?.slice(0, 100)
  })));
}
```

- `order` 可选：`totalrank`（综合）、`click`（最多播放）、`pubdate`（最新）、`dm`（最多弹幕）、`stow`（最多收藏）
- 返回结果包含标题、BV号、播放量、作者、简介

### 第二步：筛选相关视频

根据标题和简介，选出与用户需求最相关的 2-3 个视频，记录其 BV号。

### 第三步：提取视频内容（字幕优先）

对每个目标视频，先打开页面获取 cid：

```js
() => {
  const state = window.__INITIAL_STATE__;
  return JSON.stringify({
    bvid: state?.videoData?.bvid,
    cid: state?.videoData?.cid,
    title: state?.videoData?.title
  });
}
```

然后检查是否有 AI 字幕：

```js
async () => {
  const res = await fetch(`https://api.bilibili.com/x/player/v2?cid=${CID}&bvid=${BVID}`, {credentials: 'include'});
  const data = await res.json();
  return JSON.stringify(data?.data?.subtitle?.subtitles);
}
```

**有字幕**（subtitle_url 非空）→ 直接下载字幕 JSON，拼接所有 `content` 字段：

```js
async () => {
  const res = await fetch('SUBTITLE_URL');
  const data = await res.json();
  return data?.body?.map(s => s.content).join('');
}
```

**无字幕** → 进入第四步用 yt-dlp + Whisper 转录。

### 第四步：无字幕时用 yt-dlp + Whisper 转录

```bash
yt-dlp --extract-audio --audio-format mp3 -o "C:/tmp/bili_search_audio.%(ext)s" "https://www.bilibili.com/video/BVID"
```

```bash
python -m whisper "C:/tmp/bili_search_audio.mp3" --model small --language zh --output_format txt --output_dir "C:/tmp/"
```

读取转录结果（注意 UTF-8 编码）：

```python
raw = open('C:/tmp/bili_search_audio.txt', 'rb').read().decode('utf-8')
```

### 第五步：整理并输出结果

将搜索到的视频信息和提取的内容整理后直接输出给用户，包括：
- 视频标题、作者、播放量、BV号链接
- 视频核心内容摘要

## 注意事项

- B站搜索 API 需要在 B站域名下调用（携带 cookie），必须先 navigate 到 B站页面
- AI 字幕（`ai-zh`）无需登录即可获取，但 subtitle_url 有时效性
- Whisper `small` 模型中文效果好，`base` 更快
- Windows 下读取 Whisper 输出文件用 `open(path, 'rb').read().decode('utf-8')`，不要直接用 `encoding='utf-8'` 参数（终端显示乱码但文件本身是 UTF-8）
- 搜索关键词建议精准，多个关键词用空格分隔

## 常见问题

**搜索结果为空**
- 换更简短的关键词，避免过于具体
- 检查是否在 B站域名下执行 fetch

**字幕 subtitle_url 为空字符串**
- 说明字幕存在但需要登录，改用 yt-dlp + Whisper 方案

**yt-dlp 未安装**
```bash
pip install yt-dlp
```

**Whisper 未安装**
```bash
pip install openai-whisper
```
