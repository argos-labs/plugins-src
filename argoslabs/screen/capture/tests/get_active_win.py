import win32gui, win32process, psutil


################################################################################
def callback(hwnd, pid):
    b_found = False
    win_pids = win32process.GetWindowThreadProcessId(hwnd)
    if isinstance(pid, (list, tuple)):
        for _pid in pid:
            if _pid in win_pids:
                b_found = True
                break
    if not b_found:
        return
    title = win32gui.GetWindowText(hwnd)
    if not (win32gui.IsWindowEnabled(hwnd) and
        win32gui.IsWindowVisible(hwnd)):
        return
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    print(f'pid={pid}, hwnd-pids={win_pids}')
    print("Window %s:" % title)
    print("\tLocation: (%d, %d)" % (x, y))
    print("\t    Size: (%d, %d)" % (w, h))


################################################################################
def active_window_process_name():
    try:
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        # return(psutil.Process(pid[-1]).name())
        win32gui.EnumWindows(callback, pid)
    except:
        pass

active_window_process_name()