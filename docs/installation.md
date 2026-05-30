# Installation Guide / 安装说明

[中文](#中文安装说明) | [English](#english-installation-guide)

---

## 中文安装说明

本项目是适用于 Claude Code CLI 的 Windows 自动回车 Skill。

GitHub 仓库：

```text
https://github.com/EmmaMyers1/auto-enter
```

### 方式一：Windows PowerShell 快速安装

```powershell
npx skills add EmmaMyers1/auto-enter --skill auto-enter -g
```

然后启动 Claude Code：

```powershell
claude
```

使用：

```text
/auto-enter
```

### 方式二：Claude Code 插件安装

先启动 Claude Code：

```powershell
claude
```

然后在 Claude Code 中输入：

```text
/plugin marketplace add EmmaMyers1/auto-enter
/plugin install auto-enter@auto-enter
```

使用：

```text
/auto-enter:start 5
/auto-enter:status
/auto-enter:stop
/auto-enter:list
```

### 方式三：手动安装

从仓库根目录运行：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse ".\skills\auto-enter" "$env:USERPROFILE\.claude\skills\auto-enter" -Force
```

重启 Claude Code：

```powershell
claude
```

然后运行：

```text
/auto-enter
```

### 更新

```powershell
npx skills add EmmaMyers1/auto-enter --skill auto-enter -g
```

### 卸载

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\skills\auto-enter"
```

插件安装方式可在 Claude Code 中运行：

```text
/plugin uninstall auto-enter@auto-enter
```

---

## English Installation Guide

This project is a Windows Auto-Enter Skill for Claude Code CLI.

GitHub repository:

```text
https://github.com/EmmaMyers1/auto-enter
```

### Option 1: Quick install on Windows PowerShell

```powershell
npx skills add EmmaMyers1/auto-enter --skill auto-enter -g
```

Start Claude Code:

```powershell
claude
```

Use:

```text
/auto-enter
```

### Option 2: Claude Code plugin install

Start Claude Code first:

```powershell
claude
```

Then run these commands inside Claude Code:

```text
/plugin marketplace add EmmaMyers1/auto-enter
/plugin install auto-enter@auto-enter
```

Use:

```text
/auto-enter:start 5
/auto-enter:status
/auto-enter:stop
/auto-enter:list
```

### Option 3: Manual install

From the repository root:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse ".\skills\auto-enter" "$env:USERPROFILE\.claude\skills\auto-enter" -Force
```

Restart Claude Code:

```powershell
claude
```

Then run:

```text
/auto-enter
```

### Update

```powershell
npx skills add EmmaMyers1/auto-enter --skill auto-enter -g
```

### Uninstall

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\skills\auto-enter"
```

For plugin installs, run this inside Claude Code:

```text
/plugin uninstall auto-enter@auto-enter
```
