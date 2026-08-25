import random
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# --- CẤU HÌNH TÀI KHOẢN PROXYRACK CỦA BẠN ---
PROXYRACK_HOST = "premium.residential.proxyrack.net:10000"
PROXYRACK_USER = "gojyxogosutase"
PROXYRACK_PASS = "WPYV6U0-PXC4X1B-5KJAKQA-IAHTEI6-FPBHKYI-BI7X1IT-LRYHKBZ"

# Danh sách quốc gia phổ biến dùng để random khi chọn 'All Countries'
ALL_COUNTRIES = [
    'US',
    'VN',
    'FR',
    'GB',
    'DE',
    'JP',
    'KR',
    'CA',
    'AU',
    'SG',
    'IN',
    'TH',
]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json() or {}
    selected_country = data.get('country', 'all').upper()
    os_name = data.get('os', 'Windows')
    qty = int(data.get('qty', 10))

    proxies = []

    for _ in range(qty):
        # Chọn ngẫu nhiên quốc gia nếu người dùng chọn 'All Countries'
        if selected_country in ['ALL', '']:
            country = random.choice(ALL_COUNTRIES)
        else:
            country = selected_country

        # Tạo Session ID ngẫu nhiên cho mỗi dòng proxy
        sess = ''.join(
            random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=12)
        )

        # Định dạng chuỗi Proxyrack chuẩn
        proxy_str = f'{PROXYRACK_HOST}:{PROXYRACK_USER}-country-{country}-session-{sess}-osName-{os_name}:{PROXYRACK_PASS}'
        proxies.append(proxy_str)

    return jsonify({'proxies': proxies})


if __name__ == '__main__':
    app.run()
