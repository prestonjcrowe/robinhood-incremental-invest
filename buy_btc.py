import robin_stocks as r
import sys
import os

BUY_AMOUNT_USD = 1.0
USERNAME = os.environ['ROBINHOOD_USER']
PASSWORD = os.environ['ROBINHOOD_PASS']

# Authenticate
try:
    login = r.login(USERNAME, PASSWORD)
    print('Authenticated as {} successfully'.format(USERNAME))
except Exception as e:
    print('Error authenticating as {}'.format(USERNAME))
    sys.exit(e)

# Load profile data
profile = r.load_account_profile()
portfolio = r.get_crypto_positions()
cash = float(profile['portfolio_cash'])

# Print crypto portfolio
row_format = " {:<6} | {:<15} | {:<15}"
print(row_format.format("Symbol", "Name", "Amount"))
for holding in portfolio:
    name = holding['currency']['name']
    symbol = holding['currency']['code']
    quantity = holding['quantity']
    print(row_format.format(symbol, name, quantity))

if cash < BUY_AMOUNT_USD:
    sys.exit('You dont have enough funds in your account')

# Purchase btc
#print('Buying ${} of BTC'.format(BUY_AMOUNT_USD))
#res = r.order_buy_crypto_by_price('BTC',BUY_AMOUNT_USD)
#print(res)

