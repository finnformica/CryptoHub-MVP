import csv
import pandas as pd
import numpy as np
import requests

from binance.client import Client

from application import db
from application.models import Transaction

client = Client("", "")

# commit transactions to database
def load_transactions():
    df = load_data()
    for index, row in df.iterrows():
        transaction = Transaction(
                    type = row['Type'],
                    coin = row['Coin'],
                    currency = 'USD',
                    price = row['Price'],
                    quantity = row['Quantity'],
                    date = row['Date'],
                    total_spent = float(row['Price']) * float(row['Quantity']) + float(row['Fees']),
                    fees = row['Fees'],
                    notes = '-'
                )
        db.session.add(transaction)
        db.session.commit()


def get_coingecko_price(coins):
    coingecko_endpoint = 'https://api.coingecko.com/api/v3/simple/price'
    currency = '&vs_currencies=usd'

    with open('application/data/coingecko_ids.csv', 'r') as f:
        reader = csv.reader(f)
        id = dict(reader)

    ids = [id[coin.lower()] for coin in coins]
    id_string = '?ids=' + '%2C'.join(ids)

    url = coingecko_endpoint + id_string + currency
    r = requests.get(url).json()

    prices = [r[id]['usd'] for id in ids]
    return prices


def create_dataframe():
    transactions = Transaction.query.all()

    df = pd.DataFrame(data=[{'type': t.type,
            'coin': t.coin,
            'currency': t.currency,
            'price': t.price,
            'quantity': t.quantity,
            'value': t.total_spent} for t in transactions])

    return df

# construct pivot table from transactions
def create_pivot_table(df):

    def get_price(coin): # binance has less coins than coingecko but is faster
        try:
            price = client.get_symbol_ticker(symbol = coin + "USDT")['price']
        except:
            price = 0
        return float(price)

    # aggregate trade data
    table = pd.pivot_table(df, values=['value', 'quantity'], index=['coin'], columns=['type'], aggfunc=np.sum, fill_value=0)

    # restructure table
    table = table.reindex(columns=[('quantity',  'Buy'),
            ('quantity', 'Sell'),
            ('value',  'Buy'),
            ('value', 'Sell')], fill_value=0)

    coins = [name for name in table.index]
    row_data = table.to_numpy()

    # create pivot table with Buy and Sell data
    pivot = pd.DataFrame(data=row_data, columns=['Bought', 'Sold', 'Spent', 'Cash'], index=coins)

    # calculate portfolio data
    pivot['Cost'] = pivot['Spent'] - pivot['Cash']
    pivot['Quantity'] = pivot['Bought'] - pivot['Sold']
    pivot['Avg In'] = pivot['Spent'] / pivot['Bought']
    pivot['Avg Out'] = pivot['Cash'] / pivot['Sold']

    # use websockets to stream current price data
    # or figure out a way to update every 5 min
    pivot['Price'] = get_coingecko_price(coins)

    pivot['Value'] = pivot['Quantity'] * pivot['Price']
    pivot['PnL'] = pivot['Value'] - pivot['Cost']
    pivot['ROI'] = 100 * pivot['PnL'] / pivot['Spent']

    return pivot.fillna(0)
