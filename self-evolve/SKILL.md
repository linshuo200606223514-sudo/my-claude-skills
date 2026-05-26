---
name: self-evolve
description: "Browse websites and docs to learn new knowledge, auto-generate skills, and update the knowledge base. Use when: user wants to learn a new technology, browse docs, generate a skill from documentation, update knowledge, crawl a website, or says 'self-evolve'. Capabilities: Playwright MCP browsing, knowledge extraction, skill generation, memory updates."
allowed-tools:
  - mcp__playwright__browser_navigate
  - mcp__playwright__browser_snapshot
  - mcp__playwright__browser_click
  - mcp__playwright__browser_type
  - mcp__playwright__browser_tab_list
  - mcp__playwright__browser_tab_new
  - mcp__playwright__browser_tab_close
  - Write
  - Read
  - Edit
  - Bash
  - WebSearch
  - WebFetch
  - Agent
argument-hint: "[url-or-topic]"
---

# Self-Evolve: Claude 自我进化工具

让 Claude 通过浏览网页自主学习新知识、生成新技能、持续更新知识库。

## 运行模式

### 交互模式（本技能）
在对话中直接用 Playwright MCP 浏览、提取、学习。

### 批量模式
运行 `python C:/Users/clown/self-evolve/evolve.py` 进行批量爬取。

---

## 工作流程

### 当收到 URL 时

1. **导航到页面**
   - 使用 `mcp__playwright__browser_navigate` 打开 URL
   - 等待页面加载完成

2. **获取页面快照**
   - 使用 `mcp__playwright__browser_snapshot` 获取页面结构化内容
   - 如果页面有侧边栏导航，记录子页面链接

3. **提取关键知识**
   从页面内容中提取：
   - 核心概念和定义
   - API 模式和用法
   - 代码示例（完整可运行的）
   - 常见陷阱和注意事项
   - 最佳实践

4. **决定存储方式**
   - 如果是通用知识片段 → 写入 MEMORY.md 的 `## Learned Knowledge` 区域
   - 如果是完整技术文档（足够生成技能）→ 生成新 SKILL.md
   - 如果内容很多 → 写入 `C:/Users/clown/self-evolve/knowledge/<topic>.md` 详细文件，MEMORY.md 只放摘要和链接

5. **深度学习（可选）**
   如果文档站有多个页面，依次点击侧边栏链接继续学习，每个页面重复步骤 2-4。

### 当收到主题关键词时

1. 先用 `WebSearch` 搜索该主题的官方文档
2. 从搜索结果中选择最权威的 URL
3. 按上述 URL 流程执行

---

## 知识存储规范

### MEMORY.md 格式

在 `C:/Users/clown/.claude/projects/C--Users-clown/memory/MEMORY.md` 的 `## Learned Knowledge` 区域追加：

```markdown
## Learned Knowledge

### <主题名> (learned: YYYY-MM-DD)
- **来源**: <URL>
- **摘要**: 一句话总结
- **关键点**: 3-5 个要点
- **详细文件**: [<topic>.md](C:/Users/clown/self-evolve/knowledge/<topic>.md)（如有）
```

规则：
- MEMORY.md 总行数不超过 180 行
- 如果快满了，压缩最旧的条目为一行摘要
- 相同 URL 的知识更新而非追加

### 详细知识文件格式

`C:/Users/clown/self-evolve/knowledge/<topic>.md`：

```markdown
# <主题名>

> 来源: <URL>
> 学习日期: YYYY-MM-DD

## 核心概念
...

## API 模式
...

## 代码示例
...

## 注意事项
...
```

---

## 技能生成规范

当学到的知识足够形成一个独立技能时（比如一个框架的完整用法），生成新技能：

1. 创建目录 `C:/Users/clown/.claude/skills/<skill-name>/`
2. 创建 `SKILL.md`，遵循以下规范：

```yaml
---
name: <skill-name>
description: "<What it does>. Use when <trigger phrases>. <Key capabilities>."
---
```

3. 正文包含：使用指南、代码模板、常见模式、注意事项
4. 保持在 500 行以内
5. 如有大量参考资料，放入 `references/` 子目录

---

## 批量模式命令

如果用户需要批量操作，可以运行：

```bash
# 爬取所有配置的源
python C:/Users/clown/self-evolve/evolve.py crawl

# 爬取指定源
python C:/Users/clown/self-evolve/evolve.py crawl --source <name>

# 学习单个页面
python C:/Users/clown/self-evolve/evolve.py learn <url>

# 从文档生成技能
python C:/Users/clown/self-evolve/evolve.py generate-skill <url>

# 查看状态
python C:/Users/clown/self-evolve/evolve.py status
```

配置文件: `C:/Users/clown/self-evolve/config.yaml`

---

## 注意事项

- 每次浏览后都要确认知识已正确写入文件
- 不要在 MEMORY.md 中存储过于细节的内容，详细内容放 knowledge/ 目录
- 生成技能前先检查是否已有类似技能，避免重复
- 爬取时注意频率，页面间至少间隔 2 秒
- 优先提取可直接复用的代码模式和 API 用法
