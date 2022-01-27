import json
import argparse
import requests

def _argparse():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Process arguments')
    parser.add_argument('-t', '--ticker', type=str, help='Specific ticker to use')
    parser.add_argument('-o','--options', action='store_true', help='Toggle for options chain')
    parser.add_argument('--freq', type=int, help='How many minutes per candle')
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
    stock_endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/quotes?'
    full_url = stock_endpoint.format(stock_ticker=ticker)
    page = requests.get(url=full_url,
                    params={'apikey': key})
    content = json.loads(page.content)
    return content[ticker]

def main():
    args = _argparse()
    filepath = 'config.json'
    key = readConfig(filepath)
    print(get_data(args.ticker, key))

    exit()

if __name__ == '__main__':
    main()