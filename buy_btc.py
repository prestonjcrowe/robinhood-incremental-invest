# Simple script that buys a set dollar amount of Bitcoin on Robinhood.
# Meant to be run on a schedule.

import robin_stocks as r
import sys
import os
import logging

BUY_AMOUNT_USD = 1.0
USERNAME = os.environ['ROBINHOOD_USER']
PASSWORD = os.environ['ROBINHOOD_PASS']
LOG_FILENAME = 'robinhood.log'

def main():
    logging.basicConfig(filename=LOG_FILENAME,
                        level=logging.INFO,
                        format='%(asctime)s : %(message)s')

    # Authenticate
    try:
        login = r.login(USERNAME, PASSWORD)
        logging.info('Authenticated as {} successfully'.format(USERNAME))
        print('Authenticated as {} successfully'.format(USERNAME))
    except Exception as e:
        logging.error('Error authenticating as {}'.format(USERNAME))
        print('Error authenticating as {}'.format(USERNAME))
        sys.exit(e)

    # Load profile data
    profile = r.load_account_profile()
    portfolio = r.get_crypto_positions()
    cash = float(profile['portfolio_cash'])
    print_crypto_portfolio(portfolio)

    if cash < BUY_AMOUNT_USD:
        logging.info('You dont have enough funds in your account')
        sys.exit('You dont have enough funds in your account')

    # Purchase btc
    purchase_btc(BUY_AMOUNT_USD)

def purchase_btc(amount_usd):
    ask_price = get_ask_price('BTC')
    res = r.order_buy_crypto_by_price('BTC',BUY_AMOUNT_USD)
    if res == None:
        logging.error('Encountered an error purchasing BTC')
        sys.exit('Encountered an error purchasing BTC')

    quantity = res['quantity']
    price = res['price']
    print('Bought {} BTC at ${} for ${}'.format(quantity, ask_price, BUY_AMOUNT_USD))
    logging.info('Bought {} BTC at ${} for ${}'.format(quantity, ask_price, BUY_AMOUNT_USD))

def get_ask_price(symbol):
    quote = r.get_crypto_quote(symbol)
    if quote == None:
        return None
    return quote['ask_price']

def print_crypto_portfolio(portfolio):
    row_format = " {:<6} | {:<6.10} | ${:<6.3}"
    print('Crypto Portfolio')
    print('=' * 50)
    for holding in portfolio:
        name = holding['currency']['name']
        symbol = holding['currency']['code']
        quantity = holding['quantity']
        price = get_ask_price(symbol)
        usd_value = float(price) * float(quantity)
        print(row_format.format(symbol, quantity, usd_value))
    print('=' * 50)
  
if __name__ == '__main__':
    main()

