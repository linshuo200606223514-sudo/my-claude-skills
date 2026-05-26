---
name: n8n-workflow-scraper
description: 批量抓取n8n.io工作流页面信息，按固定格式写入Markdown文档。用于整理n8n热门工作流TOP列表。
---

# n8n Workflow Scraper

把n8n.io官网的工作流页面批量抓取，生成中文业务价值版Markdown文档。

## 核心能力

1. **批量扫描ID** — 按区间探测n8n.io/workflows/{ID}是否存在
2. **提取页面内容** — 从HTML中获取标题(title)和描述(description/meta)
3. **格式转换** — 把英文工作流介绍转成中文业务价值文档
4. **追加写入** — 固定格式追加到Markdown文件，更新计数

## 工作流程

### 1. 扫描发现（Discovery）

扫描n8n.io的workflow ID区间，找出存在的页面：

```powershell
# 检测单个ID
$status = (Invoke-WebRequest -Uri "https://n8n.io/workflows/{ID}/" -UseBasicParsing -TimeoutSec 8 -ErrorAction SilentlyContinue).StatusCode
# 200 = 存在，0 = 不存在
```

**策略**：按区间扫描（每50-100个ID一组），已知高密度区间：
- 12000-12600（密集）
- 7800-8400（密集）
- 11000-12000（中等）
- 14600-16000（稀疏）

### 2. 抓取内容（Fetch）

对存在的ID，提取页面信息：

```powershell
$headers = @{ 'User-Agent' = 'Mozilla/5.0' }
$r = Invoke-WebRequest -Uri "https://n8n.io/workflows/{ID}/" -UseBasicParsing -TimeoutSec 15 -Headers $headers
$content = $r.Content

# 提取标题
if ($content -match '<title>([^<]+)</title>') {
    $title = $matches[1] -replace '\s*[-|]\s*n8n.*', '' -replace '&#39;', "'" -replace '&amp;', '&'
}

# 提取描述（优先meta description）
if ($content -match '<meta name="description" content="([^"]+)"') {
    $desc = $matches[1] -replace '\\n', ' ' -replace '\s+', ' ' -replace '"', "'"
}
```

### 3. 格式模板

每个工作流按此格式写入：

```markdown
### 序号. 工作流名称
**URL**: https://n8n.io/workflows/{ID}-{slug}/
**帮你解决**：一句话说明解决什么业务问题

**运行逻辑**：
1. 步骤1
2. 步骤2
3. 步骤3

**技术栈**：工具1, 工具2, 工具3
**适用场景**：谁可以用、在什么情况下用
```

### 4. 追加写入（Bash方式）

Windows下PowerShell路径编码有问题，用Bash追加：

```bash
cat >> "/c/Users/clown/active/docs/n8n热门工作流TOP50.md" << 'APPEND_EOF'

---

### 序号. 工作流名称
**URL**: https://n8n.io/workflows/ID/
**帮你解决**：业务价值说明

**运行逻辑**：
1. 步骤1
2. 步骤2

**技术栈**：工具列表
**适用场景**：使用场景

---
APPEND_EOF
```

### 5. 更新计数

每次添加完，更新头部元数据：

```bash
sed -i 's/TOP 450/TOP {NEW}/' "/path/to/doc.md"
sed -i 's/450个工作流/{NEW}个工作流/' "/path/to/doc.md"
sed -i 's/已收录工作流：450个/已收录工作流：{NEW}个/' "/path/to/doc.md"
```

## 关键文件

- **目标文档**：`C:/Users/clown/active/docs/n8n热门工作流TOP50.md`
- **头部位置**：文件前10行（TOP数字、已收录数量）
- **插入位置**：找到 `## 常见业务场景速查表` 之前插入新内容

## 调用方式

在Claude Code中，当用户说"继续找n8n工作流"或"把n8n.io的工作流整理成文档"时，使用此skill。

### 典型对话

用户：`继续`
→ 使用此skill继续扫描下一个ID区间，追加到文档

用户：`继续找`
→ 使用此skill发现更多工作流

## 注意事项

1. **编码问题**：PowerShell处理中文路径有编码问题，文件写入用Bash的`cat >>`
2. **扫描节奏**：每个ID间隔50-100，避免请求过快被限流
3. **404处理**：遇到0状态码直接跳过，继续下一个
4. **计数同步**：每次追加后立即更新TOP数字和已收录数量