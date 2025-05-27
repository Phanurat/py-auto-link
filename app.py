from flask import Flask, render_template_string, request
import subprocess

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
    <p>ผลลัพธ์: <pre>{{ process_result }}</pre></p>
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

    # ใช้ subprocess.run รอผลลัพธ์
    result = subprocess.run(
        ['python', 'main.py', message], 
        capture_output=True, text=True
    )

    output = result.stdout or result.stderr or "No output"

    return render_template_string(HTML, process_result=output)

if __name__ == '__main__':
    app.run(host="192.168.1.140", port=4005, debug=True)
