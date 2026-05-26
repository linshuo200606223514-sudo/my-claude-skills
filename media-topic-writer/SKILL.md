---
name: media-topic-writer
description: 自媒体选题助手，搜索真实数据后生成视频脚本。Use when user wants to 选题, 出视频脚本, 自媒体内容创作, generate video script, find trending topics for social media. Searches Bilibili/Xiaohongshu/Zhihu gaps, outputs clean narration script with sources.
allowed-tools: Bash, WebSearch, Agent
---

# 自媒体选题 + 脚本生成

## 流程

### 第一步：明确方向
询问用户：
1. 内容方向（技术教程 / 工具测评 / 案例分享 / 观点类）
2. 目标平台（B站 / 小红书 / 公众号）
3. 有无现成项目或素材可用

### 第二步：搜索数据（并行）
用 Agent 工具并行搜索两个维度：

**维度A — 中文平台内容空白**
```
搜索关键词 + "site:bilibili.com"
搜索关键词 + "site:zhihu.com"
搜索关键词 + "site:xiaohongshu.com"
```
记录：命中数量、热门标题、内容空白点

**维度B — 英文/官方权威数据**
```
用 tvly search 或 WebSearch 搜索官方来源、报告、数据
```
记录：数据点、来源URL、发布日期

### 第三步：出选题
基于数据，输出选题表格：

| # | 标题 | 数据支撑 | 中文竞争 | 接单钩子 |
|---|------|---------|---------|---------|

按机会优先级排序（中文空白 + 英文有数据 = S级）

### 第四步：生成脚本
用户选定选题后，生成纯口播文稿：

**格式规范：**
- 只输出说话内容，无段落标题、无时间轴
- 数据来源用括号内嵌在对应句子后
- 分隔线 `---` 区分段落
- 文末单独列"数据来源"清单
- 结尾必须有下期预告CTA

**脚本结构：**
1. 开场钩子（反常识 / 数据冲击 / 反焦虑）
2. 官方/权威定位（引用原话）
3. 核心概念解释（类比 + 实例）
4. 数据支撑段（引用具体数字）
5. 个人案例（真实项目经历）
6. 结尾CTA（引出下期）

### 第五步：保存文件
保存到桌面：`C:/Users/clown/Desktop/视频脚本_<主题>.md`

## 搜索工具优先级

1. `tvly search` — 首选，LLM优化结果
   ```bash
   C:/Users/clown/bin/tvly.exe search "关键词" --depth advanced --max-results 8
   ```
   注意：在 Windows bash 环境下用 `cmd /c` 调用，或直接用 WebSearch 替代

2. WebSearch — tvly不可用时的备选

3. xiaohongshu-search skill — 需要小红书内部数据时

## 注意事项

- 数据来源必须标注：来源名称 + 日期
- 中文平台搜索结果为0 = 蓝海机会，重点标注
- 脚本语气：口语化、不说废话、有节奏感
- 不散布焦虑，正向引导
- 每条脚本结尾埋下一期钩子，形成系列
