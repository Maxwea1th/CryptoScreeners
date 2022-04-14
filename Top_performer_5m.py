import ccxt
import requests
import schedule
import time

exchange = ccxt.binanceusdm()
exchange.load_markets()

WEBHOOK_5M = 'https://discord.com/api/webhooks/963916282288300103/iinG8bi3InisjZvMv79M9v-nNGXp7vcv3WztK6HCxw93S0z9-f2P3QN1Y8TSBID2McI8'

def screener2():
    for symbol in exchange.load_markets():
        b = exchange.fetch_ohlcv(symbol, '5m')
        c = b[-1][-2]
        d = b[-2][-2]
        diff_percent = round(((c - d)/c)*100, 2)

        if diff_percent >= 2 or diff_percent <= -2:
            message = (f'{symbol}: {diff_percent}%')

            pay = {
            'username': 'Young Ian',
            'content': message
        }
            requests.post(WEBHOOK_1M, json=pay)
        else:
            pass
screener2()
