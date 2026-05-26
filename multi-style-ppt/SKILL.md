---
name: multi-style-ppt
description: 生成有设计感的多风格PPT演示文稿，用python-pptx实现。Use when user wants to create PPT, 做PPT, 制作幻灯片, 演示文稿, presentation with specific visual style, 水墨风PPT, 科技风PPT, 极简PPT, or wants to apply a distinctive aesthetic to slides. Combines pptx-skill (python-pptx技术) + ui-ux-pro-max (风格数据库) + frontend-design (审美主张).
---

# Multi-Style PPT

用 python-pptx 生成有强烈视觉风格的 PPT，避免默认模板的平庸感。

## Skill 协作模式

| Skill | 职责 |
|-------|------|
| `pptx-skill` | python-pptx 技术实现（形状、颜色、字体、布局） |
| `ui-ux-pro-max` | 风格数据库（配色方案、字体搭配参考） |
| `frontend-design` | 审美主张——每个风格必须有明确的视觉个性 |

## 执行原则

**一次只做一个风格，做完给用户看，用户确认后再继续。**

1. 提出 3 种候选风格（名称+配色+字体+视觉特点），等用户选
2. 用户选定后生成单个 .pptx 文件
3. 告知文件路径，让用户打开预览
4. 用户满意后再问是否需要其他风格

## python-pptx 核心技术

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width  = Inches(13.33)   # 16:9 宽屏
prs.slide_height = Inches(7.5)

# 空白布局（最灵活）
slide = prs.slides.add_slide(prs.slide_layouts[6])

# 设置背景色
bg = slide.background.fill
bg.solid()
bg.fore_color.rgb = RGBColor(0x1A, 0x1A, 0x1A)

# 添加矩形色块
shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.33), Inches(1.2))
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0x00, 0x66, 0xFF)
shape.line.fill.background()

# 添加文字框
txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(10), Inches(0.8))
tf = txBox.text_frame
p = tf.paragraphs[0]
run = p.add_run()
run.text = "标题文字"
run.font.size = Pt(28)
run.font.bold = True
run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
run.font.name = "Microsoft YaHei"
p.alignment = PP_ALIGN.LEFT

prs.save("output.pptx")
```

## 风格实现要点

### 水墨风
- 背景：宣纸米白 `#F5F0E8`
- 装饰：用细矩形叠加模拟笔触、山水轮廓
- 印章：红色正方形 + 白色文字
- 字体：SimSun / Microsoft YaHei，标题加粗
- 点缀色：朱砂红 `#C0392B`、青墨蓝 `#1A3A5C`

### 暗黑科技风
- 背景：`#0A0A0F`，顶部/底部渐变色条
- 强调色：电蓝 `#0066FF` 或青 `#00D4FF`
- 字体：Microsoft YaHei（中文）+ 等宽感
- 装饰：细线分隔、发光色块

### 极简大字排版
- 背景：纯白或米白
- 超大字号标题（Pt 48-72）
- 大量留白，内容极度精简
- 单一强调色（红或黑）

### Glassmorphism
- 深色渐变背景（深紫蓝）
- 半透明白色卡片（用浅灰近似）
- 圆角矩形 + 细边框

### 学术/期刊风
- 白底 + 深蓝 `#1A3A5C`
- 双栏布局感
- 衬线字体感（SimSun）
- 编号、引用线装饰

## 常见坑

- **中文字体**：Windows 用 `"Microsoft YaHei"` / `"SimSun"`，不要用 Google Fonts 名称
- **RGBColor**：传入三个 0-255 整数，不是十六进制字符串
- **布局6**：`slide_layouts[6]` 是空白布局，最灵活，避免用带占位符的布局
- **形状类型**：`add_shape(1, ...)` 中 `1` = MSO_SHAPE_TYPE.RECTANGLE
- **文件路径**：Windows 路径用正斜杠或原始字符串，避免编码问题
- **字体大小**：`Pt(18)` 不是 `18`，必须用 `Pt()` 包装
