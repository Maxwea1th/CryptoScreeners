import ccxt
import schedule
import time
import requests
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
from ta.momentum import RSIIndicator


exchange = ccxt.binanceusdm()



def volatility_bot():
    overbought_count = 0
    oversold_count = 0

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(f"This screening started at {current_time}")

    open('list_overbought.txt', 'w').close()
    open('list_oversold.txt', 'w').close()

    for symbol in exchange.load_markets():
        bars = exchange.fetch_ohlcv(symbol, timeframe='30m', limit=365)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        rsi_indicator = RSIIndicator(df['close'])
        df['rsi_%'] = rsi_indicator.rsi()
        df['overbought'] = rsi_indicator.rsi() >= 66.5
        df['oversold'] = rsi_indicator.rsi() <= 33.5

        last_row = df.iloc[-1]

        if last_row['overbought'] == True:
            overbought_count += 1

            tracking = f'BINANCE:{symbol}.,'
            with open('list_overbought.txt', 'a') as f:
                for tvlist in tracking:
                    tvlist_final = tvlist.replace('/', '')
                    tvlist_perp = tvlist_final.replace('.','PERP')
                    f.write(tvlist_perp)

        elif last_row['oversold'] == True:
            oversold_count += 1

            tracking = f'BINANCE:{symbol}.,'
            with open('list_oversold.txt', 'a') as f:
                for tvlist in tracking:
                    tvlist_final = tvlist.replace('/', '')
                    tv_perp = tvlist_final.replace('.', 'PERP')
                    f.write(tv_perp)

        else:
            pass

    WEBHOOK_BUYSELL = 'https://discord.com/api/webhooks/961090854393634846/CIhNIeKs0hCm1PAer5-4Z0Ttm_UMVrk96E-qxzP1Jal7EnohexHTwiEBPoFg3M7xT3hb'
    WEBHOOK_VOLATILITY = 'https://discord.com/api/webhooks/954915040253849650/uDcwltzP-GPYX-9AhOSeWK85iJLgNyFu-eF5cQYy2CWVld3fygRRTQxGVPUg5s10hUKJ'

    # if overbought_count >= 25:
    #     message = ('SHORT opportunity incoming.')
    #
    #     payload = {
    #         'username': 'Young Ian',
    #         'content': message
    #     }
    #     requests.post(WEBHOOK_BUYSELL, json=payload)
    #
    # if overbought_count >= 50:
    #     message = ('SHORT opportunity is here.')
    #
    #     payload = {
    #         'username': 'Young Ian',
    #         'content': message
    #     }
    #     requests.post(WEBHOOK_BUYSELL, json=payload)
    #
    # if overbought_count >= 75:
    #     message = ('SHORT something!')
    #
    #     payload = {
    #         'username': 'Young Ian',
    #         'content': message
    #     }
    #     requests.post(WEBHOOK_BUYSELL, json=payload)
    #
    # if overbought_count >= 100:
    #     message = ('SHORT ANYTHING!')
    #
    #     payload = {
    #         'username': 'Young Ian',
    #         'content': message
    #     }
    #     requests.post(WEBHOOK_BUYSELL, json=payload)
    #
    # if oversold_count >= 25:
    #     message = ('LONG opportunity incoming.')
    #
    #     payload = {
    #         'username': 'Young Ian',
    #         'content': message
    #     }
    #     requests.post(WEBHOOK_BUYSELL, json=payload)
    #
    # if oversold_count >= 50:
    #     message = ('LONG opportunity is here.')
    #
    #     payload = {
    #         'username': 'Young Ian',
    #         'content': message
    #     }
    #     requests.post(WEBHOOK_BUYSELL, json=payload)
    #
    # if oversold_count >= 75:
    #     message = ('LONG something!')
    #
    #     payload = {
    #         'username': 'Young Ian',
    #         'content': message
    #     }
    #     requests.post(WEBHOOK_BUYSELL, json=payload)
    #
    # if oversold_count >= 100:
    #     message = ('LONG ANYTHING!')
    #
    #     payload = {
    #         'username': 'Young Ian',
    #         'content': message
    #     }
    #     requests.post(WEBHOOK_BUYSELL, json=payload)
    # else:
    #     pass


    message = (f'Overbought: {overbought_count}    Oversold: {oversold_count}')
    payload = {
        'username': 'Young Ian',
        'content': message
    }
    requests.post(WEBHOOK_VOLATILITY, json=payload)


    file_overbought = {'file': open('list_overbought.txt', 'rb')}
    requests.post(WEBHOOK_VOLATILITY, files=file_overbought)

    file_oversold = {'file': open('list_oversold.txt', 'rb')}
    requests.post(WEBHOOK_VOLATILITY, files=file_oversold)

    print(f"This screening ended at {current_time}")


volatility_bot()

# schedule.every(30).minutes.do(volatility_bot)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
