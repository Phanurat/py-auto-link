import pyautogui
import time

print("Pressing Win+S to open Start menu")
pyautogui.hotkey('win', 's')
time.sleep(10)  # รอดู Start menu เปิดไหม
print("Done waiting")
