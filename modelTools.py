from Portfolio import Portfolio
import numpy as np
import matplotlib.pyplot as plt
import requests
from functools import reduce

my_portfolio = Portfolio()
data = requests.get("http://localhost:5000/api/options/AAPL")
data = data.json()
syms = [i['contractsymbol'] for i in data]

# get and add each contract and its prices
for s in syms:
    request_string = "http://localhost:5000/api/options/detail/" + s
    response = requests.get(request_string)
    response = response.json()
    for price in response:
        price['contractsymbol'] = s
        my_portfolio.add(price)

# get returns
my_portfolio.returns()

# contracts sorted by cumulative returns
res = sorted(my_portfolio.holdings, key=lambda item: my_portfolio.holdings[item]['cumulative_returns'], reverse=True)




"""
# this is the maximum length for the price history
# for now ill only use the contracts that havent expired yet
max_length = max([len(my_portfolio.holdings[i]['info']) for j, i in enumerate(my_portfolio.holdings)])


"""



