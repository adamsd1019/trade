'''
    Program to collect data and place trades
'''
import requests
import json
import argparse


def _argparse():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description='Process arguments')
    parser.add_argument('--ticker', type=str, help='Specific ticker to use')
    parser.add_argument('-o','--options', action='store_true',help='Toggle for options chain')
    # parser.add_argument('--strike', help='List strikes as comma delimited')

    args = parser.parse_args()
    return args


def get_data(ticker, key):
    # Collect stock data from tdapi from a specific ticker
    # ticker_data returns as a dictionary
    stock_endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/quotes?'
    full_url = stock_endpoint.format(stock_ticker=ticker)
    page = requests.get(url=full_url,
                    params={'apikey': key})
    content = json.loads(page.content)
    ticker_data = content[ticker].items()

    return ticker_data


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
            print(option)
    elif args.ticker:
        ticker_data = get_data(args.ticker, key)
        for k,v in ticker_data:
            print(k,v)

    exit()


if __name__ == "__main__":
    main()
