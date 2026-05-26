---
name: A
description: "截图 OCR 识别。Use when user says /A, 看看截图, 看看图, OCR, 识别, 看图, what's in screenshot."
---

# 截图 OCR 识别

## 功能

自动识别 Windows 最新截图中的文字，无需任何参数。

## 使用方法

用户只需说：
- **"看看截图"**
- **"看看图"**
- **"OCR"**
- **"识别"**
- **"看图"**

## 工作流程

### 自动执行

1. 获取最新截图路径
   ```
   C:\Users\clown\Pictures\Screenshots\
   ```

2. 调用 OCR API 识别

3. 输出识别结果

## 实现命令

```python
import os
import requests

screenshot_dir = r"C:\Users\clown\Pictures\Screenshots"
files = [os.path.join(screenshot_dir, f) for f in os.listdir(screenshot_dir)
         if os.path.splitext(f)[1].lower() in ['.png', '.jpg', '.jpeg', '.bmp']]
filepath = max(files, key=os.path.getmtime)

with open(filepath, "rb") as f:
    resp = requests.post("http://localhost:5000/ocr/file", files={"image": f}, timeout=30)
result = resp.json()
print(result["text"] if result.get("success") else f"Error: {result.get('error')}")
```

## 故障排除

**OCR 服务未运行？**
```bash
cd C:\Users\clown\.worktrees\listening-miniprogram
python tesseract_server.py
```

**检查服务状态：**
```bash
curl http://localhost:5000/health
```