# Skill 结构设计规范

## 概述

Skill 是 Claude Code 的可复用工具单元。本规范定义 Skill 的标准结构，帮助你创建结构清晰、易于理解的 Skill。

---

## 标准结构

```
skill-name
├── 概述（用途、适用场景）
├── 快速开始（5分钟内能跑通）
├── 核心功能
│   ├── 功能1
│   │   ├── 说明
│   │   ├── 代码/命令
│   │   └── 示例
│   ├── 功能2
│   │   └── ...
│   └── 功能3
│       └── ...
├── 配置说明
│   ├── 必要配置
│   └── 可选配置
├── 注意事项
│   ├── 限制/坑点
│   └── 安全建议
└── 常见问题排查
    ├── 问题1 → 解决方案
    └── 问题2 → 解决方案
```

---

## 树状图语法

```
父节点
├── 子节点A（同级第一个）
│   ├── 孙子节点A1
│   └── 孙子节点A2
├── 子节点B（同级第二个）
│   └── ...
└── 子节点C（同级最后一个）
    └── ...
```

**符号说明：**
| 符号 | 含义 |
|------|------|
| `├──` | 有后续兄弟节点的分支 |
| `└──` | 同级最后一个节点 |
| `│` | 垂直连线（表示层级关系） |
| `    ` | 缩进（4空格） |

**示例：**
```
企业微信
├── 群机器人Webhook
│   ├── 获取地址
│   ├── 发送文本
│   ├── 发送Markdown
│   └── 发送图片
└── 自建应用API
    ├── 获取Token
    ├── 发送消息
    └── 上传文件
```

---

## 示例：wecom-bot Skill 结构

```
wecom-bot
├── 需求判断树
│   ├── 发通知到群聊？→ Webhook机器人
│   ├── 发消息给指定员工/部门？→ 自建应用API
│   └── 不确定？→ 先问Webhook地址
│
├── 方式一：群机器人 Webhook
│   ├── 获取Webhook地址
│   ├── 发送代码（Python标准库）
│   │   ├── 文本消息
│   │   ├── Markdown消息
│   │   ├── 图文卡片
│   │   ├── 图片（base64+md5）
│   │   └── 文件（上传+发送）
│   ├── Markdown颜色语法
│   └── 频率限制（20条/分钟，2000条/天）
│
├── 方式二：自建应用API
│   ├── 三个必要凭证
│   │   ├── corp_id（管理后台）
│   │   ├── corp_secret（手机APP查看）
│   │   └── agent_id（应用详情页）
│   └── 完整实现类WeComApp
│       ├── token缓存（线程安全）
│       ├── send_text/markdown/textcard
│       ├── upload_media
│       └── send_file/image
│
├── 常见错误码排查表
│   ├── 60020 → IP不在白名单
│   ├── 42001 → token过期
│   ├── 45009 → 超频率限制
│   ├── 40001 → Secret无效
│   ├── 81013 → 接收者为空
│   └── 900001 → agentid不存在
│
└── 注意事项
    ├── 无需第三方库（纯标准库）
    ├── token缓存机制
    ├── 多实例要用Redis集中缓存
    └── Secret要用环境变量，不要写代码里
```

---

## 创建新 Skill 的步骤

### 1. 确定 Skill 名称

规则：
- 全部小写
- 用连字符分隔单词（不用下划线）
- 名称反映功能，不反映实现

```
推荐：xiaohongshu-search, wecom-bot, image-compress
不推荐：XHS_API, WeChatBot, image_processing_tool
```

### 2. 创建目录结构

```bash
mkdir -p ~/.claude/skills/你的skill名称/scripts
touch ~/.claude/skills/你的skill名称/SKILL.md
```

### 3. 编写 SKILL.md

按以下顺序组织：

```markdown
# 你的 Skill 名称

## 一句话描述这个 Skill 做什么

## 使用场景
- 场景1
- 场景2

## 快速开始
3步之内让用户能用起来

## 核心功能
[用树状图展示结构]

## 详细说明
[每个功能的详细代码/命令]

## 示例
[完整的可运行示例]

## 注意事项
[坑点、限制、安全建议]

## 常见问题
[FAQ + 解决方案表格]
```

### 4. 编写脚本（可选）

如果有可执行脚本，放在 `scripts/` 目录下：

```
skill-name/
├── SKILL.md
└── scripts/
    ├── main.sh          # 主脚本
    ├── config.py        # 配置
    └── utils.py         # 工具函数
```

---

## 好的 Skill 结构的特点

