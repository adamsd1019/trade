'''
    Program to collect data and place trades

    To-Do List:
        aggregate data from last 60 minutes of running get_data to make hourly candle
            use first get_data openPrice and last get_data closePrice

    Strategy:
        Need to use stock data to trade one stock
        base trades on 200ema crosses on the hourly chart
'''
import requests
import json
import argparse
from time import localtime, strftime


def _argparse():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description='Process arguments')
    parser.add_argument('-t', '--ticker', type=str, help='Specific ticker to use')
    parser.add_argument('-o','--options', action='store_true', help='Toggle for options chain')
    parser.add_argument('--hourly', action='store_true', help='Get hourly candle data')

    args = parser.parse_args()
    return args


def get_data(ticker, key):
    # Collect stock data from tdapi from a specific ticker
    # ticker_data returns as a dictionary
    # returns last one minute candle data
    stock_endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/quotes?'
    full_url = stock_endpoint.format(stock_ticker=ticker)
    page = requests.get(url=full_url,
                    params={'apikey': key})
    content = json.loads(page.content)
    ticker_data = content[ticker].items()

    return ticker_data


def get_candles(ticker, key):
    historical_endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&period={period}&frequencyType={frequencyType}&frequency={frequency}'
    full_url = historical_endpoint.format(stock_ticker=ticker,
                                            periodType='day',
                                            period=1,
                                            frequencyType='minute',
                                            frequency=30)
    page = requests.get(url=full_url, params={'apikey': key})
    content = json.loads(page.content)
    data = content['candles']
    for d in data:
        epoch = d['datetime']
        date = localtime(epoch/1000)
        print(strftime('%m/%d/%Y %H:%M', date))
        print('open=' + str(d['open']))
        print('close=' + str(d['close']))
        

    exit()  
    candle_open = data[-2]['open']
    candle_close = data[-1]['close']
    print(candle_open)
    print(candle_close)
    exit()  
    candle = []
    candle_open = minute1['open']
    candle_close = minute60['close']

    print()

    exit()

    return hourly_data


def get_options(ticker, key):
    # Collect options data from tdapi from a specific ticker
    # ticker_data returns as a dictionary
    options_endpoint = 'https://api.tdameritrade.com/v1/marketdata/chains?&symbol={stock_ticker}'
    full_url = options_endpoint.format(stock_ticker=ticker)
    page = requests.get(url=full_url,
                    params={'apikey': key})
    options_data = json.loads(page.content)

    result = []
    for date, value in options_data['callExpDateMap'].items():
        inTM = 0
        ninTM = 0
        date_array = date.split(":")
        if int(date_array[1]) <= 30:
            for key, data in value.items():
                for d in data:
                    if 'CALL' == d['putCall']:
                        if d['inTheMoney'] is True and inTM != 3:
                            result.append(d)
                            inTM += 1
                        elif d['inTheMoney'] is False and ninTM != 3:
                            result.append(d)
                            ninTM += 1

    return result


def main():
    args = _argparse()

    with open('config.json', 'r') as myfile:
        data = myfile.read()
    config = json.loads(data)

    key = config['key']

    if args.ticker and args.options == True:
        options = get_options(args.ticker, key)
        for option in options:
            print("description: " + option['description'] + "\tbid: " + str(option['bid']) + "\task: " + str(option['ask']))
            # print(option.keys())
    elif args.ticker and args.hourly == True:
        hourly_data = get_candles(args.ticker, key)
        for data in hourly_data:
            print('open = ' + data['openPrice'])
            print('close = ' + data['closePrice'])
            exit()
    elif args.ticker:
        ticker_data = get_data(args.ticker, key)
        for k,v in ticker_data:
            print(k,v)

    exit()


if __name__ == "__main__":
    main()
