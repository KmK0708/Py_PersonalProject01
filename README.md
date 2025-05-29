# 👉 코인 가격 모니터링 & 디스코드 알림 시스템 (USDT 기준)

---

## 📌 주요 기능

1. **코인 가격 조회**
   - Binance API를 통해 주요 컨 가격을 **USDT 기준**으로 가져온다.
   - 검색 가능한 코인:  
     `Bitcoin`, `Ethereum`, `XRP`, `Solana`, `Doge`, `Ondo`

2. **가격 기록 (CSV 저장)**
   - `.py` 파일이 위치한 디렉토리의 하위 폴더(`PriceData`)에
   - 코인별로 가격 기록 파일을 저장.
     - 예: `PriceData/BTCUSDT_price.csv`

3. **가격 변동 감지 및 디스코드 알림**
   - 프로그램 시작 시 기준 가격을 설정.
   - 기준 가격 대비
     - 5% 이상 상승 🚀
     - 5% 이상 하락 🚨
     시 디스코드 Webhook을 통해 실시간 알림.

4. **폴더 구조 관리**
   - `.py` 파일과 데이터(csv 파일들)을 분리해  
     `PriceData/` 하위 폴더에 저장해 프로젝트 폴더를 깔끔하게 유지.

5. **코인 이름 맞춤**
   - (BTCUSDT)이 아니라  
     **"Bitcoin", "Ethereum"** 등의 이름으로 터미널 출력 및 디스코드 알림을 제공.

---

## 🛠️ 주요 작업 내역

| 단계 | 작업 내역 |
|:--|:--|
| 1 | Binance API를 사용해 실시간 가격 가져오기 (USDT 기준) |
| 2 | 가격 정보를 CSV 파일로 저장 |
| 3 | 디스코드 Webhook 연동으로 가격 변동시 알림 |
| 4 | 검색 목록을 리스트에서 딕셔너리(코인 이름) 형식으로 변경 |
| 5 | CVS 저장 위치를 `.py` 파일과 같은 경로로 조정 |
| 6 | 프로젝트 폴더 내 `PriceData/` 하위 폴더 생성해 파일 저장 |
| 7 | 터미널 출력 및 알림 문구에 코인 심볼 대신 이름 표시 |
| 8 | 현재가 대비 ±5% 변동 감지 및 알림 조건 설정 |
| 9 | 프로그램 반복 시간을 5초 로 설정 (테스트용), 나중에 시간 조정 가능 |

---

## 📂 현재 폴더 구조

```
/프로젝트 폴더/
    ├— Py_Coinproject.py
    ├— Py_Coindict.py
    └— PriceData/
        ├— BTCUSDT_price.csv
        ├— ETHUSDT_price.csv
        ├— XRPUSDT_price.csv
        ├— SOLUSDT_price.csv
        ├— DOGEUSDT_price.csv
        └— ONDOUSDT_price.csv
```

---

## ⚙️ 추후 개선 아이디어

텔레그램 과 연동시켜서 모바일에서도 쉽게 알람받기


