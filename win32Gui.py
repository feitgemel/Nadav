import sys
import win32gui
import win32con
import time

time.sleep(2)

#hwnd = win32gui.FindWindow(None, "zoom.txt - notepad") 
hwnd = win32gui.FindWindow(None, "Grid 3 - Nadav - Home") 

print(hwnd) 

win32gui.ShowWindow(hwnd,5)
win32gui.SetForegroundWindow(hwnd)
win32gui.BringWindowToTop(hwnd)
win32gui.SetWindowPos(
        hwnd, win32con.HWND_TOP,
        -0, -0, 1000, 600,
        0
    )


rect = win32gui.GetWindowRect(hwnd)


print(rect) 