import requests
import datetime

current_time = ''

def get_info():
    global current_time
    response = requests.get(url="https://yobit.net/api/3/info")
    # https://yobit.net/api/3/info - возвращает JSON всех курсов на криптобирже
    with open(f'{current_time}_info.txt', 'w') as file:
        file.write(response.text)
    return response.text

def get_ticker(coin1="btc", coin2="usd"):   # получение курсов купли/продажи high/low/avg/vol/vol_cur/last/buy/sell
    global current_time
    response = requests.get(url=f'https://yobit.net/api/3/ticker/{coin1}_{coin2}?ignore_invalid=1')
    # изменение куросов за последние 24 часа. Для указания нескольких "пар", использут '-'
    # ?ignore_invalid=1 - игнорировать отсутсвие "пары"
    with open(f'{current_time}_{coin1}-{coin2}_ticker.txt', 'w') as file:
        file.write(response.text)
    return response.text

def get_depth(coin1="btc", coin2="usd", limit=150):
    global current_time
    response = requests.get(url=f'https://yobit.net/api/3/depth/{coin1}_{coin2}?limit={limit}&ignore_invalid=1')
    with open(f'{current_time}_{coin1}-{coin2}_depth.txt', 'w') as file:
        file.write(response.text)

    bids = response.json()[f'{coin1}_{coin2}']['bids']
    total_bids_amaunt = 0
    for item in bids:
        price = item[0]
        coin_amount = item[1]
        total_bids_amaunt += price * coin_amount
    return f'Total bids: {total_bids_amaunt} $'

def get_trades(coin1="btc", coin2="usd", limit=150):   # совершённые сделки купли и продажи
    global current_time
    total_trade_ask = 0
    total_trade_bid = 0
    response = requests.get(url=f'https://yobit.net/api/3/trades/{coin1}_{coin2}?limit={limit}&ignore_invalid=1')
    with open(f'{current_time}_{coin1}-{coin2}_trades.txt', 'w') as file:
        file.write(response.text)


    for item in response.json()[f'{coin1}_{coin2}']:
        if item['type'] == 'ask':
            total_trade_ask += item['price'] * item['amount']       # + сумма текущей сделки SELL
        else:
            total_trade_bid += item['price'] * item['amount']       # + сумма текущей сделки BUY
    info = f"[-] TOTAL {coin1} SELL: {round(total_trade_ask, 2)} $\n[+] TOTAL {coin1}  BUY: {round(total_trade_bid, 2)} $"
    return info



def main():
    global current_time
    current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    get_info()
    print()
    print()

    print(get_ticker())
    print()
    get_depth(coin1="btc", coin2="usd", limit=2000)
    print()
    print(get_trades())
    print()

if __name__ == '__main__':
    main()