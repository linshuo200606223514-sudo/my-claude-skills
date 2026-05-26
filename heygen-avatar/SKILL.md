---
name: heygen-avatar
description: "HeyGen数字人视频生成API。Use when: 用户要用HeyGen生成数字人视频、调用HeyGen API、创建avatar视频、TTS配音、查询视频状态。Capabilities: 列出avatar/voice、生成视频、轮询状态、下载视频。"
---

# HeyGen Avatar API

> 来源: https://docs.heygen.com
> 学习日期: 2026-04-05

## 认证

所有请求头加 `X-Api-Key`。API Key 在 HeyGen 控制台 Settings → API → API token 获取。

```python
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": "YOUR_API_KEY"
}
```

## 核心端点

| 功能 | 方法 | 端点 |
|------|------|------|
| 列出所有Avatar | GET | `https://api.heygen.com/v2/avatars` |
| 列出所有Voice | GET | `https://api.heygen.com/v2/voices` |
| 生成视频 | POST | `https://api.heygen.com/v2/video/generate` |
| 查询视频状态 | GET | `https://api.heygen.com/v1/video_status.get?video_id={id}` |
| 生成模板视频 | POST | `https://api.heygen.com/v2/template/{template_id}/generate` |

## 生成视频请求体

```json
{
  "video_inputs": [
    {
      "character": {
        "type": "avatar",
        "avatar_id": "Jocelyn_sitting_sofa_front",
        "avatar_style": "normal",
        "scale": 1,
        "offset": { "x": 0, "y": 0 }
      },
      "voice": {
        "type": "text",
        "input_text": "你好，欢迎使用HeyGen数字人。",
        "voice_id": "00c8fd447ad7480ab1785825978a22b4",
        "speed": 1.0
      },
      "background": {
        "type": "color",
        "value": "#FFFFFF"
      }
    }
  ],
  "dimension": {
    "width": 1280,
    "height": 720
  },
  "caption": false,
  "title": "我的数字人视频"
}
```

## 完整 Python 示例

```python
import requests
import time

API_KEY = "YOUR_API_KEY"
BASE_URL = "https://api.heygen.com"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": API_KEY
}

# 1. 列出可用 Avatar
def list_avatars():
    r = requests.get(f"{BASE_URL}/v2/avatars", headers=headers)
    data = r.json()
    for a in data["data"]["avatars"]:
        print(a["avatar_id"], a["avatar_name"])

# 2. 列出可用 Voice
def list_voices():
    r = requests.get(f"{BASE_URL}/v2/voices", headers=headers)
    data = r.json()
    for v in data["data"]["voices"]:
        print(v["voice_id"], v["name"], v["language"])

# 3. 生成视频
def generate_video(avatar_id, voice_id, text):
    payload = {
        "video_inputs": [{
            "character": {
                "type": "avatar",
                "avatar_id": avatar_id,
                "avatar_style": "normal"
            },
            "voice": {
                "type": "text",
                "input_text": text,
                "voice_id": voice_id,
                "speed": 1.0
            },
            "background": {
                "type": "color",
                "value": "#FFFFFF"
            }
        }],
        "dimension": {"width": 1280, "height": 720},
        "caption": False
    }
    r = requests.post(f"{BASE_URL}/v2/video/generate", json=payload, headers=headers)
    result = r.json()
    return result["data"]["video_id"]

# 4. 轮询视频状态直到完成
def wait_for_video(video_id, timeout=300):
    start = time.time()
    while time.time() - start < timeout:
        r = requests.get(
            f"{BASE_URL}/v1/video_status.get",
            params={"video_id": video_id},
            headers=headers
        )
        data = r.json()["data"]
        status = data["status"]
        print(f"状态: {status}")
        if status == "completed":
            return data["video_url"]
        elif status == "failed":
            raise Exception(f"视频生成失败: {data.get('error')}")
        time.sleep(5)
    raise TimeoutError("视频生成超时")

# 使用示例
if __name__ == "__main__":
    # list_avatars()
    # list_voices()
    video_id = generate_video(
        avatar_id="Jocelyn_sitting_sofa_front",
        voice_id="00c8fd447ad7480ab1785825978a22b4",
        text="大家好，我是你的AI助手。"
    )
    print(f"视频ID: {video_id}")
    url = wait_for_video(video_id)
    print(f"视频下载链接: {url}")
```

## Talking Photo（照片说话）

用一张照片生成说话视频，`type` 改为 `talking_photo`：

```json
{
  "character": {
    "type": "talking_photo",
    "talking_photo_id": "YOUR_PHOTO_ID"
  },
  "voice": {
    "type": "text",
    "input_text": "文字内容",
    "voice_id": "VOICE_ID",
    "emotion": "Friendly"
  }
}
```

## 视频状态值

| 状态 | 含义 |
|------|------|
| `pending` | 排队中 |
| `processing` | 生成中 |
| `completed` | 完成，有 `video_url` |
| `failed` | 失败，有 `error` 信息 |

## 背景类型

```json
// 纯色
{"type": "color", "value": "#FFFFFF"}

// 图片URL
{"type": "image", "url": "https://..."}

// 视频URL
{"type": "video", "url": "https://..."}
```

## 注意事项

- 视频生成是异步的，需轮询状态，通常需要 30秒~5分钟
- `video_url` 有效期有限，生成后尽快下载
- 免费账号有配额限制，测试时用 `"test": true` 字段（不消耗配额但有水印）
- 中文 TTS 需选择支持中文的 voice_id
- `avatar_id` 区分大小写，从 list_avatars 接口获取准确值
