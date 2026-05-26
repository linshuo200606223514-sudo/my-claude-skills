# skillhub-lookup

> 验证 Skills 在 skillhub.cn 上的可用性，并获取标准安装命令

## 触发场景

用户询问某个 Skill 在国内平台（skillhub.cn）的来源，或要求整理多平台安装教程时使用此技能。

## 使用方式

当需要查找某 Skill 在 skillhub.cn 的安装信息时，执行以下工作流：

### 1. 直接访问 Skill 页面

skillhub.cn 使用 `/skills/{skill-name}` 的直接路由格式（**不是** `skillhub.cn/skill-name`，而是 `/skills/` 复数路径）。

```
https://skillhub.cn/skills/{skill-name}
```

例如：`https://skillhub.cn/skills/summarize`、`https://skillhub.cn/skills/wecom`

### 2. 如果 slug 不确定，用搜索

访问 `https://skillhub.cn/skills`，在搜索框输入关键词，找到后查看浏览器 URL 获取真实 slug。

> 注意：skillhub.cn 的 URL 参数 `?search=` **不能**触发搜索，必须用页面内搜索框 + Enter 才能生效。

### 3. 获取安装命令

进入 Skill 页面后：
1. 点击「安装方式」标签页
2. 选择「命令行安装」标签
3. 复制两行命令：
   - 第一行：`curl -fsSL https://skillhub.cn/install/install.sh | bash`（安装 CLI）
   - 第二行：`skillhub install {skill-name}`（安装具体技能）

### 4. 注意事项

- **slug 可能与名称不同**：例如 wecom-bot 在 skillhub.cn 的 slug 是 `wecom`
- **部分 Skill 未收录**：skillhub.cn 不一定收录所有 ClawHub 技能，未收录的需标注
- **云鼎实验室安全标注**：`tavily-extract` 和 `wecom` 被云鼎实验室标注为"可疑，存在潜在风险"，但科恩实验室通过，这是正常现象
- **安装需要登录**：部分功能（如对话安装引导）需要登录后才能查看

## 示例工作流

**查找 tavily-extract 的安装信息**：

1. 导航到 `https://skillhub.cn/skills/tavily-extract`
2. 如果 404 → 尝试搜索框搜索 `tavily-extract`
3. 确认 slug 后，点击「安装方式」→「命令行安装」
4. 记录安装命令：
   ```bash
   curl -fsSL https://skillhub.cn/install/install.sh | bash
   skillhub install tavily-extract
   ```

## 多平台汇总格式

整理成以下表格：

| Skill | ClawHub | SkillsMP | skillhub.cn | 安装命令 |
|-------|---------|----------|-------------|---------|
| xxx   | ✅      | ✅       | ✅ (下载量) | `skillhub install xxx` |
| xxx   | ✅      | ✅       | ❌ 未找到  | 手动安装 |