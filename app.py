import random
import string
import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "dmxproxy_secret_key_super_safe"

# ================================
# CẤU HÌNH TÀI KHOẢN VÀ MẬT KHẨU
# ================================
ADMIN_USERNAME = "DMXProxy"        # Tên tài khoản
ADMIN_PASSWORD = "123456"          # Mật khẩu đăng nhập

# Thông tin tài khoản Proxyrack
PROXY_USER = "gojyxogosutase"
PROXY_PASS = "WPYV6U0-PXC4X1B-5KJAKQA-IAHTEI6-FPBHKYI-BI7X1IT-LRYHKBZ"

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            error = "Tài khoản hoặc mật khẩu không chính xác!"

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Endpoint lấy dung lượng GB thực tế còn lại từ Proxyrack API
@app.route('/get_stats', methods=['GET'])
def get_stats():
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        # Gọi API của Proxyrack để lấy thống kê dữ liệu
        proxies = {
            "http": f"http://{PROXY_USER}:{PROXY_PASS}@premium.residential.proxyrack.net:10000",
            "https": f"http://{PROXY_USER}:{PROXY_PASS}@premium.residential.proxyrack.net:10000"
        }
        res = requests.get("http://api.proxyrack.net/stats", proxies=proxies, timeout=5)
        data = res.json()
        
        # Lấy thông tin bytes_remaining hoặc calculate
        bytes_left = data.get('bytes_remaining') or data.get('transfer_remaining', 0)
        gb_left = round(bytes_left / (1024 ** 3), 1) if bytes_left else 0.0
        return jsonify({"gb_left": gb_left, "raw": data})
    except Exception as e:
        # Nếu có lỗi kết nối, trả về mặc định hoặc 0
        return jsonify({"gb_left": "43.0", "error": str(e)})

@app.route('/generate', methods=['POST'])
def generate():
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json or {}
    country = data.get('country', 'ALL')
    os_name = data.get('os', 'Windows')
    qty = int(data.get('qty', 10))

    proxies = []
    base_host = "premium.residential.proxyrack.net:10000"

    for _ in range(qty):
        session_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        
        country_param = ""
        if country and country != 'ALL':
            country_param = f"-country-{country}"

        proxy_str = f"{base_host}:{PROXY_USER}{country_param}-session-{session_id}-osName-{os_name}:{PROXY_PASS}"
        proxies.append(proxy_str)

    return jsonify({"proxies": proxies})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)