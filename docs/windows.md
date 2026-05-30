# Windows Notes

## Recommended terminal

Use Windows Terminal for the best experience.

The script can also target:

- `cmd.exe`
- `powershell.exe`
- `pwsh.exe`
- `conhost.exe`
- common terminal emulators such as WezTerm and Alacritty

## Check Python

```powershell
python --version
```

If Python is missing, install it:

```powershell
winget install Python.Python.3
```

## Check Claude Code

```powershell
claude --version
```

## Check target windows

```powershell
python "$env:USERPROFILE\.claude\skills\auto-enter\scripts\auto_enter.py" --list
```

## Start manually

```powershell
python "$env:USERPROFILE\.claude\skills\auto-enter\scripts\auto_enter.py" --auto --interval 5
```

## Stop manually

```powershell
python "$env:USERPROFILE\.claude\skills\auto-enter\scripts\auto_enter.py" --stop
```

## Troubleshooting

If the wrong window is selected, list windows first:

```powershell
python "$env:USERPROFILE\.claude\skills\auto-enter\scripts\auto_enter.py" --list
```

Then use a title filter:

```powershell
python "$env:USERPROFILE\.claude\skills\auto-enter\scripts\auto_enter.py" --auto --title "Claude" --interval 5
```
