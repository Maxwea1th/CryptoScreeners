import ccxt
import requests
import schedule
import time

exchange = ccxt.binanceusdm()
exchange.load_markets()

WEBHOOK_30M = 'https://discord.com/api/webhooks/963916580440383548/1comhJ7fbpvV7g-MspH0u0arKhpUIoDN44aomxXYMECTdX9vIh2pzljmraG0eZRC3c19'

def screener3():
    for symbol in exchange.load_markets():
        b = exchange.fetch_ohlcv(symbol, '30m')
        c = b[-1][-2]
        d = b[-2][-2]
        diff_percent = round(((c - d)/c)*100, 2)

        if diff_percent >= 3 or diff_percent <= -3:
            message = (f'{symbol}: {diff_percent}%')

            pay = {
            'username': 'Young Ian',
            'content': message
        }
            requests.post(WEBHOOK_1M, json=pay)
        else:
            pass
screener3()           
