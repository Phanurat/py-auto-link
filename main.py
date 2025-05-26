import pyautogui
import time

# รอให้ผู้ใช้เตรียมตัว
time.sleep(2)

# 1. เปิด Search ด้วย Win + S
pyautogui.hotkey('win', 's')
time.sleep(1)

# 2. พิมพ์ 'edge'
pyautogui.write('edge', interval=0.1)
time.sleep(1)

# 3. กด Enter เพื่อเปิด Edge
pyautogui.press('enter')

# 4. รอให้ Edge เปิด (อาจต้องปรับเวลาให้เหมาะกับเครื่อง)
time.sleep(5)

# 5. พิมพ์ URL
pyautogui.write('https://facebook.com', interval=0.1)
pyautogui.press('enter')
