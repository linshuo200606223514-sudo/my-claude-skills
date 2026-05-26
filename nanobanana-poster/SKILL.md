---
name: nanobanana-poster
description: "用 NanoBanana AI 生成海报图片。Use when user wants to generate poster, 生成海报, 生成图片, AI作图, 小红书海报, 营销海报 via NanoBanana image generation API."
---

# NanoBanana 海报生成

## 概述

NanoBanana 是 OpenAI 兼容格式的图片生成 API。返回 base64 编码的图片，**必须用 curl + Python 组合**（Python 直接调用 SSL 会挂起）。

## 关键参数

| 参数 | 值 |
|------|-----|
| base_url | `https://api.penguinsaichat.dpdns.org/v1` |
| model | `nano-banana-pro`（最高质量）/ `nano-banana-fast`（更快）/ `nano-banana-2` |
| API Key | `sk-0ZGqtMogf99v8nShOTAoWfEYfg35pOXrnRxggjX3nFIUS5H0` |
| endpoint | `/v1/chat/completions`（OpenAI chat 格式，prompt 放在 user message） |
| 响应格式 | `![image](data:image/png;base64,...)` markdown 格式 |

## 工作流程

### 第一步：构建 prompt

根据用户需求写英文 prompt（英文效果更好），包含：
- 尺寸比例（如 `2:3 portrait ratio`、`1:1 square`、`16:9 landscape`）
- 风格描述（如 `luxury magazine editorial`、`minimalist`）
- 颜色方案（用十六进制色值）
- 布局结构（从上到下描述各区域）
- 文字内容（中文文字直接写入 prompt）

**小红书海报标准 prompt 模板：**
```
Create a [THEME] Xiaohongshu poster in 2:3 portrait ratio (1080x1620px).
Color palette: [BACKGROUND], [PRIMARY], [ACCENT].
Layout top to bottom:
1) [TOP ELEMENT - e.g. decorative petals/pattern]
2) [MAIN TITLE in Chinese: '标题文字'] in [FONT STYLE] font, centered
3) [SUBTITLE in Chinese: '副标题'] in [COLOR]
4) [PRODUCT/IMAGE ELEMENT]
5) [TAGLINE: '标语文字']
6) [CTA BUTTON: '按钮文字'] in [COLOR]
Style: [AESTHETIC DESCRIPTION], generous whitespace, [BORDER/DECORATION].
```

### 第二步：写请求脚本到 C:/tmp/

将以下脚本保存为 `C:/tmp/gen_poster.py`，**prompt 中的中文必须用 Python 字符串，不能在 shell 里传参**：

```python
import json, subprocess, base64, datetime, os

prompt = "YOUR PROMPT HERE"  # 在 Python 里写 prompt，支持中文

url = "https://api.penguinsaichat.dpdns.org/v1/chat/completions"
key = "sk-0ZGqtMogf99v8nShOTAoWfEYfg35pOXrnRxggjX3nFIUS5H0"

body = json.dumps({
    "model": "nano-banana-pro",
    "messages": [{"role": "user", "content": prompt}]
})

# 写到文件，用 --data-binary @file 避免 shell 转义问题
with open("C:/tmp/nb_req.json", "w", encoding="utf-8") as f:
    f.write(body)

print("Generating...", flush=True)
result = subprocess.run(
    ["curl", "-s", "--max-time", "180", "-X", "POST", url,
     "-H", f"Authorization: Bearer {key}",
     "-H", "Content-Type: application/json",
     "--data-binary", "@C:/tmp/nb_req.json",
     "-o", "C:/tmp/nb_resp.json"],
    capture_output=True, text=True, timeout=200
)
print(f"curl exit: {result.returncode}", flush=True)

sz = os.path.getsize("C:/tmp/nb_resp.json")
print(f"Response: {sz} bytes", flush=True)

with open("C:/tmp/nb_resp.json", "r", encoding="utf-8") as f:
    data = json.load(f)

if "error" in data:
    print(f"API Error: {data['error']}")
    exit(1)

content = data["choices"][0]["message"]["content"]
print(f"Content: {len(content)} chars", flush=True)

# 提取 base64（兼容多种响应格式）
import re as _re
b64 = None
if isinstance(content, list):
    # Gemini 风格：list of parts
    for part in content:
        if isinstance(part, dict):
            if part.get("type") == "image_url":
                url_val = part["image_url"]["url"]
                if "base64," in url_val:
                    b64 = url_val.split("base64,", 1)[1]
                    break
            elif part.get("type") == "image" and "data" in part:
                b64 = part["data"]; break
elif isinstance(content, str):
    m = _re.search(r"base64,([A-Za-z0-9+/=]+)", content)
    if m:
        b64 = m.group(1)
    else:
        b64 = content.strip()

if not b64:
    print("ERROR: no image data in response"); exit(1)

img_bytes = base64.b64decode(b64)
ext = "png" if img_bytes[:4] == b'\x89PNG' else "jpg" if img_bytes[:2] == b'\xff\xd8' else "webp"
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
out = f"OUTPUT_PATH_{ts}.{ext}"  # 替换为实际输出路径
with open(out, "wb") as f:
    f.write(img_bytes)
print(f"Saved: {out} ({len(img_bytes)} bytes)", flush=True)
```

### 第三步：运行

```bash
py "C:/tmp/gen_poster.py"
```

生成耗时约 30-60 秒，响应体约 1-2MB。

### 第四步：验证尺寸

```bash
py -c "from PIL import Image; img=Image.open('OUTPUT.png'); print(img.size)"
```

## 常见比例对应描述

| 用途 | 比例 | Prompt 描述 |
|------|------|-------------|
| 小红书封面 | 2:3 | `2:3 portrait ratio (1080x1620px)` |
| 朋友圈/方图 | 1:1 | `1:1 square format (1080x1080px)` |
| 横版Banner | 16:9 | `16:9 landscape (1920x1080px)` |
| 手机壁纸 | 9:16 | `9:16 full-screen portrait (1080x1920px)` |

## 注意事项

- **不能用 Python 直接发 HTTPS 请求**（SSL 会挂起），必须通过 `subprocess` 调用 `curl`
- **不能在 shell 里传含中文的参数**，中文 prompt 必须写在 Python 脚本里
- **请求体必须写到文件**再用 `--data-binary @file`，避免 shell 转义破坏 JSON
- 响应是 markdown 格式 `![image](data:image/png;base64,...)` 需要解析提取 base64
- 图片格式自动检测：PNG 魔数 `\x89PNG`，JPEG 魔数 `\xff\xd8`

## 常见问题

**`curl exit: 0` 但 response 是 error**
- 检查 JSON body 格式，通常是 shell 转义导致 JSON 损坏
- 改用 `--data-binary @file` 方式

**图片比例不准确**
- NanoBanana 不支持精确像素控制，prompt 里写比例描述（如 `2:3 portrait`）
- 实际输出会接近但不完全等于目标比例，属正常现象

**生成内容不符合预期**
- 用英文 prompt，中文文字内容直接嵌入（如 `title text '她也值得'`）
- 增加更多视觉细节描述（颜色、字体风格、布局位置）
- 换用 `nano-banana-2` 模型尝试不同风格
