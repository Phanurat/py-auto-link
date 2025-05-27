from flask import Flask, render_template_string, request
import subprocess
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
  {% if error_msg %}
    <p style="color:red;">{{ error_msg }}</p>
  {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML)

@app.route('/run-detect', methods=['POST'])
def run_detect():
    message = request.form['message']
    print(f"[INFO] Received message: {message}")

    try:
        result = subprocess.run(
            ['python', 'main.py', message],
            capture_output=True,
            text=True,
            timeout=120  # กำหนด timeout เผื่อ process รันนานเกินไป
        )
    except subprocess.TimeoutExpired:
        return render_template_string(HTML, error_msg="Process timed out. กรุณาลองใหม่อีกครั้ง.")

    print(f"[INFO] Subprocess stdout:\n{result.stdout}")
    print(f"[INFO] Subprocess stderr:\n{result.stderr}")

    output = result.stdout or result.stderr or ""

    lines = output.splitlines()
    json_str = None
    for line in lines:
        if line.startswith("Detect result:"):
            json_str = line[len("Detect result:"):].strip()
            break

    if json_str:
        try:
            urls = json.loads(json_str)
        except json.JSONDecodeError:
            urls = ["Error decoding JSON output."]
    else:
        urls = ["No URLs detected."]

    return render_template_string(HTML, process_result=urls)

if __name__ == '__main__':
    app.run(host="192.168.1.140", port=4005, debug=True)
