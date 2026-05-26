---
name: F
description: Windows内存清理工具。用于用户说"清理内存"、"省内存"、"关掉不用"、"内存不足"时。自动检查内存状态、关闭开机自启项、结束后台进程、释放内存。
---

# Windows 内存清理

## 内存检查

执行以下命令查看当前内存状态：

```powershell
$os = Get-CimInstance Win32_OperatingSystem
$total = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
$free = [math]::Round($os.FreePhysicalMemory / 1MB, 1)
$used = $total - $free
Write-Host "总内存: $total GB | 已用: $used GB | 空闲: $free GB | 使用率: $([math]::Round($used / $total * 100))%"
```

## 内存大户 TOP 15

```powershell
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 15 | ForEach-Object {
    $name = $_.ProcessName
    if ($name.Length -gt 20) { $name = $name.Substring(0, 17) + '...' }
    Write-Host ($name.PadRight(22) + [math]::Round($_.WorkingSet64/1GB, 2).ToString().PadLeft(6) + ' GB')
}
```

## 检查开机自启项

```powershell
Get-CimInstance Win32_StartupCommand | Select-Object Name, Command | Format-Table -AutoSize
```

## 检查有窗口的进程

```powershell
Get-Process | Where-Object { $_.MainWindowTitle -ne '' } | Sort-Object WorkingSet64 -Descending | Select-Object -First 15 | ForEach-Object {
    $title = $_.MainWindowTitle
    if ($title.Length -gt 40) { $title = $title.Substring(0, 37) + '...' }
    Write-Host "$($_.ProcessName.PadRight(20)) $([math]::Round($_.WorkingSet64/1MB))MB  $title"
}
```

## 关闭开机自启项

根据用户选择，关闭不需要的开机自启项。常见可关闭的：

| 项目 | 说明 |
|------|------|
| ocr / ocr_server | OCR 服务，不用则关 |
| QuarkUpdater | 夸克更新器，不用夸克则关 |
| MuMuNxMain / MuMuPlayerService | 模拟器服务，不用则关 |
| GameViewer | 游戏助手，不用则关 |
| Docker Desktop | Docker，不用则关 |

```powershell
$toRemove = @('ocr', 'ocr_server', 'QuarkUpdaterTaskUser1.0.0.21', 'MuMuNxMain', 'MuMuPlayerService', 'GameViewer', 'Docker Desktop')
$regPath = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
foreach ($item in $toRemove) {
    try {
        Remove-ItemProperty -Path $regPath -Name $item -ErrorAction Stop
        Write-Host "[关闭] $item"
    } catch {
        Write-Host "[跳过] $item (不存在)"
    }
}
```

## 关闭后台进程

根据用户选择，关闭不需要的后台进程。常见可关闭的：

| 程序 | 说明 |
|------|------|
| ApplicationFrameHost (Realtek相关) | 声卡设置，可关 |
| et | WPS表格，不用则关 |
| WeMail | 邮件客户端，不用则关 |
| Hihonornote | 笔记软件，不用则关 |
| BitBrowser | 指纹浏览器，不用则关 |
| quark | 夸克浏览器，不用则关 |

```powershell
$procs = @('WeMail', 'Hihonornote', 'BitBrowser', 'quark', 'et')
foreach ($p in $procs) {
    Get-Process -Name $p -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "[关闭] $p"
}
```

## 保留项（不主动建议关闭）

以下项目通常不应关闭，除非用户明确要求：
- leave_timer_startup — 离线检测器
- WXWork — 企业微信
- BaiduYunDetect / BaiduYunGuanjia — 百度网盘
- doubao — 豆包
- OneDrive — 同步云盘
- MicrosoftEdge — 浏览器
- Everything — 搜索工具

## 验证结果

操作完成后再次检查内存：

```powershell
$os = Get-CimInstance Win32_OperatingSystem
$free = [math]::Round($os.FreePhysicalMemory / 1MB, 1)
$total = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
Write-Host "清理完成 | 当前空闲: $free GB | 使用率: $([math]::Round(($total-$free)/$total*100))%"
```

## 工作流程

1. 检查当前内存状态
2. 列出内存大户 TOP 15
3. 检查开机自启项和有窗口的进程
4. **列出可关闭项，让用户确认**
5. 用户说"关"后才执行关闭
6. 验证内存释放效果
7. 汇总节省了多少内存

## 确认流程

列出可关闭项后，必须等用户确认后才能关闭。用户说"关"时执行用户指定的关闭操作。用户只说"关"但没指定项目时，默认关闭所有非必要项（保留 leave_timer_startup、WXWork、BaiduYun、doubao、OneDrive、Edge、Everything）。