from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import random
import string
from functools import wraps

app = Flask(__name__)
app.secret_key = "proxyrack_secret_key_mas_proxy_2026"

# =========================================================
# 1. CẤU HÌNH TÀI KHOẢN ĐĂNG NHẬP TOOL (LOGIN)
# =========================================================
ADMIN_USER = "DMXProxy"      # Tên đăng nhập web
ADMIN_PASS = "123456"          # Mật khẩu web (bạn có thể đổi thành mật khẩu tùy thích)

# =========================================================
# 2. CẤU HÌNH TÀI KHOẢN PROXYRACK CỦA BẠN (DASHBOARD)
# =========================================================
PROXYRACK_USER = "gojyxogosutase"
PROXYRACK_PASS = "WPYV6U0-PXC4X1B-5KJAKQA-IAHTEI6-FPBHKYI-BI7X1IT-LRYHKBZ"

# Server Host & Port Premium Residential của bạn
PROXYRACK_HOST = "premium.residential.proxyrack.net"
PROXYRACK_PORT = "10000"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def generate_random_session(length=14):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = "Tài khoản hoặc mật khẩu không chính xác!"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html', user=session.get('username', 'dungnguyen'))

@app.route('/api/generate', methods=['POST'])
@login_required
def generate_proxies():
    data = request.json or {}
    country = data.get('country', 'FR')
    city = data.get('city', 'Random')
    os_name = data.get('os', 'Windows')
    qty = int(data.get('qty', 10))

    proxies = []
    for i in range(qty):
        session_id = generate_random_session(14)
        
        # Build Username string chuẩn Proxyrack / MAS Group
        user_parts = [PROXYRACK_USER]
        if country != "ALL":
            user_parts.append(f"country-{country}")
        if city != "Random":
            user_parts.append(f"city-{city}")
        user_parts.append(f"session-{session_id}")
        user_parts.append(f"osName-{os_name}")
        
        user_auth = "-".join(user_parts)
        proxy_str = f"{PROXYRACK_HOST}:{PROXYRACK_PORT}:{user_auth}:{PROXYRACK_PASS}"
        
        # Tạo IP hiển thị mẫu chuẩn giao diện (Exit IP)
        fake_ip = f"{random.randint(70, 95)}.{random.randint(10, 200)}.{random.randint(10, 200)}.{random.randint(10, 250)}"
        
        proxies.append({
            "id": i + 1,
            "proxy": proxy_str,
            "exit_ip": fake_ip
        })

    return jsonify({"status": "success", "count": len(proxies), "proxies": proxies})

if __name__ == '__main__':
    # Chạy cổng 80 để truy cập trực tiếp bằng localhost hoặc IP máy
    app.run(host='0.0.0.0', port=80, debug=True)