'''
    Authorize to ToS api
    Place new limit order
'''
import requests
import json
import argparse

def _argparse():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description='Process arguments')
    parser.add_argument('--ticker', help='Specific ticker to use')

    args = parser.parse_args()
    return args

def get_data(ticker, page):
    content = json.loads(page.content)
    ticker_data = content[ticker].items()

    return ticker_data


def main():
    key = "KHTCA8CYOAJO5NRROMHJSLWJRIQE4GYP"
    endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/quotes?'
    full_url = endpoint.format(stock_ticker='AAL')
    page = requests.get(url=full_url,
                    params={'apikey': key})
    
    ticker_data = get_data(args.ticker, page)
    print(ticker_data)

    exit()


if __name__ == "__main__":
    main()