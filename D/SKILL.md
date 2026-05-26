---
name: D
description: 查找Claude Code历史对话。搜索projects目录中的jsonl对话文件，提取last-prompt帮助用户恢复对话。
---

# 查找对话

直接执行以下命令并输出表格结果。

## 执行命令

```bash
echo "序号	项目名	时间	UUID	lastPrompt	文件路径"

count=1
for dir in $(find "C:/Users/clown/.claude/projects/" -type d -mmin -120 2>/dev/null | grep -v "subagents\|.jsonl" | sort -r); do
  # 获取项目目录名
  dirname=$(basename "$dir")

  # 在目录中查找最新的jsonl文件
  jsonl=$(find "$dir" -maxdepth 1 -name "*.jsonl" -mmin -120 2>/dev/null | head -1)

  if [ -n "$jsonl" ]; then
    uuid=$(basename "$jsonl" .jsonl | cut -c1-8)
    prompt=$(grep -a "lastPrompt" "$jsonl" 2>/dev/null | tail -1 | sed 's/.*"lastPrompt"\s*:\s*"\([^"]*\)".*/\1/' | cut -c1-50)
    ts=$(stat -c %y "$jsonl" 2>/dev/null | awk '{print $2}' | cut -c1-5)

    # 根据prompt关键词识别项目名
    if echo "$prompt" | grep -q "C盘\|扫描"; then
      name="C盘扫描小助手"
    elif echo "$prompt" | grep -q "剪辑"; then
      name="AI剪辑助手"
    elif echo "$prompt" | grep -q "github数字员工"; then
      name="GitHub数字员工"
    elif echo "$prompt" | grep -q "brainstorming"; then
      name="skills发现"
    elif echo "$prompt" | grep -q "AI自动开发企业应用\|企业工厂"; then
      name="AI企业工厂"
    elif echo "$prompt" | grep -q "端口占用"; then
      name="端口占用工具"
    elif echo "$prompt" | grep -q "闲鱼"; then
      name="闲鱼自动上架"
    elif echo "$prompt" | grep -q "github上.*有趣\|github上找到"; then
      name="GitHub有趣项目"
    elif echo "$prompt" | grep -q "离线检测"; then
      name="离线检测器"
    elif echo "$prompt" | grep -q "ima\|IMA"; then
      name="IMA技能安装"
    elif echo "$prompt" | grep -q "对话记录\|系统提示词"; then
      name="当前对话"
    else
      name="其他项目"
    fi

    if [ -n "$prompt" ] && [ "$prompt" != "lastPrompt" ]; then
      echo "$count	$name	$ts	$uuid	$prompt	$jsonl"
      count=$((count + 1))
    fi
  fi

  if [ $count -gt 15 ]; then break; fi
done
```

## 输出格式

直接输出表格：

```
序号	项目名	时间	UUID	lastPrompt	文件路径
1	离线检测器	23:41	36c081ba	"那你继续啊"	C:\Users\clown\.claude\projects\c--Users-clown--worktrees-listening-miniprogram-cloudfunctions\36c081ba-105d-4621-aba1-cf78a3ab793d.jsonl
2	IMA技能安装	23:43	3de5f728	"A"	C:\Users\clown\.claude\projects\c--Users-clown--worktrees-listening-miniprogram-cloudfunctions\3de5f728-1ffa-4777-bd80-e45430a1f865.jsonl
3	GitHub数字员工	23:43	dce7c594	"继续"	C:\Users\clown\.claude\projects\c--Users-clown--worktrees-listening-miniprogram-cloudfunctions\dce7c594-e679-4897-b8af-59f99d71fbf3.jsonl
...
```

## 复原对话

找到目录后，告诉用户：
```
去 Claude Code 打开目录: [文件路径]
然后继续之前的工作即可恢复对话
```
