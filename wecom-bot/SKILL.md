---
name: wecom-bot
description: |
  企业微信消息发送工具。支持群机器人 Webhook（最简单，发到群聊）和自建应用 API（发给指定员工/部门）。
  Use when user wants to 发消息到企业微信, 发企业微信通知, 企业微信机器人, WeCom, WeChat Work bot, send message to WeCom group.
metadata:
  author: clown
  version: "1.0"
---

# 企业微信消息发送

两种接入方式，根据需求选择：

```
需求判断
├─ 发通知到群聊？         → 方式一：Webhook 机器人（最简单，5分钟搞定）
├─ 发消息给指定员工/部门？ → 方式二：自建应用 API
└─ 不确定？               → 先问用户有没有群机器人的 Webhook 地址
```

---

## 方式一：群机器人 Webhook

### 获取 Webhook 地址

```
企业微信群聊 → 右上角「···」→ 添加机器人 → 新建机器人 → 复制 Webhook 地址
```

Webhook 格式：
```
https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

**频率限制**：20条/分钟，2000条/天

### 发送代码

直接用 Python 内联执行，无需额外依赖（只用标准库）：

```python
import urllib.request, json

WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=你的KEY"

def wecom_send(payload: dict) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(WEBHOOK, data=data, method="POST")
    req.add_header("Content-Type", "application/json; charset=utf-8")
    resp = urllib.request.urlopen(req, timeout=10)
    result = json.loads(resp.read())
    if result.get("errcode") != 0:
        raise Exception(f"发送失败: {result}")
    return result

# ── 文本消息（@所有人）──
wecom_send({
    "msgtype": "text",
    "text": {
        "content": "服务器告警！磁盘已满 🚨",
        "mentioned_list": ["@all"]   # 或 ["zhangsan", "lisi"]
    }
})

# ── Markdown 消息（支持表格、颜色）──
wecom_send({
    "msgtype": "markdown",
    "markdown": {"content": """## 📊 系统监控
| 指标 | 数值 | 状态 |
|------|------|------|
| CPU  | 45%  | <font color="info">正常</font> |
| 内存 | 78%  | <font color="warning">偏高</font> |
| 磁盘 | 92%  | <font color="warning">告警</font> |

**处理建议：** 请立即清理磁盘！"""}
})

# ── 图文卡片（带链接）──
wecom_send({
    "msgtype": "news",
    "news": {"articles": [{
        "title": "系统维护公告",
        "description": "今晚 22:00-24:00 系统维护，请提前保存工作",
        "url": "https://example.com/notice",
        "picurl": "https://example.com/banner.png"   # 可选封面图
    }]}
})
```

### Markdown 颜色语法

```markdown
<font color="info">蓝色</font>      # 信息/正常
<font color="warning">橙色</font>   # 警告/偏高
<font color="comment">灰色</font>   # 注释/次要信息
```

### 发送图片（base64）

```python
import base64, hashlib, urllib.request, json

