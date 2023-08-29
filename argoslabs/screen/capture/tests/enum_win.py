import win32gui

def callback(hwnd, extra):
    title = win32gui.GetWindowText(hwnd)
    if not (win32gui.IsWindowEnabled(hwnd) and 
        win32gui.IsWindowVisible(hwnd) and title):
        return
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    print("Window %s:" % title)
    print("\tLocation: (%d, %d)" % (x, y))
    print("\t    Size: (%d, %d)" % (w, h))

def main():
    win32gui.EnumWindows(callback, None)

if __name__ == '__main__':
    main()
