import json
import argparse
import requests

def _argparse():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Process arguments')
    parser.add_argument('-t', '--ticker', default=False, help='Specific ticker to use')
    parser.add_argument('-o','--options', action='store_true', help='Toggle for options chain')
    parser.add_argument('-wl', '--watchlist', action='store_true', help='Check tickers on watchlist')
    args = parser.parse_args()
    return args

def readConfig(filepath):
    with open(filepath, 'r') as myfile:
        data = myfile.read()
    config = json.loads(data)
    return config['key']

def get_data(ticker, key):
    # Collect stock data from tdapi from a specific ticker
    # ticker_data returns as a dictionary
    # returns last one minute candle data
    if ',' in ticker:
        stock_endpoint = 'https://api.tdameritrade.com/v1/marketdata/quotes?symbol=' + ticker
    else:
        stock_endpoint = f'https://api.tdameritrade.com/v1/marketdata/{ticker}/quotes?'
    page = requests.get(url=stock_endpoint,
                        params={'apikey': key})
    content = json.loads(page.content)
    return content

def main():
    args = _argparse()
    filepath = 'config.json'
    key = readConfig(filepath)
    if args.ticker:
        print(get_data(args.ticker, key))
    elif args.watchlist:
        with open('watchlist.txt', 'r') as file:
            watchlist = file.readlines()
            new_watchlist = []
            for ticker in watchlist:
                new_watchlist.append(ticker.strip())
            print(get_data(str(new_watchlist).replace('[', '').replace(']', '').replace("'", '').replace(' ', ''), key))
    exit()

if __name__ == '__main__':
    main()