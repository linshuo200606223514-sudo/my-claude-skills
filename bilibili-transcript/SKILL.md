---
name: bilibili-transcript
description: "从B站视频提取文稿并保存到文件。Use when user wants to extract transcript, 提取文稿, 获取字幕, 转录视频 from a Bilibili/B站 video URL."
---

# Bilibili 视频文稿提取

## 工作流程

### 第一步：打开页面，获取视频信息

用 `mcp__playwright__browser_navigate` 打开视频 URL，然后用 `mcp__playwright__browser_evaluate` 获取 bvid 和 cid：

```js
() => {
  const state = window.__INITIAL_STATE__;
  if (state && state.videoData) {
    return JSON.stringify({
      aid: state.videoData.aid,
      bvid: state.videoData.bvid,
      cid: state.videoData.cid,
      title: state.videoData.title
    });
  }
  return 'not found';
}
```

### 第二步：检测官方字幕

```js
async () => {
  const res = await fetch(`https://api.bilibili.com/x/player/v2?cid=${CID}&bvid=${BVID}`, {credentials: 'include'});
  const data = await res.json();
  return JSON.stringify(data?.data?.subtitle?.subtitles);
}
```

- 如果 `subtitles` 数组非空，直接下载字幕 JSON（`subtitle_url` 字段），提取所有 `content` 拼接成文本，**跳到第五步**。
- 如果为空，继续第三步。

### 第三步：用 yt-dlp 下载音频（推荐）

优先用 yt-dlp，比 curl 更稳定：

```bash
yt-dlp --extract-audio --audio-format mp3 -o "C:/tmp/bili_audio.%(ext)s" "https://www.bilibili.com/video/BVID"
```

输出文件为 `C:/tmp/bili_audio.mp3`。

如果没有 yt-dlp，用 curl 下载音频流（需先从 `window.__playinfo__.data.dash.audio[0].baseUrl` 获取 URL）：

```bash
curl -L -o "C:/tmp/bili_audio.m4s" \
  -H "Referer: https://www.bilibili.com/" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  "AUDIO_URL"
```

### 第四步：Whisper 转录

```bash
python -m whisper "C:/tmp/bili_audio.mp3" \
  --model small \
  --language zh \
  --output_format txt \
  --output_dir "C:/tmp/"
```

转录结果在 `C:/tmp/bili_audio.txt`（UTF-8 编码）。

### 第五步：格式化文本（加标点和段落）

**Windows 编码陷阱（两个）：**
1. 不能用 `>` 重定向 stdout，Windows 会用 GBK 写文件
2. 不能通过 bash 参数传中文路径/标题，bash 会用 GBK 编码参数，Python 收到后解码出 `�` 替换字符，写进文件名和内容里

**关键：Haiku 模型默认返回 `ThinkingBlock + TextBlock`，必须传 `thinking={'type': 'disabled'}` 并用以下方式提取文本：**
```python
msg = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=8192,
    thinking={'type': 'disabled'},  # 必须禁用思考模型
    messages=[{"role": "user", "content": f"..."}]
)
text = next((block.text for block in msg.content if block.type == 'text'), '')
```

**语言自动检测：文本前500字符若大部分是ASCII且空格多，判断为英文，用不同的提示词。**

**长文本分段：超过4000字符的内容需要分 chunk 处理（每3500字符一段），各段分别格式化后再合并。**

保存以下脚本到 `C:/tmp/format_transcript.py`（用 Python 写文件，不传中文参数）：

```python
import anthropic, sys, os

# argv[1]: 转录txt路径（ASCII路径）
# argv[2]: 输出目录（ASCII路径，可选，默认桌面）
# 标题从转录文件第一行读取（# 开头），或用文件名
input_path = sys.argv[1]
out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser('~/Desktop/B站视频转录')
os.makedirs(out_dir, exist_ok=True)

raw = open(input_path, encoding='utf-8-sig', errors='replace').read()

# 从内容第一行提取标题（格式化脚本写入的 # 标题行）
title = ''
for line in raw.splitlines():
    if line.startswith('# '):
        title = line[2:].strip()
        break
if not title:
    title = os.path.splitext(os.path.basename(input_path))[0]

client = anthropic.Anthropic()
msg = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=8192,
    messages=[{
        "role": "user",
        "content": f"以下是中文语音识别文本，每行是一句话但缺少标点符号和段落结构。请帮我：1）加上标点符号；2）合并相关的句子成段落；3）保持原意，不增删内容。直接输出格式化后的文本，不要加任何说明：\n\n{raw}"
    }]
)

# 用 Python 直接写文件，标题来自内容而非 bash 参数
out_path = os.path.join(out_dir, title + '.txt')
open(out_path, 'w', encoding='utf-8-sig').write(f'# {title}\n\n' + msg.content[0].text)
print(f"Saved to {out_path}")
```

运行（只传 ASCII 路径，不传中文）：

```bash
python C:/tmp/format_transcript.py C:/tmp/bili_audio.txt "C:/Users/clown/Desktop/B站视频转录"
```

如果没有 Anthropic API key，备选方案：

```bash
# 用 ollama（如果已安装）
ollama run qwen2.5:7b "给以下中文语音识别文本加标点和段落，不改动内容：$(cat C:/tmp/bili_audio.txt)"
```

### 第六步：保存到目标路径（文件内含视频链接）

**文件名规则：使用视频标题，去掉 Windows 文件名非法字符（`/\:*?"<>|`），下划线替代。**

输出目录：`C:/Users/clown/Desktop/B站视频转录/`

```python
import os, shutil

title = title.replace('/', '_').replace('\\', '_').replace(':', '_')
title = title.replace('*', '_').replace('?', '_').replace('"', '_')
title = title.replace('<', '_').replace('>', '_').replace('|', '_')

out_path = os.path.join('C:/Users/clown/Desktop/B站视频转录/', title + '.txt')
with open(out_path, 'w', encoding='utf-8-sig') as f:
    f.write(out_content)  # 内容包含 # 标题 + 链接 + 正文
```

文件内容必须包含原文链接。

## 输出文件内容格式

```
# 视频标题

原文链接：https://www.bilibili.com/video/BV号

[格式化后的正文]
```

**注意：文件内必须包含视频链接，方便后续引用。**

## 注意事项

- Whisper `small` 模型对中文效果较好，`base` 更快但质量差
- yt-dlp 比 curl 更稳定，优先使用
- B站 AI 字幕需要登录才能访问，未登录时 `subtitles` 为空数组
- **Windows 编码陷阱1**：不能用 `>` 重定向，必须在 Python 内用 `open(..., encoding='utf-8-sig').write()` 写文件
- **Windows 编码陷阱2**：不能通过 bash 参数传中文字符串（标题、路径），bash 用 GBK 编码参数，Python 解码后得到 `�` 替换字符，写进文件名和内容里永久损坏
- 格式化后用 `python -c "print(open(path, encoding='utf-8-sig').read()[:200])"` 验证内容正常

## 常见问题

**Whisper 报错 `No module named whisper`**
```bash
pip install openai-whisper
```

**格式化文件乱码 / 文件名出现 `?` 或方块字**
- 原因1：用了 `>` 重定向，Windows 以 GBK 写文件
- 原因2：通过 bash 参数传了中文标题/路径（这批文件已损坏，需重新转录）
- 修复：改用新版脚本，只传 ASCII 路径，标题从文件内容自动提取

**`No module named anthropic`**
```bash
pip install anthropic
```

**格式化结果不理想**
- 分段处理长文本（每次 2000 字以内）
