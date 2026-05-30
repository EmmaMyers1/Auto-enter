"""
Auto-Enter: Send Enter key to a target window at regular intervals.
Uses Win32 PostMessage so it works even when the window is minimized or not in focus.
Sends Enter to both the main window AND all child/descendant windows to handle
modern terminal emulators (Windows Terminal, etc.) that process input in child windows.
Run: python auto_enter.py --auto --title "Claude" --interval 5
Stop: python auto_enter.py --stop
Status: python auto_enter.py --status
"""

import argparse
import ctypes
import json
import os
import signal
import sys
import time
from ctypes import wintypes

# Force UTF-8 output to avoid GBK encoding errors with Unicode window titles
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# This skill controls Windows terminal windows via Win32 APIs.
if os.name != "nt":
    print("[auto-enter] ERROR: This script is Windows-only and requires Win32 APIs.")
    sys.exit(1)

# Win32 API
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_CHAR = 0x0102
VK_RETURN = 0x0D

PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

# Process names considered "console/terminal" windows
CONSOLE_PROCESSES = {
    "windowsterminal.exe",
    "cmd.exe", "powershell.exe", "pwsh.exe",
    "conhost.exe", "console.exe", "alacritty.exe",
    "wezterm.exe", "winterm.exe", "terminus.exe",
}

# Title keywords that suggest a Claude Code CLI window
CLAUDE_TITLE_HINTS = ["claude", "code", "terminal", "powershell", "cmd", "命令"]

PID_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".auto_enter_pid")


def get_window_process_name(hwnd):
    """Get the executable name (e.g. 'windowsterminal.exe') for a window handle."""
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    try:
        hproc = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid.value)
        if not hproc:
            return "unknown"
        exe_buf = ctypes.create_unicode_buffer(260)
        exe_len = wintypes.DWORD(260)
        if kernel32.QueryFullProcessImageNameW(hproc, 0, exe_buf, ctypes.byref(exe_len)):
            name = os.path.basename(exe_buf.value).lower()
        else:
            name = "unknown"
        kernel32.CloseHandle(hproc)
        return name
    except Exception:
        return "unknown"


def is_console_process(proc_name):
    """Check if a process name belongs to a console/terminal application."""
    return proc_name.lower() in CONSOLE_PROCESSES


def enum_all_descendants(hwnd):
    """Recursively enumerate ALL descendant windows (children, grandchildren, etc.) of hwnd.
    Uses BFS to avoid stack overflow on deeply nested windows."""
    result = []

    def collect_children(parent):
        kids = []
        def cb(h, _):
            kids.append(h)
            return True
        WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        user32.EnumChildWindows(parent, WNDENUMPROC(cb), 0)
        return kids

    queue = [hwnd]
    while queue:
        parent = queue.pop(0)
        kids = collect_children(parent)
        result.extend(kids)
        queue.extend(kids)

    return result


def send_enter_to_window(hwnd):
    """Send WM_KEYDOWN + WM_CHAR + WM_KEYUP for VK_RETURN to a single window."""
    user32.PostMessageW(hwnd, WM_KEYDOWN, VK_RETURN, 0x001C0001)
    time.sleep(0.01)
    user32.PostMessageW(hwnd, WM_CHAR, 0x0D, 0x001C0001)
    time.sleep(0.01)
    user32.PostMessageW(hwnd, WM_KEYUP, VK_RETURN, 0xC01C0001)


def send_enter_to_all(hwnd, debug=False):
    """Send Enter to the main window AND all descendant windows.
    Returns the total number of windows targeted."""
    descendants = enum_all_descendants(hwnd)
    targets = [hwnd] + descendants

    for t in targets:
        send_enter_to_window(t)

    if debug and len(targets) > 1:
        for t in descendants:
            length = user32.GetWindowTextLengthW(t)
            cls_buf = ctypes.create_unicode_buffer(64)
            user32.GetClassNameW(t, cls_buf, 64)
            if length > 0:
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(t, buf, length + 1)
                print(f"  [DEBUG] child hwnd={t} class='{cls_buf.value}' title='{buf.value}'")
            else:
                print(f"  [DEBUG] child hwnd={t} class='{cls_buf.value}' (no title)")

    return len(targets)


def find_window_by_title(title_substr):
    """Find all visible windows whose title contains the given substring (case-insensitive).
    Returns list of (hwnd, title, proc_name)."""
    result = []

    def enum_callback(hwnd, _lparam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buf, length + 1)
                if title_substr.lower() in buf.value.lower():
                    result.append((hwnd, buf.value, get_window_process_name(hwnd)))
        return True

    WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(WNDENUMPROC(enum_callback), 0)
    return result


