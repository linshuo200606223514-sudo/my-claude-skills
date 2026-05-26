---
name: C
description: 端口占用检测与进程管理工具。用于启动服务前检查端口是否被占用、解决端口冲突、终止占用端口的进程。当需要启动服务、遇到端口被占用错误、或者需要清理孤儿进程时使用。核心功能：查询端口占用、显示占用进程PID和名称、终止进程、批量检测端口范围。
---

# 端口占用检测与进程管理

## 快速查询

```powershell
# 查询单个端口
netstat -ano | findstr :<端口号>

# 查询多个端口（逗号分隔）
netstat -ano | findstr :8080,:3000,:5173

# 获取占用端口的进程名称
Get-Process -Id <PID> | Select-Object -ExpandProperty ProcessName
```

## 工作流程

### 步骤1：检测端口状态

当AI准备启动服务时，**先执行**端口检测：

```powershell
# 检测单个端口
netstat -ano | findstr :<端口号>
```

- **无输出** = 端口空闲，可用
- **有输出** = 端口被占用，继续下一步

### 步骤2：识别占用进程

如果端口被占用，从输出中提取 PID，然后查询进程信息：

```powershell
# 查询进程名称
Get-Process -Id <PID> | Select-Object -ExpandProperty ProcessName
```

### 步骤3：决策处理

| 场景 | 操作 |
|------|------|
| 端口空闲 | 直接启动服务 |
| 端口被占用但进程不重要 | 终止进程后启动 |
| 端口被占用且进程重要 | 换端口或等待 |

### 步骤4：终止占用进程（如需要）

```powershell
# 强制终止进程
taskkill /PID <PID> /F
```

## 常用端口参考

| 端口 | 默认用途 |
|------|----------|
| 3000 | 开发服务器常见端口 |
| 5173 | Vite 默认端口 |
| 8080 | 通用 HTTP 端口 |
| 9222 | Node.js 调试端口 |
| 3001 | 备用开发端口 |

## 批量检测脚本

当需要检测多个端口时，使用：

```powershell
$ports = @(8080, 3000, 5173, 9222)
foreach ($port in $ports) {
    $result = netstat -ano | findstr ":$port"
    if ($result) {
        Write-Host "[占用] 端口 $port" -ForegroundColor Yellow
        $result -split "`n" | ForEach-Object {
            $pid = ($_ -split '\s+')[-1]
            $name = (Get-Process -Id $pid -ErrorAction SilentlyContinue).ProcessName
            Write-Host "  PID: $pid | 进程: $name"
        }
    } else {
        Write-Host "[空闲] 端口 $port" -ForegroundColor Green
    }
}
```

## 输出格式规范

检测结果统一输出：

```
端口 8080 检测结果：
  状态: [占用/空闲]
  PID: <PID>
  进程名: <名称>
  操作建议: [继续/终止进程/换端口]
```

## 决策规则

1. **端口空闲** → 直接启动服务，无需任何操作
2. **端口被占用** → 先识别进程，再决定：
   - 如果是 node.exe、python.exe、java 等开发进程 → 终止后使用
   - 如果是系统进程或重要服务 → **换端口**，不要终止
3. **无法判断进程重要性** → 询问用户

## 实时监控工具

提供 GUI 实时监控工具：

```bash
python C:/Users/clown/.claude/skills/C/port_monitor.py
```

功能：
- 实时显示所有监听端口
- 显示进程名、PID、项目来源
- 自动识别项目类型（GitHub搜索、OCR、Token统计等）
- 3秒自动刷新（可调整）
- 用户项目绿色高亮

## 安全约束

- **禁止**终止系统关键进程（lsass.exe、csrss.exe、smss.exe 等）
- **禁止**终止未知的企业安全软件进程
- 优先建议**换端口**而非强制终止