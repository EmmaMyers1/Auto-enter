---
name: auto-enter
description: Automatically sends Enter to Windows Terminal, cmd, or PowerShell at a configurable interval to help approve Claude Code CLI permission prompts. Use only when the user explicitly asks to start, stop, check status, or list windows for auto-enter.
user-invocable: true
allowed-tools: "Bash"
metadata:
  version: "1.0.0"
  platform: "Windows"
---

# Auto Enter

Auto Enter helps Claude Code CLI users on Windows automatically press `Enter` in a terminal window at a configurable interval.

It is intended for cases where Claude Code repeatedly asks for permission confirmations and the user explicitly wants those prompts approved automatically.

> Safety note: this skill can approve prompts automatically. Start it only when you understand what Claude Code is doing, and stop it when the task is finished.

## What it does

- Finds the most likely Windows terminal window automatically.
- Supports Windows Terminal, `cmd.exe`, Windows PowerShell, and PowerShell 7.
- Sends `Enter` through Win32 `PostMessage`, so it can work even when the terminal is not focused.
- Writes a small PID file next to the script so it can be stopped or checked later.

## Important path note

Do **not** hard-code a local path such as:

```text
C:\Users\Administrator\.claude\skills\auto-enter\scripts\auto_enter.py
```

Always use the current skill directory variable:

```text
${CLAUDE_SKILL_DIR}
```

This makes the skill portable across different Windows users and installation locations.

## Commands

### Start

Ask the user for an interval if they did not provide one. Recommended choices are `3`, `5`, `7`, or `10` seconds. Default to `5`.

```powershell
python "${CLAUDE_SKILL_DIR}\scripts\auto_enter.py" --auto --interval 5
```

When using Claude Code's Bash tool, prefer a background process on Windows:

```powershell
powershell.exe -NoProfile -ExecutionPolicy RemoteSigned -Command "Start-Process -WindowStyle Hidden -FilePath python -ArgumentList @('${CLAUDE_SKILL_DIR}\scripts\auto_enter.py','--auto','--interval','5')"
```

Replace `5` with the user's chosen interval.

### Start with title filter

Use this when more than one terminal window is open:

```powershell
python "${CLAUDE_SKILL_DIR}\scripts\auto_enter.py" --auto --title "Claude" --interval 5
```

### Status

```powershell
python "${CLAUDE_SKILL_DIR}\scripts\auto_enter.py" --status
```

### Stop

```powershell
python "${CLAUDE_SKILL_DIR}\scripts\auto_enter.py" --stop
```

### List target windows

```powershell
python "${CLAUDE_SKILL_DIR}\scripts\auto_enter.py" --list
```

### Debug

```powershell
python "${CLAUDE_SKILL_DIR}\scripts\auto_enter.py" --auto --interval 5 --debug
```

## Operating rules for Claude

1. Do not start Auto Enter unless the user explicitly asks for it.
2. Always ask for or infer a short interval before starting. Default to `5` seconds when unclear.
3. After starting, tell the user how to stop it: `/auto-enter:stop` or the `--stop` command above.
4. Prefer `--list` or `--title` when multiple terminal windows may be open.
5. Stop the old instance before starting a new one; the script already does this automatically.
6. Do not use Auto Enter for destructive, unclear, or high-risk operations.
7. Remind the user to stop Auto Enter when the current Claude Code task is complete.

## Script reference

```text
usage: python auto_enter.py [-h] [--title TITLE] [--interval INTERVAL]
                            [--auto] [--debug] [--list] [--stop] [--status]

--auto, -a      Auto-detect the best console/terminal window.
--title, -t     Optional window title filter.
--interval, -i  Seconds between Enter presses. Default: 5.
--debug         Show child window details for troubleshooting.
--list, -l      List visible windows with process names and hints.
--stop          Stop a running auto-enter process.
--status        Show whether auto-enter is running.
```
