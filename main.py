import sys
import time
import pyautogui
import pyperclip
import random

pyautogui.FAILSAFE = True

def process_open(message, browser_name="Microsoft Edge"):
    print("Open Program...")  # แสดงสถานะ
    pyautogui.hotkey('win', 's')
    time.sleep(1)
    pyperclip.copy(browser_name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(4)

    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)

    pyautogui.hotkey('alt', 'f4')

def detect_post():
    print("Processing Detect...")
    time.sleep(3)
    detect_options = ['links', 'posts', 'posts']
    result = random.choice(detect_options)
    return result

def send_detect(process_box):
    print(f"Detect result: {process_box}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No message provided")
        sys.exit(1)

    msg = sys.argv[1]
    process_open(msg)
    result = detect_post()
    send_detect(result)
