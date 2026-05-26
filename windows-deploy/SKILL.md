---
name: windows-deploy
description: 为客户生成 Windows 部署脚本（安装.bat + install.py + run.bat），规避 BAT 中文编码乱码问题。Use when: 用户要给客户打包 Windows 工具、生成安装脚本、部署 Python 项目到客户电脑。
---

# Windows 客户部署脚本生成

## Trigger

Use when user wants to:
- 给客户生成安装脚本
- 打包 Windows 部署包
- 生成 安装.bat / run.bat
- 客户电脑部署 Python 工具

## 核心规范：BAT 文件编码陷阱

**问题根因**：客户电脑默认代码页 GBK/936，bat 文件保存为 UTF-8 时，`chcp 65001` 执行前中文字节已被错误解析为命令，导致"不是内部或外部命令"报错，整个安装流程崩溃。

**解决方案**：bat 文件只写纯 ASCII，所有安装逻辑移到 `install.py`。

## 标准文件结构

```
项目目录/
├── 安装.bat        ← 纯 ASCII，只调用 install.py
├── install.py      ← 安装逻辑，可用中文 print
├── run.bat         ← 纯 ASCII，只启动主程序
└── python_path.txt ← install.py 自动生成，记录 Python 路径
```

## 标准模板

### 安装.bat（纯 ASCII）

```bat
@echo off
where python >nul 2>&1
if not errorlevel 1 (
    python "%~dp0install.py"
    pause
    exit /b
)
echo [ERROR] Python not found. Please install Python 3.10+ from https://www.python.org/downloads/
pause
```

### install.py

```python
import subprocess
import sys
import os

def find_python():
    candidates = [
        os.path.expandvars(r"%LOCALAPPDATA%\Python\bin\python.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Python\Python312\python.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Python\Python311\python.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Python\Python310\python.exe"),
        r"C:\Python312\python.exe",
        r"C:\Python311\python.exe",
        r"C:\Python310\python.exe",
        r"C:\Program Files\Python312\python.exe",
        r"C:\Program Files\Python311\python.exe",
        r"C:\Program Files\Python310\python.exe",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return sys.executable

def main():
    print("========================================")
    print("  正在安装依赖...")
    print("========================================")

    python = find_python()
    print(f"[OK] Python: {python}")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "python_path.txt"), "w") as f:
        f.write(python)

    # 根据项目修改此列表
    packages = ["requests", "playwright"]
    print("[安装] pip 包...")
    r = subprocess.run([python, "-m", "pip", "install"] + packages + ["-q"])
    if r.returncode != 0:
        print("[错误] 安装失败，请检查网络连接")
        input("按任意键退出...")
        sys.exit(1)

    # 如需安装浏览器，取消注释：
    # subprocess.run([python, "-m", "playwright", "install", "chromium"])

    print()
    print("========================================")
    print("  安装完成！双击 run.bat 启动")
    print("========================================")
    input("按任意键退出...")

if __name__ == "__main__":
    main()
```

### run.bat（纯 ASCII）

```bat
@echo off
set PYTHON=
if exist "%~dp0python_path.txt" set /p PYTHON=<"%~dp0python_path.txt"
if not exist "%PYTHON%" set PYTHON=

if "%PYTHON%"=="" (
    for %%p in (
        "%LOCALAPPDATA%\Python\bin\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
        "C:\Program Files\Python312\python.exe"
        "C:\Program Files\Python311\python.exe"
        "C:\Program Files\Python310\python.exe"
    ) do (
        if exist %%p set PYTHON=%%p
    )
)
if "%PYTHON%"=="" set PYTHON=python

%PYTHON% "%~dp0main.py"
pause
```

## 检查清单

生成脚本后必须验证：

- [ ] `安装.bat` 和 `run.bat` 中无任何中文字符（包括注释）
- [ ] bat 文件末尾有 `pause`，防止闪退
- [ ] `install.py` 已包含在打包文件中
- [ ] `install.py` 的 `packages` 列表已按项目实际需求修改
- [ ] 如用 playwright，已加 `playwright install chromium` 步骤

## 常见 WARNING 说明

安装时出现以下 WARNING 属正常，不影响运行：
```
WARNING: The script xxx.exe is installed in '...\Scripts' which is not on PATH.
```
原因：pip 把可执行文件装到 Scripts 目录，但该目录未加入 PATH。Python 脚本直接调用库不依赖 PATH，忽略即可。
