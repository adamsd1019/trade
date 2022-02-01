import json
import argparse
import requests
from datetime import datetime, timezone

def _argparse():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Process arguments')
    parser.add_argument('-t', '--ticker', default=False, help='Specific ticker to use')
    parser.add_argument('-o','--options', action='store_true', help='Toggle for options chain')
    parser.add_argument('-wl', '--watchlist', action='store_true', help='Check tickers on watchlist')
    parser.add_argument('-m', '--movers', action='store_true', help='Check index movers')
    args = parser.parse_args()
    return args

def readConfig(filepath):
    with open(filepath, 'r') as myfile:
        data = myfile.read()
    config = json.loads(data)
    return config['key']

def timestamp():
    today = datetime.today()
    return today.replace(tzinfo=timezone.utc).timestamp() * 1000

def get_data(ticker, key):
    # saves one minute candle data for the last 5 days to json file
    # content returns as a dictionary
    epoch = int(timestamp())
    if ',' in ticker:
        stock_endpoint = 'https://api.tdameritrade.com/v1/marketdata/quotes?symbol=' + ticker
    else:
        # stock_endpoint = f'https://api.tdameritrade.com/v1/marketdata/{ticker}/quotes?'
        stock_endpoint = f'https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory?periodType=day&period=5&frequencyType=minute&frequency=1&endDate={epoch}'
    page = requests.get(url=stock_endpoint,
                        params={'apikey': key})
    return json.loads(page.content)

def moversByIndex(key):
    # gets data on what's moving based on index
    indexes = ['DJI', 'COMPX', 'SPX.X']
    contents = []
    for index in indexes:
        stock_endpoint = f'https://api.tdameritrade.com/v1/marketdata/${index}/movers'
        page = requests.get(url=stock_endpoint,
                    params={'apikey': key,
                            'direction': 'up',
                            'change': 'percent'})
        contents.append(json.loads(page.content))
    return contents

def main():
    args = _argparse()
    config_file = 'config.json'
    # data_file = 'stock_data.json'
    key = readConfig(config_file)

    if args.ticker:
        print(get_data(args.ticker, key))
    elif args.movers:
        for content in moversByIndex(key):
            print(content)
    elif args.watchlist:
        with open('watchlist.txt', 'r') as file:
            watchlist = file.readlines()
        for ticker in watchlist:
            new_watchlist = []
            for ticker in watchlist:
                new_watchlist.append(ticker.strip())
            print(get_data(str(new_watchlist).replace('[', '').replace(']', '').replace("'", '').replace(' ', ''), key))

    exit()

if __name__ == '__main__':
    main()