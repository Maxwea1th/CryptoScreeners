import ccxt
import requests
import schedule
import time

exchange = ccxt.binanceusdm()
exchange.load_markets()

WEBHOOK_4H = 'https://discord.com/api/webhooks/963916769502826567/k8GfcsBaX9aGpg4Q5JTUMQWXPTKn5P0DLN8qB_TF_Kln1AyGecNm7hCKWMBHKGbe5Q_D'

def screener4():
    for symbol in exchange.load_markets():
        b = exchange.fetch_ohlcv(symbol, '4h')
        c = b[-1][-2]
        d = b[-2][-2]
        diff_percent = round(((c - d)/c)*100, 2)

        if diff_percent >= 5 or diff_percent <= -5:
            message = (f'{symbol}: {diff_percent}%')

            pay = {
            'username': 'Young Ian',
            'content': message
        }
            requests.post(WEBHOOK_1M, json=pay)
        else:
            pass
screener4()            
