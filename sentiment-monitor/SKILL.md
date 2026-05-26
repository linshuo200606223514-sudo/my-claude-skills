---
name: sentiment-monitor
description: |
  品牌舆情监控员工。用于监控指定企业在互联网上的负面内容，自动搜索百度/必应，用 Claude 判断是否负面，生成报告保存到桌面，发现负面内容时推送 Windows 通知。Use when user wants to monitor brand reputation, 舆情监控, 负面内容检测, 品牌监控, or says "帮我监控舆情", "查一下有没有负面", "舆情分析".
allowed-tools: Bash(python *)
---

# 舆情监控员工

## 严格规则

**CRITICAL: 你只能做一件事——运行下面这条命令。禁止创建任何文件、禁止自己搜索网络、禁止生成任何报告。**

```bash
"C:\Users\clown\AppData\Local\Python\bin\python.exe" "C:\Users\clown\Desktop\舆情检测助手\sentiment_worker.py"
```

运行后等待脚本完成，把终端输出的报告路径告诉用户。完成。

---

## 为新客户创建监控（仅当用户明确要求新建时）

1. 询问：企业全称、监控关键词
2. 复制 `C:\Users\clown\Desktop\舆情检测助手\sentiment_worker.py`，修改 `KEYWORDS` 和 `FACTORY_CONTEXT`
3. 运行新脚本

## 注意事项

- 百度搜索不走代理（直连），必应走代理（127.0.0.1:7890）
- Claude 模型用 `claude-sonnet-4-6`
- 百度偶尔 ERR_EMPTY_RESPONSE，重跑一次即可
