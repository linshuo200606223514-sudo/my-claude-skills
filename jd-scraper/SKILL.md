---
name: jd-scraper
description: 京东商品数据自动化采集，生成Word采购文档。Use when user wants to scrape JD.com products, collect JD product info, 采集京东商品, 京东采集, 京东爬虫, 京东自动化. Handles anti-bot via Chrome CDP remote debugging.
---

# 京东商品自动化采集

## 唯一可行方案：Chrome CDP + 低频访问

**NEVER 使用以下方式（全部会被拦截）：**
- Playwright headless 模式直接访问
- Cookie 注入（TLS指纹绑定，跨浏览器无效）
- 直接调用 `p.3.cn/prices/mgets` API（已封锁）
- `context.new_page()` 频繁开新标签页

**ALWAYS 使用：**
- Chrome `--remote-debugging-port` + Playwright `connect_over_cdp`
- 复用已有标签页，不开新页
- 页面间隔 8-12 秒（随机）
- 单批次不超过 5-6 个商品

---

## 执行步骤

### Step 1：让用户启动 Chrome 调试实例

告诉用户运行以下命令（先关闭所有 Chrome 窗口）：

```
taskkill /F /IM chrome.exe
chrome.exe --remote-debugging-port=9223 --user-data-dir="%TEMP%\chrome-debug"
```

然后在弹出的 Chrome 中手动登录京东。

### Step 2：确认 CDP 连接

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
    page = browser.contexts[0].pages[0]
    print(page.url)
```

### Step 3：搜索页获取 SKU 列表（API 拦截）

```python
import json

sku_ids = []

def handle_response(response):
    if 'api.m.jd.com/api' in response.url and 'search-pc-java' in response.url:
        try:
            data = response.json()
            for item in data.get('wareList', []):
                sku_ids.append(item.get('wareId'))
        except:
            pass

page.on('response', handle_response)
page.goto(f'https://search.jd.com/Search?keyword={keyword}&enc=utf-8')
page.wait_for_timeout(5000)
```

### Step 4：逐个访问商品页（复用标签页）

```python
import random, time

results = []
for sku_id in sku_ids:
    # 复用同一个 page，不开新标签页
    page.goto(f'https://item.jd.com/{sku_id}.html')
    
    # 等待价格异步加载（京东价格延迟渲染，必须等 5-8 秒）
    page.wait_for_timeout(6000)
    
    title = page.query_selector('.sku-name')
    price = page.query_selector('.p-price .price')
    shop = page.query_selector('#crumb-wrap .curr-shop')
    
    results.append({
        'sku_id': sku_id,
        'title': title.inner_text() if title else '',
        'price': price.inner_text() if price else '',
        'shop': shop.inner_text() if shop else '',
        'url': f'https://item.jd.com/{sku_id}.html'
    })
    
    # 截图
    page.screenshot(path=f'screenshots/{sku_id}.png')
    
    # 随机间隔 8-12 秒
    time.sleep(random.uniform(8, 12))
```

### Step 5：触发验证码时

遇到滑块验证码时，**暂停脚本，提示用户手动完成**，然后继续：

```python
# 检测验证码
if '京东验证' in page.title() or page.query_selector('#JDJRV-wrap-loginsubmit'):
    input('检测到验证码，请手动完成后按 Enter 继续...')
```

### Step 6：写入 Word 文档

使用 `scripts/write_word.py` 生成采购文档。

---

## 关键参数

| 参数 | 值 |
|------|-----|
| CDP 端口 | 9223 |
| 价格等待时间 | 6000ms（不能少） |
| 页面间隔 | 8-12 秒随机 |
| 单批上限 | 5-6 个商品 |
| 价格选择器 | `.p-price .price` |
| 标题选择器 | `.sku-name` |
| 店铺选择器 | `#crumb-wrap .curr-shop` |

---

## 完整脚本

参考 `scripts/jd_collect.py`（如存在）。
如需新建，按以上步骤组合，入口函数接收 `keyword` 和 `max_items` 参数。
