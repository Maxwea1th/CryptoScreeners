import ccxt
import requests
import schedule
import time

exchange = ccxt.binanceusdm()
exchange.load_markets()

WEBHOOK_1M = 'https://discord.com/api/webhooks/963913572226842725/T1Iubzybtro4DsCMZ_n6mbqFU9eePA86BMsJvktmNpH_qnLrAu9Uy9rWxMf9tvmmyvRM'
WEBHOOK_5M = 'https://discord.com/api/webhooks/963916282288300103/iinG8bi3InisjZvMv79M9v-nNGXp7vcv3WztK6HCxw93S0z9-f2P3QN1Y8TSBID2McI8'
WEBHOOK_30M = 'https://discord.com/api/webhooks/963916580440383548/1comhJ7fbpvV7g-MspH0u0arKhpUIoDN44aomxXYMECTdX9vIh2pzljmraG0eZRC3c19'
WEBHOOK_4H = 'https://discord.com/api/webhooks/963916769502826567/k8GfcsBaX9aGpg4Q5JTUMQWXPTKn5P0DLN8qB_TF_Kln1AyGecNm7hCKWMBHKGbe5Q_D'

def screener1():
    print('1min------------------------')
    for symbol in exchange.load_markets():
        print(symbol)
        b = exchange.fetch_ohlcv(symbol, '1m') #change timeframe here
        c = b[-1][-2]
        print(c)
        d = b[-2][-2]
        print(d)
        diff_percent = round(((c - d)/c)*100, 2)
        print(diff_percent)

        if diff_percent >= 0.75 or diff_percent <= -0.75: #change percentage here
            message = (f'{symbol}: {diff_percent}%')

            pay = {
            'username': 'Young Ian',
            'content': message
        }
            requests.post(WEBHOOK_1M, json=pay)
        else:
            pass

def screener2():
    print('5min---------------------')
    for symbol in exchange.load_markets():
        print(symbol)
        b = exchange.fetch_ohlcv(symbol, '5m')
        c = b[-2][-2]
        print(c)
        d = b[-3][-2]
        print(d)
        diff_percent = round(((c - d)/c)*100, 2)
        print(diff_percent)

        if diff_percent >= 1.25 or diff_percent <= -1.25:
            message = (f'{symbol}: {diff_percent}%')

            pay = {
            'username': 'Young Ian',
            'content': message
        }
            requests.post(WEBHOOK_5M, json=pay)
        else:
            pass

def screener3():
    print('30min-------------------------')
    for symbol in exchange.load_markets():
        print(symbol)
        b = exchange.fetch_ohlcv(symbol, '30m')
        c = b[-2][-2]
        print(c)
        d = b[-3][-2]
        print(d)
        diff_percent = round(((c - d)/c)*100, 2)
        print(diff_percent)

        if diff_percent >= 2 or diff_percent <= -2:
            message = (f'{symbol}: {diff_percent}%')

            pay = {
            'username': 'Young Ian',
            'content': message
        }
            requests.post(WEBHOOK_30M, json=pay)
        else:
            pass

def screener4():
    print('4h---------------------')
    for symbol in exchange.load_markets():
        print(symbol)
        b = exchange.fetch_ohlcv(symbol, '4h')
        c = b[-2][-2]
        print(c)
        d = b[-3][-2]
        print(d)
        diff_percent = round(((c - d)/c)*100, 2)
        print(diff_percent)

        if diff_percent >= 2.5 or diff_percent <= -2.5:
            message = (f'{symbol}: {diff_percent}%')

            pay = {
            'username': 'Young Ian',
            'content': message
        }
            requests.post(WEBHOOK_4H, json=pay)
        else:
            pass


schedule.every(1).minutes.do(screener1)
schedule.every(5).minutes.do(screener2)
schedule.every(30).minutes.do(screener3)
schedule.every(4).hours.do(screener4)

while True:
    schedule.run_pending()
    time.sleep(1)
