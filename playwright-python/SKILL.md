---
name: playwright-python
description: "Playwright Python browser automation - page navigation, selectors, waiting, screenshots, testing. Use when automating browsers with Python, writing Playwright tests, scraping web pages, or building browser automation scripts."
---

# Playwright Python

> Source: https://playwright.dev/python/docs/intro

## Installation

```bash
pip install pytest-playwright
playwright install
```

Or with conda:
```bash
conda config --add channels conda-forge
conda config --add channels microsoft
conda install pytest-playwright
```

## Sync API Pattern

```python
from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    chromium = playwright.chromium  # or "firefox" or "webkit"
    browser = chromium.launch()
    page = browser.new_page()
    page.goto("http://example.com")
    # other actions...
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
```

## Async API Pattern

```python
import asyncio
from playwright.async_api import async_playwright, Playwright

async def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = await chromium.launch()
    page = await browser.new_page()
    await page.goto("http://example.com")
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())
```

## Core Concepts

- **Browser**: `chromium`, `firefox`, `webkit` — launch with `playwright.<browser>.launch()`
- **Page**: Main interaction object — `browser.new_page()`
- **Locators**: Preferred way to find elements — `page.locator()`, `page.get_by_role()`, `page.get_by_text()`
- **Navigation**: `page.goto(url)` with `wait_until="networkidle"` / `"domcontentloaded"` / `"load"`
- **Waiting**: Auto-wait built in; explicit: `page.wait_for_selector()`, `page.wait_for_load_state()`
- **Screenshots**: `page.screenshot(path="screenshot.png", full_page=True)`
- **Headless/Headed**: `browser.launch(headless=False)` to see the browser

## Common Patterns

### Page navigation and content extraction
```python
page.goto("https://example.com", wait_until="networkidle")
title = page.title()
text = page.inner_text("body")
html = page.content()
```

### Click and type
```python
page.get_by_role("link", name="Get started").click()
page.get_by_label("Username").fill("user@example.com")
page.get_by_role("button", name="Submit").click()
```

### Wait for elements
```python
page.wait_for_selector(".result", timeout=10000)
page.locator(".item").wait_for(state="visible")
```

### Extract multiple elements
```python
items = page.query_selector_all(".list-item")
for item in items:
    print(item.inner_text())
```

### Handle new pages/popups
```python
with page.expect_popup() as popup_info:
    page.click("a[target='_blank']")
popup = popup_info.value
```

## Testing with Pytest

```python
import re
from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    page.goto("https://playwright.dev/")
    expect(page).to_have_title(re.compile("Playwright"))

def test_get_started_link(page: Page):
    page.goto("https://playwright.dev/")
    page.get_by_role("link", name="Get started").click()
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()
```

## Gotchas

- Always use `playwright install` after pip install to download browser binaries
- `networkidle` wait is useful but can be slow; prefer `domcontentloaded` when possible
- Use `headless=False` + `slow_mo=500` for debugging
- Context manager (`with sync_playwright()`) handles cleanup automatically
- For stealth/anti-detection: use `playwright-stealth` package

## References

- See `references/code_examples.md` for additional code examples from docs