| 特点 | 说明 |
|------|------|
| **名称清晰** | 看名字知道干什么 |
| **快速开始** | 5分钟内能跑通 |
| **树状图** | 一眼看清整体结构 |
| **代码可直接运行** | 复制粘贴就能用 |
| **示例完整** | 有输入输出说明 |
| **错误排查** | 常见问题有答案 |
| **注意事项** | 坑点提前告知 |

---

## 使用示例

### 如何用这个 Skill 测评其他 Skill

**场景：你刚装了一个新 Skill，想知道它好不好用**

```
User: 帮我测评一下 wecom-bot 这个 Skill
```

**Claude 响应步骤：**

1. 加载 wecom-bot 的 SKILL.md
2. 按7个维度逐项评分
3. 给出树状图还原结构
4. 指出优点和问题
5. 给出改进建议

---

### 实际对话示例

```
User: 帮我测评 xiaohongshu-search

Claude: [加载 SKILL.md]

=== xiaohongshu-search 测评结果 ===

总分：8.5/10

树状图（还原）：
```
xiaohongshu-search
├── 概述（小红书内容搜索）
├── 搜索功能
│   ├── 关键词搜索
│   ├── 按时间筛选
│   └── 按热度排序
├── 数据提取
│   ├── 笔记标题/内容
│   ├── 作者信息
│   └── 互动数据
├── 配置说明
└── 常见问题排查
```

优点：
- 树状图清晰，结构完整
- 有完整的中文示例
- 代码可直接运行

问题：
- 缺少快速开始章节
- 错误码表格不完整

改进建议：
- 在开头加3步快速开始
- 补充错误码 60020、45009 的说明

---

### 测评模板

评测评一个 Skill 时，按这个结构输出：

```
## [Skill名称] 测评结果

### 一句话总结
[用一句话描述这个skill是做什么的]

### 来源
[skill的网页地址：GitHub / 插件市场 / 官网等]

**必须获取实际可访问的网页地址，优先级：**
1. GitHub仓库地址（如 `https://github.com/owner/repo`）
2. 插件市场地址（如 `https://skills.sh/owner/skill-name`、`https://agentskill.club/skill/xxx`）
3. npm package地址（如 `https://www.npmjs.com/package/package-name`）
4. 官方网站（如 `https://firecrawl.dev/`）
5. Claude Code内置Skill → 标注为"Claude Code内置Skill"
6. **内部Skill** → 标注本地路径（如 `C:/Users/clown/.claude/skills/bilibili-transcript/SKILL.md`）

**获取方法：**
- 在SKILL.md中搜索 `github.com`、`npmjs.com`、`skills.sh`、`agentskill.club` 等关键词
- 在SKILL.md的description或frontmatter中查找链接
- **如果无外部链接，使用本地SKILL.md路径作为来源标注**

### 1. 技术结构图
[用业务语言描述skill的组成部分，不要写代码]

### 2. 实际例子
[3-5个场景，用业务语言描述]

### 3. 批量执行
[一行命令示例]

### 测评结果
| 维度 | 评分 | 说明 |
|------|------|------|
| 名称清晰 | ✅/❌ | ... |
| 快速开始 | ✅/❌ | ... |
| 结构完整 | ✅/❌ | ... |
| 批量能力 | ✅/❌ | ... |
| 示例质量 | ✅/❌ | ... |
| 错误排查 | ✅/❌ | ... |
| 注意事项 | ✅/❌ | ... |

### 总分
X/10
```

**注意：**
- 技术结构图：用业务语言描述组成部分，不要写代码
- 实际例子：用自然语言描述用户场景，不要写命令行
- 对话示例：不要出现 `${BUN_X}`、`scripts/main.ts` 等技术术语

---

### 实际使用例子要求

每个测评**必须包含**3-5个实际对话示例，体现这个 Skill 是如何被调用的。

**格式要求：用业务语言，不要技术语言**

❌ 错误示范（技术语言）：
```
User: 执行 ${BUN_X} scripts/main.ts --mode normal
Claude: → 调用 main.ts，分块翻译
输出：translation.md
```

✅ 正确示范（业务语言）：
```
User: 翻译这篇文章
Claude: → 加载配置 → 分析内容 → 翻译
输出：译文已保存到 translate/article-zh/translation.md
```

**模板：**
```
User: [用户需求 - 用自然语言]
Claude: [Skill 做了什么 - 用业务语言描述，不要写代码]
输出: [实际产出物 - 用户能看到的东西]
```

**示例：**

```
User: 发一组9张图到公众号
Claude: → 选择图文方式
  → 打开Chrome，扫二维码登录
  → 自动填充标题和内容
  → 上传9张图片