def _title_has_claude_hint(title):
    """Check if a window title contains hints of being a Claude Code / dev terminal."""
    t = title.lower()
    return any(h in t for h in CLAUDE_TITLE_HINTS)


def find_best_console_window(title_substr=None):
    """Find the best console window for Claude Code CLI.
    Prefers: console processes > non-console; Claude-related titles > other titles.
    If title_substr is given, filters by title first.
    Returns (hwnd, title, proc_name) or None."""
    candidates = []
    seen_hwnds = set()

    def enum_callback(hwnd, _lparam):
        if hwnd in seen_hwnds or not user32.IsWindowVisible(hwnd):
            return True
        seen_hwnds.add(hwnd)
        length = user32.GetWindowTextLengthW(hwnd)
        if length == 0:
            return True

        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        win_title = buf.value.strip()
        if not win_title:
            return True

        proc_name = get_window_process_name(hwnd)
        is_console = is_console_process(proc_name)
        has_hint = _title_has_claude_hint(win_title)

        if title_substr:
            if title_substr.lower() in win_title.lower():
                # Priority: console=0, non-console=1; hint=better
                candidates.append((0 if is_console else 1, 0 if has_hint else 1, len(win_title), hwnd, win_title, proc_name))
        else:
            if is_console:
                candidates.append((0, 0 if has_hint else 1, len(win_title), hwnd, win_title, proc_name))
        return True

    WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(WNDENUMPROC(enum_callback), 0)

    if not candidates:
        return None

    # Sort: console first, then Claude-hint, then shorter title
    candidates.sort(key=lambda x: (x[0], x[1], x[2]))
    best = candidates[0]
    return (best[3], best[4], best[5])


def run_loop(hwnd, win_title, interval, debug=False):
    """Main loop: send Enter at regular intervals to a known hwnd + all descendants."""
    print(f"[auto-enter] Starting, interval={interval}s, target='{win_title}'")
    print(f"[auto-enter] PID={os.getpid()}")
    if debug:
        print(f"[auto-enter] Debug mode ON — will show child windows on first send")

    first_send = True

    while True:
        if not user32.IsWindow(hwnd):
            print(f"[auto-enter] WARNING: Target window closed. Searching for new one...")
            best = find_best_console_window()
            if best:
                hwnd, win_title, proc_name = best
                print(f"[auto-enter] Reconnected to '{win_title}' ({proc_name})")
                first_send = True
            else:
                print(f"[auto-enter] No console window found. Retrying in {interval}s...")
                time.sleep(interval)
                continue

        n = send_enter_to_all(hwnd, debug=debug and first_send)
        first_send = False

        timestamp = time.strftime("%H:%M:%S")
        if debug:
            print(f"[auto-enter] {timestamp} -> Enter sent to '{win_title}' + {n-1} child windows (hwnd={hwnd})")
        else:
            print(f"[auto-enter] {timestamp} -> Enter sent to '{win_title}' (hwnd={hwnd})")

        time.sleep(interval)


def run_loop_by_title(title, interval, window_index=0, debug=False):
    """Main loop (legacy, title-based): send Enter at regular intervals."""
    print(f"[auto-enter] Starting, interval={interval}s, target='{title}'")
    print(f"[auto-enter] PID={os.getpid()}")

    if not title:
        print("[auto-enter] ERROR: --title is required to find the target window.")
        sys.exit(1)

    first_send = True

    while True:
        windows = find_window_by_title(title)
        if not windows:
            print(f"[auto-enter] WARNING: No visible window matching '{title}' found. Retrying in {interval}s...")
            time.sleep(interval)
            continue

        if window_index >= len(windows):
            print(f"[auto-enter] WARNING: window_index {window_index} >= found windows ({len(windows)}). Using index 0.")
            window_index = 0

        hwnd, win_title, proc_name = windows[window_index]
        n = send_enter_to_all(hwnd, debug=debug and first_send)
        first_send = False

        timestamp = time.strftime("%H:%M:%S")
        print(f"[auto-enter] {timestamp} -> Enter sent to '{win_title}' + children (hwnd={hwnd})")

        time.sleep(interval)


def write_pid():
    with open(PID_FILE, "w") as f:
        json.dump({"pid": os.getpid()}, f)


def read_pid():
    if os.path.exists(PID_FILE):
        with open(PID_FILE) as f:
            return json.load(f).get("pid")
    return None


def stop_existing():
    pid = read_pid()
    if pid is None:
        print("[auto-enter] No running instance found.")
        return False
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"[auto-enter] Stopped PID {pid}.")
    except OSError:
        print(f"[auto-enter] PID {pid} not running (stale).")
    finally:
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
    return True


