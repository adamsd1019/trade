'''
    Program to collect data and place trades
'''
import requests
import json
import argparse

def _argparse():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description='Process arguments')
    parser.add_argument('--ticker', type=str, help='Specific ticker to use')

    args = parser.parse_args()
    return args

def get_data(ticker, endpoint, key):
    # Collect data from tdapi from a specific ticker
    # ticker_data returns as a dictionary
    full_url = endpoint.format(stock_ticker=ticker)
    page = requests.get(url=full_url,
                    params={'apikey': key})
    content = json.loads(page.content)
    ticker_data = content[ticker].items()

    return ticker_data


def main():
    args = _argparse()

    key = "KHTCA8CYOAJO5NRROMHJSLWJRIQE4GYP"
    endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/quotes?'
    
    ticker_data = get_data(args.ticker, endpoint, key)
    for k,v in ticker_data:
        print(k,v)

    exit()


if __name__ == "__main__":
    main()