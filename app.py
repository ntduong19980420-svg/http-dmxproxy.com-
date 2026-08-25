import random
import string
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
# Chuỗi khóa bảo mật session
app.secret_key = "dmxproxy_secret_key_super_safe"

# ================================
# CẤU HÌNH TÀI KHOẢN VÀ MẬT KHẨU
# ================================
ADMIN_USERNAME = ""        # Tên tài khoản
ADMIN_PASSWORD = "123456"          # Mật khẩu đăng nhập

@app.route('/')
def home():
    # Kiểm tra xem người dùng đã đăng nhập chưa
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
    base_user = "gojyxogosutase"
    pass_key = "WPYV6U0-PXC4X1B-5KJAKQA-IAHTEI6-FPBHKYI-BI7X1IT-LRYHKBZ"

    for _ in range(qty):
        session_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        
        country_param = ""
        if country and country != 'ALL':
            country_param = f"-country-{country}"

        proxy_str = f"{base_host}:{base_user}{country_param}-session-{session_id}-osName-{os_name}:{pass_key}"
        proxies.append(proxy_str)

    return jsonify({"proxies": proxies})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)