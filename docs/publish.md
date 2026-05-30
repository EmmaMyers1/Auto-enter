# Publish to GitHub / 发布到 GitHub

[中文](#中文发布说明) | [English](#english-publish-guide)

---

## 中文发布说明

### 1. 确认仓库信息

GitHub 用户名：

```text
EmmaMyers1
```

推荐仓库名：

```text
auto-enter
```

仓库地址：

```text
https://github.com/EmmaMyers1/auto-enter
```

### 2. 初始化 Git

在本项目根目录运行：

```powershell
git init -b main
git add .
git commit -m "Initial auto-enter skill"
```

### 3. 创建 GitHub 仓库

在 GitHub 新建空仓库：

```text
https://github.com/EmmaMyers1/auto-enter
```

建议不要勾选自动生成 README，因为本项目已经包含 README。

### 4. 推送到 GitHub

```powershell
git remote add origin https://github.com/EmmaMyers1/auto-enter.git
git push -u origin main
```

### 5. GitHub Description 建议

```text
Windows Auto-Enter skill for Claude Code CLI that sends Enter to terminal windows at configurable intervals to help approve permission prompts.
```

中文描述：

```text
用于 Claude Code CLI 的 Windows 自动回车 Skill，可按设定间隔向终端发送 Enter，辅助确认权限提示。
```

### 6. 推荐 Topics

```text
claude-code, claude-skill, agent-skills, windows, powershell, automation, auto-enter
```

---

## English Publish Guide

### 1. Confirm repository information

GitHub username:

```text
EmmaMyers1
```

Recommended repository name:

```text
auto-enter
```

Repository URL:

```text
https://github.com/EmmaMyers1/auto-enter
```

### 2. Initialize Git

Run this from the project root:

```powershell
git init -b main
git add .
git commit -m "Initial auto-enter skill"
```

### 3. Create the GitHub repository

Create an empty GitHub repository:

```text
https://github.com/EmmaMyers1/auto-enter
```

Do not initialize it with a README because this project already includes one.

### 4. Push to GitHub

```powershell
git remote add origin https://github.com/EmmaMyers1/auto-enter.git
git push -u origin main
```

### 5. Suggested GitHub Description

```text
Windows Auto-Enter skill for Claude Code CLI that sends Enter to terminal windows at configurable intervals to help approve permission prompts.
```

Chinese description:

```text
用于 Claude Code CLI 的 Windows 自动回车 Skill，可按设定间隔向终端发送 Enter，辅助确认权限提示。
```

### 6. Recommended topics

```text
claude-code, claude-skill, agent-skills, windows, powershell, automation, auto-enter
```
