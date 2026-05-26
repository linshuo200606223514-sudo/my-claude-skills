---
name: bilibili-classifier
description: "将B站视频文案txt文件按主题自动分类到子文件夹。Use when user wants to 分类B站文案, 整理视频文稿, classify bilibili transcripts by topic."
---

# B站文案自动分类

将一个文件夹内的B站视频文案 `.txt` 文件，根据标题内容自动分类到主题子文件夹中。

## 使用方式

用户提供：
- **源文件夹**：包含 `.txt` 文案文件的目录
- **目标文件夹**：分类后的输出目录（不存在则自动创建）

## 工作流程

### 第一步：读取所有文件名

用 Bash 列出源文件夹所有 `.txt` 文件：

```bash
ls "源文件夹路径"
```

### 第二步：分析标题，制定分类方案

根据文件名（即视频标题）分析内容主题，制定分类方案。常见分类参考：

| 分类名 | 关键词 |
|--------|--------|
| AI编程与Vibe-Coding | Vibe Coding、全自动开发、AI编程、Agent协作、框架 |
| Claude-Code专题 | Claude Code、Claude skills、RAG知识管理 |
| AI工具与效率 | 神器推荐、效率、知识库、技能、开源工具 |
| AI图像与视频创作 | Blender、建模、图像生成、视频剪辑、提示词 |
| AI模型与前沿 | 新模型、GPT、Claude Opus、Anthropic、GLM |
| 创业与一人公司 | 一人公司、复盘、被动收入、数字游民 |
| 自媒体与内容创作 | B站、起号、内容、播放量、选题 |
| 学习方法 | 学习、入门到精通、教程、指南、养成计划 |

根据实际文件内容灵活调整分类，不必拘泥于上表。

### 第三步：执行分类（Python脚本）

用 `C:/Users/clown/AppData/Local/Python/bin/python.exe` 执行以下脚本：

```python
import os
import shutil

# 根据第二步分析结果填写
categories = {
    "分类名1": ["前缀1_", "前缀2_"],
    "分类名2": ["前缀3_"],
    # ...
}

src = r"源文件夹路径"
dst = r"目标文件夹路径"

os.makedirs(dst, exist_ok=True)
categorized = set()

for category, prefixes in categories.items():
    cat_dir = os.path.join(dst, category)
    os.makedirs(cat_dir, exist_ok=True)
    for filename in os.listdir(src):
        if not filename.endswith(".txt"):
            continue
        for prefix in prefixes:
            if filename.startswith(prefix):
                shutil.copy2(os.path.join(src, filename), os.path.join(cat_dir, filename))
                categorized.add(filename)
                print(f"[{category}] {filename}")
                break

all_files = [f for f in os.listdir(src) if f.endswith(".txt")]
uncategorized = [f for f in all_files if f not in categorized]
print(f"\n已分类: {len(categorized)} 个")
if uncategorized:
    print(f"未分类: {uncategorized}")
else:
    print("所有文件已分类完毕")
```

### 第四步：处理未分类文件

如果有未分类文件，将其放入 `其他` 子文件夹，或根据内容补充到合适分类。

### 第五步：汇报结果

告知用户：
- 创建了哪些分类文件夹
- 每个文件夹包含多少文件
- 是否有未分类文件

## 注意事项

- 文件是**复制**（`shutil.copy2`），不是移动，源文件夹保持不变
- 如果文件名没有数字前缀，改用关键词匹配文件名
- Python路径：`C:/Users/clown/AppData/Local/Python/bin/python.exe`
