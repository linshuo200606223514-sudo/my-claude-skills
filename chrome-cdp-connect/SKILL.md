---
name: chrome-cdp-connect
description: 连接用户已登录的 Chrome 浏览器进行网页自动化操作。使用 CDP（Chrome DevTools Protocol）连接到 Shuo - Chrome.lnk 快捷方式启动的 Chrome。用于：打开网页、操作已登录的网站、浏览器自动化。触发词：打开浏览器、操作浏览器、用浏览器、在浏览器里。
---

# Chrome CDP 连接指南

连接用户已登录的 Chrome（Shuo - Chrome.lnk）进行网页操作。

## 快捷方式信息

- 路径：`C:\Users\clown\Desktop\Shuo - Chrome.lnk`
- 目标：`C:\Program Files\Google\Chrome\Application\chrome.exe`
- 参数：`--profile-directory="Default" --remote-debugging-port=9223 --remote-allow-origins=*`

## 关键经验：Chrome 单实例问题

**最常见的坑**：Chrome 有单实例机制。如果已有 Chrome 进程在跑（哪怕没有调试端口），新实例会把请求转发给旧实例后退出，导致调试端口永远不会监听。

**正确启动流程**：

```bash
# 1. 先杀掉所有 Chrome 进程
powershell -command "Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue"
sleep 3

# 2. 用完整参数重新启动（必须带 user-data-dir）
powershell -command "Start-Process 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe' -ArgumentList '--user-data-dir=C:\\Users\\clown\\AppData\\Local\\Google\\Chrome\\User Data','--profile-directory=Default','--remote-debugging-port=9223','--remote-allow-origins=*','--no-first-run'"
sleep 5

# 3. 验证端口是否监听
powershell -command "netstat -ano" | grep "9223"
# 应该看到：TCP  127.0.0.1:9223  LISTENING
```

## 验证连接

```bash
cd /c/Users/clown/.claude/skills/dev-browser && npx tsx <<'EOF'
import { chromium } from "playwright";

const browser = await chromium.connectOverCDP("http://localhost:9223");
const contexts = browser.contexts();
const pages = contexts[0]?.pages() ?? [];
console.log("Pages:", pages.map((p, i) => `${i}: ${p.url()}`));
await browser.close();
EOF
```

## 导航到目标网页

```bash
cd /c/Users/clown/.claude/skills/dev-browser && npx tsx <<'EOF'
import { chromium } from "playwright";

const browser = await chromium.connectOverCDP("http://localhost:9223");
const contexts = browser.contexts();
const page = contexts[0].pages()[0];

await page.goto("https://目标网址");
await page.waitForTimeout(3000);
console.log("URL:", page.url());
console.log("Title:", await page.title());
await page.screenshot({ path: "tmp/screenshot.png" });
await browser.close();
EOF
```

## 故障排查

| 症状 | 原因 | 解决方法 |
|------|------|----------|
| `ECONNREFUSED` | 端口没监听 | 按上面流程杀进程重启 |
| 进程有参数但端口没开 | Chrome 单实例转发 | 必须先 `Stop-Process` 再启动 |
| 跳到登录页 | Cookie 丢失 | 用户需要手动登录一次 |
| `Unexpected status 404` | 连到了别的服务（如 dev-browser 的 9222） | 确认端口号，用 `netstat` 检查 |

## 注意事项

- dev-browser 服务器默认占用 **9222**，Chrome CDP 用 **9223**，不要混淆
- 连接后不要调用 `browser.close()`，否则会关掉用户的 Chrome
- 用 `await browser.disconnect()` 代替 `close()`（Playwright CDP 模式）
- 截图保存到 `C:/Users/clown/.claude/skills/dev-browser/tmp/`
