---
name: web-rpa
description: "网页RPA自动化操作。Use when: 用户要做网页自动化、RPA、爬取网页、模拟点击表单、批量操作网站。Capabilities: 导航、点击、输入、搜索、提取数据、处理JS事件绑定。"
---

# Web RPA 自动化

使用 Playwright MCP (`mcp__plugin_playwright_playwright__*`) 操作网页。

## 工具选择

优先用 `mcp__plugin_playwright_playwright__*`，不用 `mcp__playwright__*`（Chrome 冲突问题）。

## 标准流程

### 1. 导航 + 快照
```
browser_navigate → browser_snapshot
```
快照返回带 `ref` 的元素树，用 ref 定位元素。

### 2. 点击元素
```
browser_click { ref: "e45", element: "描述" }
```

### 3. 输入文字
```
browser_type { ref: "e48", text: "内容" }
```

### 4. 截图确认
```
browser_take_screenshot { type: "png" }
```

---

## 关键陷阱与解决方案

### JS 事件绑定问题
网页按钮常用 jQuery 绑定事件，直接 `browser_click` 可能触发错误的处理函数。

**诊断**：
```js
// 用 evaluate 查看按钮 id 和对应逻辑
() => { const btns = document.querySelectorAll('input[type=button]'); return Array.from(btns).map(b => b.id + ' | ' + b.value); }
```

**查看 JS 源码**：
```js
() => fetch('/path/to/script.js').then(r=>r.text()).then(t=>{ const i = t.indexOf('btnId'); return t.substring(i-50, i+500); })
```

### Tab 切换 + data 属性
很多网站用 `data` 属性控制搜索类型（如"找工作"=0，"招人才"=1）。

**检查当前值**：
```js
() => { return $('#search_t2 .type').attr('data'); }
```

**修改后触发**：
```js
() => { $('#search_t2 .type').attr('data', '1'); document.querySelector('#keybtn2').click(); return 'done'; }
```

### 多个同名元素
首页常有多个搜索框（找工作/招人才/近期），id 通常是 `keyword1/2/3`，`keybtn1/2/3`。
先用 evaluate 枚举确认对应关系再操作。

### evaluate 语法
- 不能用分号结尾的单行语句（MCP 限制）
- 用箭头函数包裹：`() => { ...; return result; }`
- jQuery 可直接用 `$`（如果页面有加载）

---

## 常用 evaluate 片段

```js
// 枚举所有按钮
() => Array.from(document.querySelectorAll('input[type=button]')).map(b => b.id + '|' + b.value)

// 枚举所有输入框
() => Array.from(document.querySelectorAll('input[type=text]')).map(i => i.id + '|' + i.placeholder)

// 设置输入框值并触发事件
() => { const el = document.querySelector('#inputId'); el.value = '内容'; el.dispatchEvent(new Event('input')); el.dispatchEvent(new Event('change')); return 'ok'; }

// 直接跳转（绕过复杂JS逻辑）
() => { location.href = '/search/result.aspx?keyword=' + encodeURIComponent('关键词'); }

// 读取外部JS文件内容
() => fetch('/path/script.js').then(r=>r.text()).then(t=>t.substring(0, 3000))

// 查找JS函数定义
() => fetch('/path/script.js').then(r=>r.text()).then(t=>{ const i=t.indexOf('functionName'); return t.substring(i, i+500); })
```

---

## 数据提取

```js
// 提取列表数据
() => Array.from(document.querySelectorAll('.result-item')).map(el => ({
  title: el.querySelector('.title')?.textContent?.trim(),
  link: el.querySelector('a')?.href,
  desc: el.querySelector('.desc')?.textContent?.trim()
}))

// 提取表格数据
() => Array.from(document.querySelectorAll('table tr')).map(tr =>
  Array.from(tr.querySelectorAll('td,th')).map(td => td.textContent.trim())
)
```

---

## 实战案例：澄海人才网搜索简历

```
1. 导航到首页
2. 快照找到"招人才" tab 的 ref → browser_click
3. 确认 #search_t2 .type 的 data 属性是否为 "1"
4. 若不是，用 evaluate 设置 data="1"
5. 用 evaluate 设置 #keyword2 的值
6. 用 evaluate 点击 #keybtn2
→ 跳转到 /search/searresumeok.aspx?keyword=...
```

---

## 注意事项

- 操作前先 snapshot 确认页面状态
- 重要操作后用 screenshot 截图验证
- 遇到 `searchClick is not defined` 错误 → 说明 data 属性值不对，触发了错误分支
- 遇到 Chrome 启动失败 → 切换用 `mcp__plugin_playwright_playwright__*` 系列工具