def wecom_send_image(webhook_url: str, image_path: str):
    with open(image_path, "rb") as f:
        img_data = f.read()
    payload = {
        "msgtype": "image",
        "image": {
            "base64": base64.b64encode(img_data).decode("utf-8"),
            "md5": hashlib.md5(img_data).hexdigest()
        }
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    return json.loads(urllib.request.urlopen(req, timeout=10).read())
```

### 发送文件

```python
import urllib.request, os, json

def wecom_upload_and_send_file(webhook_url: str, file_path: str):
    key = webhook_url.split("key=")[1]
    upload_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=file"
    filename = os.path.basename(file_path)
    boundary = "----FormBoundary7MA4YWxkTrZu0gW"
    with open(file_path, "rb") as f:
        file_data = f.read()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'
        f"Content-Type: application/octet-stream\r\n\r\n"
    ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(upload_url, data=body, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    result = json.loads(urllib.request.urlopen(req, timeout=30).read())
    if result.get("errcode") != 0:
        raise Exception(f"上传失败: {result}")
    media_id = result["media_id"]
    return json.loads(urllib.request.urlopen(
        urllib.request.Request(
            webhook_url,
            data=json.dumps({"msgtype": "file", "file": {"media_id": media_id}}).encode(),
            method="POST",
            headers={"Content-Type": "application/json"}
        ), timeout=10
    ).read())
```

---

## 方式二：自建应用 API

适合：发消息给**指定员工或部门**，比 Webhook 更精准。

### 三个必要凭证

| 凭证 | 获取路径 |
|---|---|
| `corp_id` | 管理后台 → 我的企业 → 企业信息 → 企业ID |
| `corp_secret` | **手机端**企业微信 APP → 工作台 → 应用 → 「···」→「查看Secret」|
| `agent_id` | 管理后台 → 应用管理 → 自建应用详情页 |

> ⚠️ `corp_secret` 必须在**手机端**查看，网页后台 2024 年起不再显示。

> ⚠️ 必须在管理后台「应用详情 → 开发者接口 → 企业可信IP」添加服务器公网 IP，否则报 `60020`。

### 完整实现

```python
import urllib.request, json, time, threading
from typing import Optional

class WeComApp:
    """企业微信自建应用 API 客户端，内置 token 缓存（线程安全）"""

    BASE = "https://qyapi.weixin.qq.com/cgi-bin"

    def __init__(self, corp_id: str, corp_secret: str, agent_id: int):
        self.corp_id = corp_id
        self.corp_secret = corp_secret
        self.agent_id = agent_id
        self._token: Optional[str] = None
        self._expires_at: float = 0
        self._lock = threading.Lock()

    # ── Token 管理（提前5分钟刷新）──
    def token(self, force=False) -> str:
        with self._lock:
            if not force and self._token and time.time() < self._expires_at - 300:
                return self._token
            url = f"{self.BASE}/gettoken?corpid={self.corp_id}&corpsecret={self.corp_secret}"
            r = json.loads(urllib.request.urlopen(url, timeout=10).read())
            if r.get("errcode") != 0:
                raise Exception(f"获取 token 失败: {r}")
            self._token = r["access_token"]
            self._expires_at = time.time() + r.get("expires_in", 7200)
            return self._token

    def _post(self, path: str, payload: dict) -> dict:
        url = f"{self.BASE}{path}?access_token={self.token()}"
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/json; charset=utf-8")
        r = json.loads(urllib.request.urlopen(req, timeout=10).read())
        if r.get("errcode") == 42001:  # token 过期，自动重试
            url = f"{self.BASE}{path}?access_token={self.token(force=True)}"
            r = json.loads(urllib.request.urlopen(
                urllib.request.Request(url, data=data, method="POST",
                                       headers={"Content-Type": "application/json"}),
                timeout=10).read())
        if r.get("errcode") != 0:
            raise Exception(f"API 失败: errcode={r.get('errcode')}, errmsg={r.get('errmsg')}")
        return r

    def _base_msg(self, msgtype, touser="@all", toparty="", totag=""):
        return {"touser": touser, "toparty": toparty, "totag": totag,
                "msgtype": msgtype, "agentid": self.agent_id, "safe": 0}

    # ── 发文本 ──
    def send_text(self, content: str, touser="@all", toparty="", totag=""):
        msg = self._base_msg("text", touser, toparty, totag)
        msg["text"] = {"content": content}
        return self._post("/message/send", msg)

    # ── 发 Markdown ──
    def send_markdown(self, content: str, touser="@all", toparty="", totag=""):
        msg = self._base_msg("markdown", touser, toparty, totag)
        msg["markdown"] = {"content": content}
        return self._post("/message/send", msg)

    # ── 发文本卡片 ──
    def send_textcard(self, title: str, description: str, url: str,
                      btntxt="详情", touser="@all"):
        msg = self._base_msg("textcard", touser)
        msg["textcard"] = {"title": title, "description": description,
                           "url": url, "btntxt": btntxt}
        return self._post("/message/send", msg)

    # ── 上传临时素材（返回 media_id，有效期3天）──
    def upload_media(self, file_path: str, media_type="file") -> str:
        import os, mimetypes
        token = self.token()
        upload_url = f"{self.BASE}/media/upload?access_token={token}&type={media_type}"
        filename = os.path.basename(file_path)
        mime = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        boundary = "----FormBoundary7MA4YWxkTrZu0gW"
        with open(file_path, "rb") as f:
            file_data = f.read()
        body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"media\"; "
                f"filename=\"{filename}\"\r\nContent-Type: {mime}\r\n\r\n"
                ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()
        req = urllib.request.Request(upload_url, data=body, method="POST")
        req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
        r = json.loads(urllib.request.urlopen(req, timeout=60).read())
        if r.get("errcode") != 0:
            raise Exception(f"上传失败: {r}")
        return r["media_id"]

    # ── 发文件（自动上传）──
    def send_file(self, file_path: str, touser="@all"):
        media_id = self.upload_media(file_path, "file")
        msg = self._base_msg("file", touser)
        msg["file"] = {"media_id": media_id}
        return self._post("/message/send", msg)

    # ── 发图片（自动上传）──
    def send_image(self, image_path: str, touser="@all"):
        media_id = self.upload_media(image_path, "image")
        msg = self._base_msg("image", touser)
        msg["image"] = {"media_id": media_id}
        return self._post("/message/send", msg)


# ── 使用示例 ──
if __name__ == "__main__":
    app = WeComApp(
        corp_id="ww1234567890abcdef",   # 企业ID
        corp_secret="你的应用Secret",    # 手机端查看
        agent_id=1000001                 # 应用AgentId
    )

    # 发文本给指定人
    app.send_text("🚀 部署完成！", touser="zhangsan|lisi")

    # 发 Markdown 给整个部门（部门ID=2）
    app.send_markdown("""## 📋 发布通知
> 版本：v2.0.0

**更新内容：**
- ✅ 修复登录 Bug
- 🆕 新增批量导出功能""", toparty="2")

    # 发文本卡片（点击跳转链接）
    app.send_textcard(
        title="新工单 #1234",
        description='<div class="gray">2026-03-25 10:00</div>'
                    '<div class="highlight">优先级：高 🔴</div>'
                    '<div class="normal">客户反馈系统无法登录</div>',
        url="https://your-system.com/ticket/1234",
        btntxt="立即处理",
        touser="zhangsan"
    )

    # 发文件给全员
    # app.send_file("./月报.xlsx", touser="@all")
```

---

## 常见错误排查

| 错误码 | 原因 | 解决方案 |
|--------|------|----------|
| `60020` | 服务器 IP 不在白名单 | 管理后台 → 应用详情 → 企业可信IP → 添加 |
| `42001` | access_token 过期 | 代码已内置自动重试，若持续出现检查时钟同步 |
| `45009` | 超出发送频率 | Webhook: 20条/分钟；应用消息: 1条/分钟/用户 |
| `40001` | Secret 无效 | 重新在手机端企业微信 APP 查看并复制 |
| `81013` | 接收者为空 | touser/toparty/totag 至少填一个 |
| `900001` | agentid 不存在 | 检查应用详情页的 AgentId 是否正确 |

## 注意事项

- **无需安装第三方库**：所有代码只用 Python 标准库（`urllib`、`json`、`base64`）
- **token 缓存**：自建应用的 access_token 有效期 2 小时，WeComApp 类已自动缓存和刷新
- **多实例警告**：多台服务器同时运行时，必须用 Redis 等集中缓存 token，否则会互相失效
- **Secret 安全**：`corp_secret` 只在服务端使用，不要写入代码库，用环境变量传入
- **回调响应**：如需接收用户消息，回调接口必须在 5 秒内响应，且 URL 需要 HTTPS
