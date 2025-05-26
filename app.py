from flask import Flask, render_template_string, redirect, url_for
import subprocess

app = Flask(__name__)

# หน้าเว็บ มีปุ่มกด
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Run main.py</title>
</head>
<body>
    <h1>กดปุ่มเพื่อเรียกใช้งาน main.py</h1>
    <form action="/run" method="post">
        <button type="submit">Run main.py</button>
    </form>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/run', methods=['POST'])
def run_main():
    try:
        # เรียกไฟล์ main.py ด้วย subprocess
        subprocess.Popen(['python', 'main.py'])
    except Exception as e:
        return f"Error: {e}"
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='192.168.1.154', port=4005, debug=True)
