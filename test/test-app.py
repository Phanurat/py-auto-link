from flask import Flask, render_template_string, request
import threading
import time
import pyautogui
import pyperclip
import cv2
import numpy as np
import mss
import pytesseract
from ultralytics import YOLO
import re
import json

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head><title>Detect Process</title></head>
<body>
  <h1>พิมพ์ข้อความเพื่อเปิดใน Microsoft Edge</h1>
  <form method="POST" action="/run-detect">
    <input type="text" name="message" placeholder="พิมพ์ข้อความที่นี่" required />
    <button type="submit">Run</button>
  </form>
  {% if process_result %}
    <h2>ผลลัพธ์ URL ที่ตรวจจับได้:</h2>
    <ul>
      {% for url in process_result %}
        <li>{{ url }}</li>
      {% endfor %}
    </ul>
  {% endif %}
</body>
</html>
'''

# ตัวแปรเก็บผลลัพธ์ detect URL ระหว่างรอ
detected_urls = []
detect_done = False

def process_open(message, browser_name="Microsoft Edge"):
    print("Open Program...")
    pyautogui.FAILSAFE = True
    pyautogui.hotkey('win', 's')
    time.sleep(1)
    pyperclip.copy(browser_name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(5)

    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    print("Opened Edge and navigated.")

def detect_post():
    global detected_urls, detect_done
    model = YOLO('best.onnx')  # แก้ path ตามจริง
    monitor = {
        "top": 0,
        "left": 0,
        "width": 1920 // 2,
        "height": 1080
    }
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    all_urls = set()

    with mss.mss() as sct:
        while True:
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            results = model(img)
            result = results[0]

            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            try:
                text = pytesseract.image_to_string(img_gray, lang="eng", config="--psm 6", timeout=2).strip()
            except RuntimeError:
                text = ""
                print("⚠️ OCR timeout")

            urls = re.findall(r'https?://[^\s]+', text)
            for url in urls:
                if url not in all_urls:
                    all_urls.add(url)
                    print("[Detected new URL]:", url)

            # แสดงผลบนหน้าจอ
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                label = result.names[int(box.cls[0])]
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, f"{label} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            y0 = 80
            for i, url in enumerate(sorted(all_urls)):
                cv2.putText(img, url, (10, y0 + i * 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

            cv2.imshow("YOLOv8 + OCR Link Detection", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("User exited detection window.")
                break

            if all_urls:
                break  # เจอ URL แล้วออก loop

    detected_urls = sorted(all_urls)
    detect_done = True
    cv2.destroyAllWindows()

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML)

@app.route('/run-detect', methods=['POST'])
def run_detect():
    global detected_urls, detect_done
    detected_urls = []
    detect_done = False

    message = request.form['message']
    print(f"[INFO] Received message: {message}")

    # เรียกเปิดโปรแกรมและเปิดหน้าเว็บ
    process_open(message)

    # รัน detect_post ใน thread เพื่อไม่บล็อค main thread Flask
    t = threading.Thread(target=detect_post)
    t.start()

    # รอให้ detect เสร็จ (หรือ timeout 60 วินาที)
    timeout = 60
    waited = 0
    while not detect_done and waited < timeout:
        time.sleep(1)
        waited += 1

    if not detected_urls:
        detected_urls = ["No URLs detected."]

    return render_template_string(HTML, process_result=detected_urls)

if __name__ == '__main__':
    app.run(host="192.168.1.140", port=4005, debug=True) 