def show_status():
    pid = read_pid()
    if pid is None:
        print("[auto-enter] No running instance.")
        return
    if _is_process_running(pid):
        print(f"[auto-enter] Running, PID={pid}")
    else:
        print("[auto-enter] Not running (stale PID file).")
        try:
            os.remove(PID_FILE)
        except Exception:
            pass


def _is_process_running(pid):
    """Windows-compatible check: use psutil if available, else tasklist."""
    try:
        import psutil
        return psutil.pid_exists(pid)
    except ImportError:
        import subprocess
        try:
            out = subprocess.check_output(
                ['tasklist', '/FI', f'PID eq {pid}'],
                stderr=subprocess.DEVNULL,
                text=True,
            )
            return str(pid) in out
        except Exception:
            return True


def list_windows(title=None):
    """List all visible windows, optionally filtered by title. Shows process names."""
    result = []
    seen_hwnds = set()

    def enum_callback(hwnd, _lparam):
        if hwnd in seen_hwnds or not user32.IsWindowVisible(hwnd):
            return True
        seen_hwnds.add(hwnd)
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            win_title = buf.value
            if title is None or title.lower() in win_title.lower():
                proc_name = get_window_process_name(hwnd)
                result.append((hwnd, win_title, proc_name))
        return True

    WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(WNDENUMPROC(enum_callback), 0)

    if title:
        print(f"Windows matching '{title}':")
    else:
        print("All visible windows:")
    for i, (hwnd, wt, proc) in enumerate(result):
        tag = " [CONSOLE]" if is_console_process(proc) else ""
        hint = " <-- likely Claude Code" if _title_has_claude_hint(wt) else ""
        print(f"  [{i}] hwnd={hwnd}  \"{wt}\"  ({proc}){tag}{hint}")


def main():
    parser = argparse.ArgumentParser(description="Auto-Enter: Send Enter key at intervals")
    parser.add_argument("--title", "-t", help="Substring to match window title (e.g. 'Claude', 'Terminal')")
    parser.add_argument("--interval", "-i", type=int, default=5, help="Interval in seconds between each Enter (default: 5)")
    parser.add_argument("--auto", "-a", action="store_true", help="Auto-detect the best console/terminal window (prefers console + Claude-related titles)")
    parser.add_argument("--debug", action="store_true", help="Show child window details on first send (for troubleshooting)")
    parser.add_argument("--list", "-l", action="store_true", help="List windows matching --title (shows process names + hints)")
    parser.add_argument("--stop", action="store_true", help="Stop running auto-enter process")
    parser.add_argument("--status", action="store_true", help="Show whether auto-enter is running")
    args = parser.parse_args()

    if args.stop:
        stop_existing()
        return
    if args.status:
        show_status()
        return
    if args.list:
        list_windows(args.title)
        return

    # Stop any existing instance first
    stop_existing()
    write_pid()

    def cleanup(signum=None, frame=None):
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        print("\n[auto-enter] Stopped.")
        sys.exit(0)

    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)

    # --- Auto-detect mode ---
    if args.auto:
        best = find_best_console_window(args.title)
        if best:
            hwnd, win_title, proc_name = best
            print(f"[auto-enter] Auto-detected: '{win_title}' ({proc_name})")
            run_loop(hwnd, win_title, args.interval, debug=args.debug)
        else:
            print("[auto-enter] ERROR: No console window found.")
            print("  Make sure your terminal with Claude Code is open and visible.")
            if args.title:
                print(f"  Title filter used: '{args.title}'")
            print("  Try: python auto_enter.py --list to see available windows.")
            sys.exit(1)
        return

    # --- Title-based mode ---
    if not args.title:
        print("[auto-enter] ERROR: --title is required (or use --auto).")
        print("  Examples:")
        print("    python auto_enter.py --list")
        print("    python auto_enter.py --auto --title Claude --interval 5")
        print("    python auto_enter.py --title \"Claude Code\" --interval 5")
        sys.exit(1)

    windows = find_window_by_title(args.title)
    if not windows:
        print(f"[auto-enter] WARNING: No visible window matching '{args.title}' found now.")
        print(f"  Will keep searching every {args.interval}s.")
    else:
        print(f"[auto-enter] Found {len(windows)} matching window(s):")
        for hwnd, wt, proc in windows:
            tag = " [CONSOLE]" if is_console_process(proc) else ""
            print(f"  hwnd={hwnd}  \"{wt}\"  ({proc}){tag}")

    run_loop_by_title(args.title, args.interval, debug=args.debug)


if __name__ == "__main__":
    main()
