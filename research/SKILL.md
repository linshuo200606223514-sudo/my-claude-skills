---
name: research
description: |
  深度信息收集与研究分析。Use when: 用户要调研某个话题、收集资料、做竞品分析、了解某技术/产品/事件、说"帮我研究"、"调研一下"、"收集信息"、"做个分析"、"research"。
  工作流: 拆解问题 → 多源搜索 → 深度提取 → 综合分析 → 结构化报告。
  支持: 技术调研、市场分析、竞品对比、新闻事件、学术概念、产品评测。
allowed-tools:
  - WebSearch
  - WebFetch
  - Bash(tvly *)
  - Write
  - Read
argument-hint: "<研究主题或问题>"
---

# Research: 深度信息收集工具

## 工作流程

### 第一步：拆解研究问题

收到主题后，先分析：
- 核心问题是什么？
- 需要哪几个维度的信息？（背景、现状、对比、趋势、评价等）
- 生成 3-5 个具体搜索子查询

### 第二步：多源搜索

优先使用 Tavily（更精准），回退到 WebSearch：

```bash
# 基础搜索
tvly search "查询词" --depth advanced --max-results 8 --json

# 最新动态
tvly search "查询词" --time-range month --topic news --json

# 带完整内容
tvly search "查询词" --include-raw-content --max-results 5 --json

# 指定权威域名
tvly search "查询词" --include-domains github.com,docs.python.org --json
```

如果 `tvly` 不可用，用 `WebSearch` 替代。

### 第三步：深度提取

对搜索结果中最相关的 2-3 个 URL，用 `WebFetch` 获取完整内容：

```
WebFetch(url, "提取关于[主题]的核心信息：定义、特点、用法、优缺点、对比")
```

### 第四步：综合分析

整合所有来源，按以下结构组织：

```
## 核心结论（3句话以内）

## 背景与定义

## 关键发现
- 发现1（来源）
- 发现2（来源）

## 深度分析
（按维度展开）

## 对比/评价（如适用）

## 趋势与展望

## 信息来源
- [标题](URL) — 一句话说明价值
```

### 第五步：保存报告（可选）

如果用户需要保存，写入文件：

```
Write("C:/Users/clown/Desktop/research_<主题>_<日期>.md", 报告内容)
```

---

## 研究类型指南

### 技术调研
- 搜索官方文档、GitHub、技术博客
- 重点：原理、API、性能、生态、坑点
- 域名过滤：`--include-domains github.com,stackoverflow.com`

### 市场/竞品分析
- 搜索产品官网、评测文章、用户反馈
- 重点：功能对比、定价、用户口碑、市场份额
- 时间范围：`--time-range month` 获取最新动态

### 新闻事件
- 搜索新闻源
- 重点：事件经过、多方观点、影响分析
- 参数：`--topic news --time-range week`

### 学术/概念
- 搜索维基百科、学术站点、权威机构
- 重点：定义、历史、应用、争议

---

## 质量标准

- 至少引用 3 个独立来源
- 区分事实与观点
- 标注信息时效性（尤其是快速变化的领域）
- 结论要有依据，不凭空推断
- 中文主题用中文搜索，英文主题用英文搜索，必要时双语搜索

---

## 示例

**用户**: 帮我研究一下 Cursor 和 GitHub Copilot 的对比

**执行**:
1. 拆解：功能对比、价格、用户评价、技术架构、最新动态
2. 搜索：
   - `tvly search "Cursor vs GitHub Copilot 2026" --depth advanced --max-results 8 --json`
   - `tvly search "Cursor AI editor review" --time-range month --json`
   - `tvly search "GitHub Copilot features pricing 2026" --json`
3. 深度提取 2-3 个最相关页面
4. 输出结构化对比报告
