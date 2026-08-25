import random
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

PROXYRACK_HOST = "premium.residential.proxyrack.net:10000"
PROXYRACK_USER = "gojyxogosutase"
PROXYRACK_PASS = "WPYV6U0-PXC4X1B-5KJAKQA-IAHTEI6-FPBHKYI-BI7X1IT-LRYHKBZ"

ALL_COUNTRIES = ['US', 'VN', 'FR', 'GB', 'DE', 'JP', 'KR', 'CA', 'AU', 'SG', 'IN', 'TH', 'AR', 'BR', 'ES', 'IT']


@app.route('/')
def home():
  return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
  data = request.get_json() or {}
  selected_country = data.get('country', 'ALL').upper()
  os_name = data.get('os', 'Windows')

  try:
    qty = int(data.get('qty', 10))
  except (ValueError, TypeError):
    qty = 10

  qty = max(1, min(qty, 100))

  proxies = []
  for _ in range(qty):
    if selected_country == 'ALL' or not selected_country:
      country = random.choice(ALL_COUNTRIES)
    else:
      country = selected_country

    sess = ''.join(
        random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=12)
    )

    proxy_str = f'{PROXYRACK_HOST}:{PROXYRACK_USER}-country-{country}-session-{sess}-osName-{os_name}:{PROXYRACK_PASS}'
    proxies.append(proxy_str)

  return jsonify({'proxies': proxies})


if __name__ == '__main__':
  app.run()
