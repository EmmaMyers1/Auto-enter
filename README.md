# Auto Enter

[中文](#中文说明) | [English](#english-readme)

---

## 中文说明

Auto Enter 是一个适用于 **Claude Code CLI** 的 Windows 自动回车 Skill。它可以按设定间隔向 Windows Terminal、cmd 或 PowerShell 发送 `Enter`，用于在用户明确启动后辅助确认 Claude Code 的权限提示。

> 安全提醒：这个 Skill 会自动发送回车，可能会确认 Claude Code 的权限提示。请只在你明确知道 Claude Code 正在执行什么任务时使用，并在任务完成后及时停止。

### 功能特点

- 支持 Windows Terminal、cmd、Windows PowerShell、PowerShell 7。
- 可自动查找最合适的终端窗口。
- 可设置自动回车间隔，例如 3 秒、5 秒、10 秒。
- 支持查看状态、停止运行、列出可用终端窗口。
- 使用 `${CLAUDE_SKILL_DIR}` 定位脚本路径，避免硬编码本机路径。
- 已清理 `.git`、`__pycache__`、`.pyc`、运行 PID 等不适合上传 GitHub 的文件。

### 仓库结构

```text
auto-enter/
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
├── commands/
│   ├── list.md
│   ├── start.md
│   ├── status.md
│   └── stop.md
├── docs/
│   ├── installation.md
│   ├── publish.md
│   └── windows.md
├── skills/
│   └── auto-enter/
│       ├── SKILL.md
│       └── scripts/
│           └── auto_enter.py
├── .gitignore
├── LICENSE
└── README.md
```

### 安装方式一：Windows PowerShell 快速安装

确保你已经安装：

- Claude Code
- Python 3
- Node.js / npm

然后在 Windows PowerShell 中运行：

```powershell
npx skills add EmmaMyers1/auto-enter --skill auto-enter -g
```

安装完成后启动 Claude Code：

```powershell
claude
```

在 Claude Code 中输入：

```text
/auto-enter
```

### 安装方式二：Claude Code 插件方式安装

先启动 Claude Code：

```powershell
claude
```

然后在 Claude Code 中输入：

```text
/plugin marketplace add EmmaMyers1/auto-enter
/plugin install auto-enter@auto-enter
```

安装后可使用：

```text
/auto-enter:start 5
/auto-enter:status
/auto-enter:stop
/auto-enter:list
```

### 安装方式三：手动安装

如果你是从 GitHub 下载或克隆本仓库，可以在仓库根目录运行：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse ".\skills\auto-enter" "$env:USERPROFILE\.claude\skills\auto-enter" -Force
```

然后重启 Claude Code：

```powershell
claude
```

使用：

```text
/auto-enter
```

### 使用方法

启动自动回车，默认建议 5 秒：

```text
/auto-enter:start 5
```

查看状态：

```text
/auto-enter:status
```

停止自动回车：

```text
/auto-enter:stop
```

列出可用终端窗口：

```text
/auto-enter:list
```

如果有多个终端窗口，可以在 Skill 中使用标题过滤：

```powershell
python "${CLAUDE_SKILL_DIR}\scripts\auto_enter.py" --auto --title "Claude" --interval 5
```

### 更新

使用 `npx skills add` 安装的用户，可以重新运行：

```powershell
npx skills add EmmaMyers1/auto-enter --skill auto-enter -g
```

手动安装的用户，可以重新复制：

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\skills\auto-enter"
Copy-Item -Recurse ".\skills\auto-enter" "$env:USERPROFILE\.claude\skills\auto-enter" -Force
```

### 卸载

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\skills\auto-enter"
```

如果使用插件方式安装，可以在 Claude Code 中运行：

```text
/plugin uninstall auto-enter@auto-enter
```

### 仓库描述

```text
Windows Auto-Enter skill for Claude Code CLI that sends Enter to terminal windows at configurable intervals to help approve permission prompts.
```

中文描述：

```text
用于 Claude Code CLI 的 Windows 自动回车 Skill，可按设定间隔向终端发送 Enter，辅助确认权限提示。
```

---

## English README

Auto Enter is a Windows-only **Claude Code CLI Skill** that sends `Enter` to Windows Terminal, cmd, or PowerShell at configurable intervals. It is designed to help approve Claude Code permission prompts after the user explicitly starts it.

> Safety note: this skill automatically sends Enter and may approve Claude Code permission prompts. Use it only when you understand what Claude Code is doing, and stop it when the task is complete.

### Features

- Supports Windows Terminal, cmd, Windows PowerShell, and PowerShell 7.
- Automatically detects the most likely terminal window.
- Configurable interval, such as 3, 5, or 10 seconds.
- Supports start, stop, status check, and window listing.
- Uses `${CLAUDE_SKILL_DIR}` to locate bundled scripts, avoiding hard-coded local paths.
- Clean GitHub-ready structure without `.git`, `__pycache__`, `.pyc`, or runtime PID files.

### Repository structure

```text
auto-enter/
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
├── commands/
│   ├── list.md
│   ├── start.md
│   ├── status.md
│   └── stop.md
├── docs/
│   ├── installation.md
│   ├── publish.md
│   └── windows.md
├── skills/
│   └── auto-enter/
│       ├── SKILL.md
│       └── scripts/
│           └── auto_enter.py
├── .gitignore
├── LICENSE
└── README.md
```

### Installation option 1: Quick install on Windows PowerShell

Make sure you have installed:

- Claude Code
- Python 3
- Node.js / npm

Then run this in Windows PowerShell:

```powershell
npx skills add EmmaMyers1/auto-enter --skill auto-enter -g
```

Start Claude Code:

```powershell
claude
```

Then use:

```text
/auto-enter
```

### Installation option 2: Claude Code plugin install

Start Claude Code first:

```powershell
claude
```

Then run these commands inside Claude Code:

```text
/plugin marketplace add EmmaMyers1/auto-enter
/plugin install auto-enter@auto-enter
```

After installation, use:

```text
/auto-enter:start 5
/auto-enter:status
/auto-enter:stop
/auto-enter:list
```

### Installation option 3: Manual install

If you downloaded or cloned this repository, run the following from the repository root:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse ".\skills\auto-enter" "$env:USERPROFILE\.claude\skills\auto-enter" -Force
```

Restart Claude Code:

```powershell
claude
```

Then use:

```text
/auto-enter
```

### Usage

Start Auto Enter with a recommended 5-second interval:

```text
/auto-enter:start 5
```

Check status:

```text
/auto-enter:status
```

Stop Auto Enter:

```text
/auto-enter:stop
```

List available terminal windows:

```text
/auto-enter:list
```

If multiple terminal windows are open, use a title filter inside the skill:

```powershell
python "${CLAUDE_SKILL_DIR}\scripts\auto_enter.py" --auto --title "Claude" --interval 5
```

### Update

For users who installed with `npx skills add`, run:

```powershell
npx skills add EmmaMyers1/auto-enter --skill auto-enter -g
```

For manual installs, copy the skill again:

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\skills\auto-enter"
Copy-Item -Recurse ".\skills\auto-enter" "$env:USERPROFILE\.claude\skills\auto-enter" -Force
```

### Uninstall

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\skills\auto-enter"
```

For plugin installs, run this inside Claude Code:

```text
/plugin uninstall auto-enter@auto-enter
```

###  Repository description

```text
Windows Auto-Enter skill for Claude Code CLI that sends Enter to terminal windows at configurable intervals to help approve permission prompts.
```

Chinese description:

```text
用于 Claude Code CLI 的 Windows 自动回车 Skill，可按设定间隔向终端发送 Enter，辅助确认权限提示。
```

## License

MIT
