---
name: baidu-search
description: "百度搜索并提取结果。Use when user wants to 百度搜索, 用百度查, baidu search, 搜索百度, 百度一下."
---

# 百度搜索

## 工作流程

### 第一步：打开百度搜索

用 Playwright 导航到百度搜索结果页：

```js
// 直接构造搜索 URL
const keyword = encodeURIComponent('YOUR_KEYWORD');
const url = `https://www.baidu.com/s?wd=${keyword}&rn=20`;
// navigate 到该 URL
```

用 `mcp__plugin_playwright_playwright__browser_navigate` 打开搜索 URL。

等待页面加载：
```js
// wait_for time: 2
```

### 第二步：提取搜索结果

用 `mcp__plugin_playwright_playwright__browser_evaluate` 提取结果：

```js
() => {
  const results = [];
  // 普通搜索结果
  document.querySelectorAll('#content_left .result, #content_left .result-op').forEach((el, i) => {
    if (i >= 10) return;
    const titleEl = el.querySelector('h3 a, .t a');
    const absEl = el.querySelector('.c-abstract, .content-right_8Zs40, .c-span9');
    const title = titleEl ? titleEl.innerText.trim() : '';
    const url = titleEl ? titleEl.href : '';
    const abstract = absEl ? absEl.innerText.trim().slice(0, 200) : '';
    if (title) results.push({ title, url, abstract });
  });
  return JSON.stringify(results);
}
```

### 第三步：深度提取（可选）

如果用户需要某条结果的详细内容，navigate 到该 URL 后用 `browser_evaluate` 提取正文：

```js
() => {
  // 移除导航、广告等干扰元素
  ['nav', 'header', 'footer', 'aside', '.ad', '#sidebar'].forEach(sel => {
    document.querySelectorAll(sel).forEach(el => el.remove());
  });
  return document.body.innerText.slice(0, 3000);
}
```

### 第四步：整理输出

将搜索结果整理后输出给用户：
- 标题 + 链接
- 摘要
- 如有深度提取，附上正文摘要

## 注意事项

- 百度有反爬，直接 navigate 比 fetch API 更稳定
- 搜索结果 DOM 选择器可能变化，备用选择器：`.c-container h3 a`、`.result h3 a`
- 如遇验证码，等待几秒后重试，或换关键词
- 百度新闻搜索用：`https://www.baidu.com/s?wd=${keyword}&tn=news`
- 百度图片搜索用：`https://image.baidu.com/search/index?tn=baiduimage&word=${keyword}`

## 搜索类型

| 类型 | URL 模板 |
|------|---------|
| 普通搜索 | `https://www.baidu.com/s?wd=KEYWORD&rn=20` |
| 新闻搜索 | `https://www.baidu.com/s?wd=KEYWORD&tn=news` |
| 最新结果 | `https://www.baidu.com/s?wd=KEYWORD&gpc=stf%3D1` |
| 图片搜索 | `https://image.baidu.com/search/index?tn=baiduimage&word=KEYWORD` |

## 常见问题

**结果为空**
- 检查选择器是否匹配当前百度 DOM，用 `browser_snapshot` 查看页面结构
- 备用：直接用 `browser_snapshot` 读取页面文本内容

**遇到验证码**
- `mcp__plugin_playwright_playwright__browser_wait_for` 等待 3 秒后重试
- 换更通用的关键词

**需要登录态**
- 先 navigate 到 `https://www.baidu.com`，确认已登录后再搜索
