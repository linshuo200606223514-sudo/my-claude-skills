---
name: multi-style-webpage
description: 批量生成多种视觉风格的网页展示集。Use when user wants to create multi-style website showcase, 多风格官网, 风格展示集, style gallery, 68种风格, 多套设计方案, or wants to demonstrate multiple visual aesthetics for one brand/product. Generates independent HTML files per style + Python index generator with iframe preview grid.
---

# Multi-Style Webpage

批量生成多种视觉风格的网页展示集，每种风格独立 HTML 文件，配套 Python 脚本生成带 iframe 预览的导航索引页。

## 实战来源

夜鹭云官网 68 种风格项目（`C:\Users\clown\Desktop\夜鹭云官网-68种风格\夜鹭云官网`），验证可行的完整方案。

## Skill 协作模式

本 skill 需同时激活两个设计 skill：

| Skill | 职责 |
|-------|------|
| `frontend-design` | 每个风格页面的代码质量 + 审美主张，避免"AI 通用感" |
| `ui-ux-pro-max` | 风格数据库参考（50种风格/21种配色/50种字体搭配） |

**工作顺序**：先用 `ui-ux-pro-max` 确定风格清单和配色字体，再用 `frontend-design` 逐一实现每个风格页面。

## 文件结构

```
输出目录/
├── index.html          # 导航索引页（Python 生成）
├── gen_index.py        # 索引页生成脚本
├── style-a.html        # 风格 A
├── style-b.html        # 风格 B
└── ...
```

## 风格页面规范

每个 `style-x.html` 是**完全独立**的单文件 HTML，包含：
- 内联 CSS（不依赖外部文件）
- 内联 JS（如需动效）
- Google Fonts CDN 引用（可选）
- 完整的品牌内容（导航、Hero、功能介绍、CTA、Footer）

每个风格必须有**明确的审美主张**，在代码注释中写明：
```html
<!-- 风格：赛博朋克·霓虹 | 配色：霓虹粉+青 | 字体：Orbitron | 特点：扫描线动效 -->
```

## 导航索引页规范

`gen_index.py` 生成 `index.html`，核心结构：

```python
styles = [
    ("A", "style-a.html", "风格名称", "描述", "Tag1|Tag2"),
    ...
]

# 每张卡片：iframe 缩放预览 + 风格信息 + 跳转链接
# iframe 缩放：width:200%, height:200%, transform:scale(0.5), transform-origin:top left
```

索引页配色建议：深色背景（`#080c18`）+ 蓝色 accent，与各风格页形成对比，突出展示效果。

## 风格分类参考

从 `ui-ux-pro-max` 的50种风格中选取，建议覆盖：

**暗黑系**：OLED黑粒子、赛博朋克、矩阵黑客、深海沉浸、宇宙星云  
**极简系**：极简大字排版、北欧极简、禅意冥想、瑞士国际主义  
**复古系**：Art Deco、蒸汽朋克、Y2K千禧、80s CRT、报纸印刷  
**东方系**：中国水墨、日本和风、禅意冥想  
**科技系**：Glassmorphism、Neumorphism、Bento Grid、Apple风、SaaS产品风  
**艺术系**：野兽派、解构主义、故障艺术、超现实主义、达达主义  
**自然系**：有机自然、水彩插画、手绘草图、薄雾朦胧、暗夜森林  

## 执行步骤

1. **确认需求**：品牌名称、行业、输出目录
2. **提出风格方案**：列出3-5种候选风格（名称+配色+字体+特点），**等用户确认选哪种**，不要自行决定
3. **生成单个风格页**：用户确认后只生成那一个，完成后让用户预览
4. **询问是否继续**：用户满意后再问"要不要再做一种风格？"，由用户决定数量
5. **积累到多个后**：再生成 gen_index.py 和 index.html 导航页

**关键原则：一次只做一个，做完给用户看，用户说继续才继续。**

## 质量检查

每个风格页完成后确认：
- [ ] 在浏览器中独立打开正常显示
- [ ] 有明显的视觉个性，与其他风格差异显著
- [ ] 动效流畅（如有）
- [ ] 中文字体正确加载（Noto Sans SC / Noto Serif SC）

## 常见坑

- **iframe 预览空白**：检查 `sandbox` 属性，需加 `allow-scripts allow-same-origin`
- **中文字体不显示**：Google Fonts 在国内需要网络，离线环境用系统字体 fallback
- **风格雷同**：每种风格必须在配色、字体、布局三个维度都有明显差异
- **文件过大**：WebGL/Canvas 动效页面可能超过 500KB，正常现象
