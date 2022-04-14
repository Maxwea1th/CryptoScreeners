import ccxt
import requests
import schedule
import time

exchange = ccxt.binanceusdm()
exchange.load_markets()

WEBHOOK_1M = 'https://discord.com/api/webhooks/963913572226842725/T1Iubzybtro4DsCMZ_n6mbqFU9eePA86BMsJvktmNpH_qnLrAu9Uy9rWxMf9tvmmyvRM'

def screener1():
    for symbol in exchange.load_markets():
        b = exchange.fetch_ohlcv(symbol, '1m') #change timeframe here
        c = b[-1][-2]
        d = b[-2][-2]
        diff_percent = round(((c - d)/c)*100, 2)

        if diff_percent >= 1 or diff_percent <= -1: #change percentage here
            message = (f'{symbol}: {diff_percent}%')

            pay = {
            'username': 'Young Ian',
            'content': message
        }
            requests.post(WEBHOOK_1M, json=pay)
        else:
            pass
 
screener1()
