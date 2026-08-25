import random
import requests
import concurrent.futures
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# --- CẤU HÌNH TÀI KHOẢN PROXYRACK ---
PROXYRACK_HOST = "premium.residential.proxyrack.net:10000"
PROXYRACK_USER = "gojyxogosutase"
PROXYRACK_PASS = "WPYV6U0-PXC4X1B-5KJAKQA-IAHTEI6-FPBHKYI-BI7X1IT-LRYHKBZ"

# Dịch vụ để check IP thực tế
IP_CHECK_URL = "https://api.ipify.org?format=text"

ALL_COUNTRIES = ['US', 'VN', 'FR', 'GB', 'DE', 'JP', 'KR', 'CA', 'AU', 'SG', 'IN', 'TH']

# Hàm check IP của một proxy cụ thể
def get_proxy_exit_ip(proxy_str):
    proxy_parts = proxy_str.split(':')
    if len(proxy_parts) != 4:
        return proxy_str, "Format Error"
    
    host, port, user, password = proxy_parts
    proxies = {
        "http": f"http://{user}:{password}@{host}:{port}",
        "https": f"http://{user}:{password}@{host}:{port}",
    }
    
    try:
        # Gửi request qua proxy với timeout ngắn
        response = requests.get(IP_CHECK_URL, proxies=proxies, timeout=5)
        if response.status_code == 200:
            return proxy_str, response.text
    except Exception:
        pass
    
    return proxy_str, "Check Failed"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json() or {}
    selected_country = data.get('country', 'all').upper()
    os_name = data.get('os', 'Windows')
    qty = int(data.get('qty', 10))
    # Giới hạn số lượng check cùng lúc để tránh lag server
    qty = min(qty, 20) 

    temp_proxies = []

    for _ in range(qty):
        country = random.choice(ALL_COUNTRIES) if selected_country in ['ALL', ''] else selected_country
        sess = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=12))
        proxy_str = f'{PROXYRACK_HOST}:{PROXYRACK_USER}-country-{country}-session-{sess}-osName-{os_name}:{PROXYRACK_PASS}'
        temp_proxies.append(proxy_str)

    # Sử dụng ThreadPool để check nhiều proxy cùng lúc
    proxy_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_proxy = {executor.submit(get_proxy_exit_ip, p): p for p in temp_proxies}
        for future in concurrent.futures.as_completed(future_to_proxy):
            proxy, exit_ip = future.result()
            proxy_data.append({
                'proxy': proxy,
                'exit_ip': exit_ip
            })

    # Sắp xếp lại cho đúng thứ tự ban đầu
    sorted_data = []
    for p_str in temp_proxies:
        for item in proxy_data:
            if item['proxy'] == p_str:
                sorted_data.append(item)
                break

    return jsonify({'proxies': sorted_data})

if __name__ == '__main__':
    app.run()