输出：[OK] 图文已存草稿箱

User: 怎么知道发成功了
Claude: → 访问 mp.weixin.qq.com → 内容管理 → 草稿箱
```

---

### 适用场景

| 场景 | 你会怎么问 |
|------|-----------|
| 刚装了一个 Skill | "帮我测评一下这个 Skill" |
| 想优化现有 Skill | "这个 Skill 缺什么？" |
| 对比两个类似 Skill | "wecom-bot 和 dingtalk-bot 哪个更好用" |
| 写新 Skill 前参考 | "帮我看看 xxx 的结构有什么问题" |

---

## 批量测评

**每次最多测评3个skills**，确保每个测评质量。

### 测评数量规则

| 情况 | 数量 |
|------|------|
| 用户指定具体skills | 最多3个（按指定顺序） |
| 用户未指定 | 从未测评的skills中选3个 |

### 无法获取网页来源的处理

对于无法找到实际网页地址的skill，在**来源**部分标注：

```
来源：内部Skill（无公开网页地址）
```

**内部Skill判断标准：**
- SKILL.md中无任何外部链接
- 无GitHub/npm/skills.sh等关键词
- 描述明确指向特定用户环境（如绑定快捷方式、用户特定路径）

**内部Skill仍需完整测评**，不影响评分，仅在来源处标注。

### 输入格式（三种都支持）

1. **逗号分隔**：`tavily-search, media-topic-writer, content-access`
2. **前缀匹配**：`baoyu-*`（所有以 baoyu- 开头的 skill）
3. **目录通配**：`skills/`（skills 目录下所有 skill）

### 使用方式

```
User: 批量测评 tavily-search, media-topic-writer, brainstorming
User: 测评所有 baoyu- 开头的 skill
User: 测评 skills/ 目录下的所有 skill
```

### 批量模式流程

1. **解析输入**：识别三种格式之一
   - 逗号分隔 → 解析为 skill 列表
   - 前缀匹配 → glob 匹配 `~/.claude/skills/{prefix}*/SKILL.md`
   - 目录通配 → 读取目录下所有 skill

2. **并行读取**：使用 Glob/Bash 并行读取多个 SKILL.md

3. **逐个测评**：对每个 skill 按标准模板输出测评结果

4. **保存汇总报告**：输出到 `C:/Users/clown/Desktop/Skills资料/批量测评报告_{timestamp}.md`

### 汇总报告格式

```markdown
# 批量测评报告

生成时间：2026-05-13 14:30

| Skill | 总分 | 名称清晰 | 快速开始 | 树状图 | 代码 | 示例 | 错误排查 | 注意事项 |
|-------|------|---------|---------|-------|------|------|---------|---------|
| tavily-search | 7/10 | ✅ | ✅ | ⚠️ | ✅ | ⚠️ | ⚠️ | ✅ |
| media-topic-writer | 6.5/10 | ✅ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ✅ |
| content-access | 7/10 | ✅ | ⚠️ | ✅ | ✅ | ⚠️ | ⚠️ | ✅ |

## 汇总

- 测评总数：3
- 平均分：6.8/10
- 表现最佳：tavily-search (7/10)、content-access (7/10)
- 需要改进：media-topic-writer (6.5/10)

## 各 Skill 详细结果

### tavily-search
[完整测评内容...]
```

### 实际对话示例

```
User: 帮我批量测评 tavily-search, tavily-extract, content-access

Claude: [检测到批量测评请求]

[解析输入：逗号分隔，三个 skill]
[并行读取三个 SKILL.md]
  → tavily-search/SKILL.md ✓
  → tavily-extract/SKILL.md ✓
  → content-access/SKILL.md ✓

[逐个输出测评结果...]

[生成汇总报告]
输出：批量测评报告已保存到 C:/Users/clown/Desktop/Skills资料/批量测评报告_2026-05-13.md
```

### 关键实现点

1. **输入解析**：用 Bash/Glob 处理三种输入格式
2. **并行读取**：glob 模式 `~/.claude/skills/*/SKILL.md` 批量读取
3. **汇总表格**：Markdown 表格 + 汇总统计
4. **输出到文件**：保存到 `C:/Users/clown/Desktop/Skills资料/批量测评报告_{date}.md`
5. **保持兼容**：单 skill 测评逻辑完全不变

---

## 反面教材

❌ 一个超长的 SKILL.md，没有分层，没有示例
❌ 树状图和实际内容对不上
❌ 只有代码，没有解释
❌ 代码依赖不说明，要用户自己猜
❌ 功能堆砌，没有按使用场景组织