import requests
import csv
from datetime import datetime
import time
import os

#디스코드 웹훅 주소
WEBHOOK_URL = "https://discord.com/api/webhooks/1365705287071432714/br-fizLEvugPrHnWjFyKgfksuYicrlI2tGsCtpNDTnpug62e1pPksYngjEkgVHzMzGeC"

# 감시할 코인 딕셔너리
coin_names = {
    'BTCUSDT': 'Bitcoin',
    'ETHUSDT': 'Ethereum',
    'XRPUSDT': 'XRP',
    'SOLUSDT': 'Solana',
    'DOGEUSDT': 'Doge',
    'ONDOUSDT': 'Ondo'
}  
# 비트코인, 이더리움, 리플 , 솔라나...

#디스코드 웹훅으로 디스코드에 알람보내기 함수
def send_discord_alert(message, webhook_url):
    """
    디스코드 웹훅을 이용해 알림 보내기
    """
    print("🔔 디스코드 알림 보내는 중입니다...")
    data = {"content": message}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, json=data, headers=headers)

    print(f"응답 코드: {response.status_code}")
    print(f"응답 내용: {response.text}")

    if response.status_code == 204:
        print("✅ 알림 발송 성공")
    else:
        print("❌ 알림 발송 실패")

def get_coin_price(symbol):
    """
    바이낸스에서 코인 현재 가격 가져오기 (USDT 기준)
    """
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    if 'price' not in data:
        print(f"바이낸스로부터 {symbol} 가격 정보를 받아오지 못했습니다.")
        return None
    return float(data['price'])

# 현재 .py 파일이 있는 폴더 경로 얻기
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 저장할 하위 폴더 이름
SUBFOLDER = "PriceData"

# 하위 폴더 전체 경로
SAVE_DIR = os.path.join(BASE_DIR, SUBFOLDER)

# 하위 폴더가 없으면 자동으로 생성
os.makedirs(SAVE_DIR, exist_ok=True)

def save_price_to_csv(symbol,time_str, price):
    """
    현재 시간과 가격 정보를 CSV 파일에 기록
    """
    filename = os.path.join(SAVE_DIR, f"{symbol}_price.csv")  # 파일 경로를 현재 폴더에 맞춤
    try:
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([time_str, price])
        # 코인 이름 출력
        coin_name = coin_names.get(symbol, symbol)
        print(f"[{coin_name}] {time_str} 가격 {price:.4f} USDT 저장 완료 (파일: {filename})")
    except Exception as e:
        print(f"❗ 파일 저장 실패: {symbol} ({e})")


# 프로그램 시작 시, 코인별 기준 가격 설정
baseline_prices = {}

for symbol in coin_names: # 코인리스트에 있는 코인들을 하나씩 순회
    price = get_coin_price(symbol)
    if price is None:
        print(f"⚠️ {symbol} 기준 가격 설정 실패. 프로그램 종료.")
        exit()
    baseline_prices[symbol] = price
    print(f"[{symbol}] 기준 가격 설정 완료: {price} 원")

# 디스코드로 전체 시작 알림
send_discord_alert("✅ 여러 코인 모니터링 시작합니다!", WEBHOOK_URL)

# 반복 실행 (5초마다 테스트 => 5분으로 수정할것)
while True:
    for symbol in coin_names:
        current_price = get_coin_price(symbol)
        if current_price is None:
            print(f"⚠️ {symbol} 가격 불러오기 실패. 스킵합니다.")
            continue

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_price_to_csv(symbol, now, current_price)

        baseline_price = baseline_prices[symbol]

        # 조건 체크: 현재 가격이 기준 가격의 95% 이하인 경우 (-5%)
        if current_price < baseline_price * 0.95:
            coin_name = coin_names.get(symbol, symbol)  # 이름 찾고, 없으면 심볼 그대로
            alert_msg = f"🚨 [{coin_name}] 가격 하락! 현재 {current_price:.2f} 달러 (기준가 대비 5% 하락)"
            send_discord_alert(alert_msg, WEBHOOK_URL)

        # 조건 체크: 현재 가격이 기준 가격의 105% 이상인 경우 (+5%)
        elif current_price > baseline_price * 1.05:
            coin_name = coin_names.get(symbol, symbol)
            alert_msg = f"🚀 [{coin_name}] 가격 상승! 현재 {current_price:.2f} 달러 (기준가 대비 5% 상승)"
            send_discord_alert(alert_msg, WEBHOOK_URL)

    # 5초 대기 (테스트용) → 실제 운영할 때는 300초(5분) 추천
    time.sleep(5)
