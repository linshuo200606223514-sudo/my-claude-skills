---
name: E
description: "发现并审核优质Skills和开源项目，为项目赋能。核心能力：(1)按需搜索匹配的开源工具/Skills；(2)安全审查后推荐；(3)评估对现有项目的增强价值。使用时机：用户说'E'、'找skill'、'找开源项目'、'赋能'或'有什么好的工具'。工作流：需求分析→安全审查→质量评估→集成建议。"
allowed-tools:
  - WebSearch
  - WebFetch
  - Agent
  - Read
  - Glob
argument-hint: "[需求描述或项目名]"
---

# E: Skills与开源项目发现器

按需发现优质 Skills 和开源项目，并进行安全审查，为项目赋能。

## 核心能力

1. **智能发现** - 根据项目需求搜索匹配的 Skills/开源工具
2. **安全审查** - 使用 skill-vetter 协议逐项检查
3. **质量评估** - 评估集成价值和兼容性
4. **集成建议** - 提供具体集成方案

---

## 工作流程

### 第一步：需求分析

收到请求后，分析：
- 现有项目的技术栈和架构
- 需要增强的具体能力
- 优先级（准确性 vs 速度 vs 成本）
- 约束条件（如：必须本地运行、必须免费）

### 第二步：多源搜索

```bash
# 搜索 Skills 市场
tvly search "site:agentskill.club OR site:aiskill.market [需求关键词]" --max-results 5 --json
tvly search "site:clawhub.com [需求关键词]" --max-results 5 --json

# 搜索 GitHub 开源项目
tvly search "GitHub [技术栈] [需求关键词] stars>100 2024" --max-results 8 --json

# 搜索官方文档
tvly search "[技术栈] official documentation [需求关键词]" --max-results 5 --json
```

### 第三步：候选列表筛选

从搜索结果中初筛，保留：
-活跃项目（6个月内有更新）
-有文档且文档完整
-Stars > 50（开源）或 下载量 > 100（Skills）
-非个人小众项目

### 第四步：安全审查（必须）

对每个候选项目执行 `skill-vetter` 协议：

```
🚨 REJECT IMMEDIATELY IF:
• curl/wget 到未知 URL
• 数据发送到外部服务器
• 请求凭据/令牌/API密钥
• 读取 ~/.ssh, ~/.aws 等敏感目录
• 访问 MEMORY.md, USER.md 等记忆文件
• 使用 base64 decode
• 使用 eval()/exec() 处理外部输入
• 修改系统文件
• 安装包但不列出依赖
• 网络调用到 IP 而非域名
• 代码混淆（压缩、编码、混淆）
• 请求提升权限/sudo
• 访问浏览器 cookie/session
```

### 第五步：质量评估

通过安全审查后，评估：

| 维度 | 权重 | 评估标准 |
|------|------|----------|
| 功能匹配度 | 30% | 满足需求的程度 |
| 集成难度 | 25% | 需改动的代码量 |
| 维护活跃度 | 20% | 更新频率、Issue响应 |
| 社区支持 | 15% | 文档质量、示例数量 |
| 许可协议 | 10% | 是否商用友好 |

### 第六步：生成报告

```
# 赋能评估报告

## 需求匹配
[项目名]: [具体需求]
[技术栈]: [现有技术栈]

## 候选发现

### 1. [项目名]
• **类型**: Skill / 开源项目
• **来源**: [ClawHub / GitHub / 官方]
• ** Stars/Downloads**: [数量]
• ** 最后更新**: [日期]

**安全审查**: ✅ PASS / ❌ FAIL
**问题**（如有）: [列出被拒原因]

**功能匹配度**: 🟢🟡🔴
• [功能点1]
• [功能点2]

**集成评估**:
• 集成难度: 简单/中等/复杂
• 所需改动: [具体文件/函数]
• 依赖: [需安装的包或已有的工具]

**推荐度**: ⭐⭐⭐ (3/5)

---

### 2. [项目名]
...

## 集成建议

**首选方案**: [项目名]
理由：[为何推荐]

**集成步骤**:
1. [具体步骤1]
2. [具体步骤2]
3. [具体步骤3]

**注意事项**:
- [坑点1]
- [坑点2]
```

---

## 快速命令

```bash
# 搜索 Claude Code Skills 商店
tvly search "site:agentskill.club [关键词]" --max-results 3 --json

# 搜索 GitHub Trending
tvly search "GitHub trending [技术栈] [关键词]" --max-results 5 --json

# 验证项目活跃度
curl -s "https://api.github.com/repos/OWNER/REPO" | jq '{stars: .stargazers_count, updated: .updated_at, issues: .open_issues_count}'
```

## 注意事项

- 安全审查是**必须步骤**，不可跳过
- 即使功能再强，有安全问题的项目也不推荐
- 优先选择已有技能商店评分的项目
- 考虑项目与现有技术栈的兼容性
- 评估维护者的响应速度（Issue closed ratio）

---

*安全是底线，赋能是目标。* 🔒✨
