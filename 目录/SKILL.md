---
name: 目录
description: 记录和查看项目目录。Use when user wants to add project path, list projects, remove project, 记项目, 查项目, 项目在哪.
argument-hint: [add/rm/find] [名称] [路径]
---

# 项目目录管理

注册表: `~/.claude/projects-registry.json`

## 当前已注册项目

!`cat ~/.claude/projects-registry.json 2>/dev/null || echo '(空)'`

## 用法

- `/目录` — 列出所有项目
- `/目录 add <名称> <路径> [描述]` — 添加项目
- `/目录 rm <名称>` — 删除项目
- `/目录 find <关键词>` — 搜索项目

## 执行规则

1. 读取 `~/.claude/projects-registry.json`，不存在则创建 `{"projects":[]}`
2. 执行对应操作，写回文件
3. add 时用 `ls` 验证路径是否存在，不存在则警告但仍添加
4. 路径统一用正斜杠存储
5. 输出用中文，简洁展示表格
