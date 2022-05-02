import ccxt
import requests
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

exchange = ccxt.binanceusdm()

def s1():
    long = 0
    short = 0

    open('list_s1_short.txt', 'w').close()
    open('list_s1_long.txt', 'w').close()

    for symbol in exchange.load_markets():
        bars = exchange.fetch_ohlcv(symbol, timeframe='30m', limit=365)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        rsi_indicator = RSIIndicator(df['close'])
        df['rsi_%'] = rsi_indicator.rsi()
        df['overbought'] = rsi_indicator.rsi() >= 66.5
        df['oversold'] = rsi_indicator.rsi() <= 33.5

        ema50 = EMAIndicator(df['close'], window=50)
        ema200 = EMAIndicator(df['close'], window=200)
        df['50ema'] = ema50.ema_indicator()
        df['200ema'] = ema200.ema_indicator()

        last_row = df.iloc[-1]

        if last_row['overbought'] == True and last_row['50ema'] < last_row['200ema']:
            short += 1
            tracking = f'BINANCE:{symbol}.,'
            with open('list_s1_short.txt', 'a') as f:
                for tvlist in tracking:
                    tvlist_final = tvlist.replace('/', '')
                    tvlist_perp = tvlist_final.replace('.','PERP')
                    f.write(tvlist_perp)


        elif last_row['oversold'] == True and last_row['50ema'] > last_row['200ema']:
            long += 1
            tracking = f'BINANCE:{symbol}.,'
            with open('list_s1_long.txt', 'a') as f:
                for tvlist in tracking:
                    tvlist_final = tvlist.replace('/', '')
                    tvlist_perp = tvlist_final.replace('.','PERP')
                    f.write(tvlist_perp)
        else:
            pass

    WEBHOOK_S1 = 'https://discord.com/api/webhooks/'

    message1 = f'Long opportunity: {long}'
    payload1 = {
        'username': 'Young Ian',
        'content': message1
    }

    message2 = f'Short opportunity: {short}.'
    payload2 = {
        'username': 'Young Ian',
        'content': message2
    }

    file_short = {'file': open('list_s1_short.txt', 'rb')}
    file_long = {'file': open('list_s1_long.txt', 'rb')}

    requests.post(WEBHOOK_S1, json=payload1)
    requests.post(WEBHOOK_S1, files=file_long)

    requests.post(WEBHOOK_S1, json=payload2)
    requests.post(WEBHOOK_S1, files=file_short)



s1()
