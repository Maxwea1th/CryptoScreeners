import ccxt
import pandas as pd
import requests
from ta.trend import EMAIndicator

exchange = ccxt.binanceusdm()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def trend():
    uptrend = 0
    downtrend = 0

    for symbol in exchange.load_markets():
        bars = exchange.fetch_ohlcv(symbol, timeframe='30m', limit=365)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        ema50 = EMAIndicator(df['close'], window=50)
        ema200 = EMAIndicator(df['close'], window=200)
        df['50ema'] = ema50.ema_indicator()
        df['200ema'] = ema200.ema_indicator()

        last_row = df.iloc[-1]

        if last_row['50ema'] > last_row['200ema']:
            uptrend += 1

        elif last_row['50ema'] < last_row['200ema']:
            downtrend += 1

        else:
            pass

    WEBHOOK_TREND = 'https://discord.com/api/webhooks/963993186995425291/5hH991fdf7e9O62AQXsia6yYBSH3DrA1s3rk1aIDK1EQScZ5Ze8XXeNbhqxP7N5O5OSE'

    message = f'Uptrend: {uptrend} // Downtrend: {downtrend}'

    payload = {
        'username': 'Young Ian',
        'content': message
    }
    requests.post(WEBHOOK_TREND, json=payload)


trend()
