---
name: industry-research
description: |
  行业研究工具。输入关键词，自动搜索该领域头部玩家、最新动态、竞品对比，输出结构化 markdown 报告并保存到本地。
  聚焦自媒体、SEO、GEO、营销等领域。触发词："/industry-research {关键词}"、"研究一下XX行业"、"找一下XX领域的头部工具"。
allowed-tools: Bash(tvly *), Bash(mkdir *), Write
---

# industry-research

输入关键词，快速扫描该领域头部玩家和最新动态，输出结构化报告。

## 执行流程

### Step 1 — 获取关键词

从用户输入中提取研究关键词。如果用户直接写 `/industry-research SEO工具`，关键词就是 `SEO工具`。

### Step 2 — 多路并行搜索

同时运行以下4条搜索，结果分别保存到临时文件：

```bash
tvly search "{关键词} 头部工具 平台 官网 2026" --max-results 8 -o C:/tmp/research-main.json
tvly search "{关键词} 最新动态 融资 产品发布 2026" --max-results 6 --topic news -o C:/tmp/research-news.json
tvly search "{关键词} 竞品对比 推荐 哪个好" --max-results 6 -o C:/tmp/research-compare.json
tvly search "{关键词} 用户评价 v2ex reddit" --max-results 5 -o C:/tmp/research-community.json
```

注意：4条命令并行执行（同一个 Bash 调用，用 `&` 连接，最后 `wait`）。

### Step 3 — 筛选官网并提取详情

读取 `research-main.json`，筛出 score > 0.7 的结果，排除以下域名（聚合站/论坛）：
- zhihu.com, baidu.com, weibo.com, toutiao.com
- reddit.com, v2ex.com, quora.com
- wikipedia.org, baike.baidu.com

对筛出的前5个官网 URL 用 tavily extract 抓取内容：

```bash
tvly extract "{url1}" "{url2}" "{url3}" "{url4}" "{url5}" -o C:/tmp/research-extract.json
```

### Step 4 — 生成报告

综合所有搜索结果和提取内容，生成以下格式的报告：

```markdown
## {关键词} 行业研究报告 — {YYYY-MM-DD}

### 头部玩家
| 名称 | 官网 | 核心功能 | 定价模式 |
|------|------|----------|----------|
| ... | ... | ... | ... |

### 最新动态
- **{日期}** {事件描述} — [来源]({url})
- ...

### 值得关注的趋势
- ...

### 社区评价摘要
- ...

### 数据来源
- [{标题}]({url})
- ...
```

### Step 5 — 保存报告

```bash
mkdir -p "C:/Users/clown/industry-research"
```

将报告写入 `C:/Users/clown/industry-research/{关键词}-{YYYYMMDD}.md`

文件名中的空格替换为 `-`，例如：`SEO工具-20260422.md`

### Step 6 — 告知用户

输出报告内容，并告知保存路径。

---

## 注意事项

- tvly 命令输出中文时可能有编码问题，始终用 `-o` 保存到文件再读取，不要直接 `--json` 输出到终端
- 如果某个 URL 提取失败，跳过继续，不要中断整个流程
- 报告中的"定价模式"如果找不到明确信息，填"未知/需官网确认"
- 搜索关键词保持中文，不要翻译成英文（除非关键词本身是英文）
