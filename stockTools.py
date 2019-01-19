from Portfolio import Portfolio
import numpy as np
import json
from datetime import datetime
import datetime as dt
import matplotlib.pyplot as plt
import requests
from scipy import stats
from scipy.optimize import curve_fit
import statsmodels.formula.api as smf
import pandas as pd
from functools import reduce
import modelTools as mT


def get_one_stock(ticker, my_portfolio):
    # get price data for one asset

    data = requests.get("http://data.fanaleresearch.com/api/quotes/" + ticker)
    data = data.json()
    for price in data:
        my_portfolio.add(price)



def bolinger_bands(my_portfolio):
    """
    Build bolinger bands (1 std up and down from 21 day moving average) around stock and graph
    :param my_portfolio:
    :return:
    """