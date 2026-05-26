---
name: vibes_skills
description: AI-powered code generation tools with GUI and CLI interfaces
---

# vibes_skills

这是一个基于 Claude API 的代码生成工具集，提供多种方式来生成代码。

## When to use

当用户需要：
- 使用 AI 生成代码
- 通过图形界面或命令行生成代码
- 批量处理代码生成任务
- OCR 文本对比功能

## Available Tools

### 1. code_generator.py - 命令行代码生成器
终端直接生成代码，无需修改代码。

使用方法：
```bash
cd D:\vibes_skills
.venv\Scripts\python.exe code_generator.py "你的代码需求"
```

### 2. ai_code_gui.py - 图形界面代码生成器
双击即用的 GUI 界面，适合非技术用户。

使用方法：
```bash
cd D:\vibes_skills
.venv\Scripts\python.exe ai_code_gui.py
```
或直接运行 `启动GUI.bat`

### 3. claude_code_skill.py - 技能类封装
提供 Pydantic 模型封装的异步代码生成接口。

### 4. ocr_text_compare - OCR 文本对比工具
位于 `ocr_text_compare/` 子目录

## Instructions

1. 确保虚拟环境已激活：`D:\vibes_skills\.venv`
2. 根据需求选择合适的工具
3. 命令行工具适合自动化脚本
4. GUI 工具适合交互式使用
5. 所有工具共享相同的 Claude API 配置

## Configuration

工具使用 Claude API，配置位于各脚本顶部：
- API Key: 需要有效的 Claude API 密钥
- Base URL: API 中转地址
- Model: claude-opus-4-6

## Dependencies

- Python 3.x
- pydantic
- requests
- tkinter (GUI 版本)
