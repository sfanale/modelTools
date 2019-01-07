import numpy as np
import scipy.optimize as sp
from functools import reduce
from datetime import datetime

import modelTools

class Portfolio:
    # This will be a general portfolio class
    # price data will be read in out of order, need to format it into

    def __init__(self):
        self.holdings = {}
        self.rf = .5
        self.weights = []

    def add(self, price):
        if 'close' in price:  # asset type is stock
            if price['symbol'] not in self.holdings:
                self.holdings[price['symbol']] = {'prices':{datetime.fromtimestamp(float(price['pricedate'])).date():
                                                                price['close']}, 'type': 'stock'}
            else:
                self.holdings[price['symbol']]['prices'][datetime.fromtimestamp(float(price['pricedate'])).date()] = price['close']

        else:  # asset type is option
            if price['contractsymbol'] not in self.holdings:
                self.holdings[price['contractsymbol']] = {'info':
                                                            {datetime.fromtimestamp(float(price['pricedate'])).date():
                                                                {
                                                                'strike': price['strike'], 'price': price['lastprice'],
                                                                'bid': price['bid'], 'ask': price['ask'],
                                                                'expiry': price['expiry'], 'volume':price['volume'],
                                                                'type': price['optiontype'], 'openinterest':price['openinterest']}}
                                                            , 'type': 'option','prices': {datetime.fromtimestamp(
                                                            float(price['pricedate'])).date(): price['lastprice']}}
            else:
                self.holdings[price['contractsymbol']]['info'][datetime.fromtimestamp(float(price['pricedate'])).date()] ={ 'strike': price['strike'],
                                                   'price': price['lastprice'], 'bid': price['bid'], 'ask': price['ask'], 'expiry': price['expiry'],
                                                   'type': price['optiontype'], 'openinterest':price['openinterest'], 'volume':price['volume']}
                self.holdings[price['contractsymbol']]['prices'][datetime.fromtimestamp(float(price['pricedate'])).date()] = price['lastprice']

    def returns(self):
        for stock in self.holdings:
            if self.holdings[stock]['type'] is 'option':
                c = self.holdings[stock]
                dates = sorted(list(c['prices'].keys()))   # sort prices in contract array by date
                prices = [c['prices'][d] for d in dates]
                calcprices = [round((c['info'][d]['ask']+c['info'][d]['bid'])/2, 4) for d in dates]
                for p in range(len(calcprices)):
                    if calcprices[p] == 0:
                        calcprices[p] = prices[p]  # if any prices are zero set them equal to the last trade


                returns = [prices[i]/prices[i-1] for i in range(1, len(prices))]
                returns.insert(0, 1)   # adding this for the first day for now, results
                calcreturns = [calcprices[i]/calcprices[i-1] for i in range(1, len(calcprices))]
                calcreturns.insert(0, 1)
                res = {dates[i]: returns[i] for i in range(len(returns))}
                calcrets = {dates[i]: calcreturns[i] for i in range(len(calcreturns))}
                self.holdings[stock]['returns'] = res
                self.holdings[stock]['calcreturns'] = calcrets
                # this is in cumRet*start amount = final
                self.holdings[stock]['cumulative_returns'] = reduce((lambda x, y: x*y), returns)

            elif self.holdings[stock]['type'] is 'stock':
                dates = list(self.holdings[stock]['prices'].keys())
                prices = [self.holdings[stock]['prices'][d] for d in dates]
                returns = {dates[i]: prices[i]/prices[i-1] for i in range(1,len(dates))}
                returns[dates[0]] = 1
                self.holdings[stock]['returns'] = returns
                self.holdings[stock]['cumulative_returns'] = reduce((lambda x, y: x * y), returns.values())

    def returns_til_expiry(self):
        for i, stock in enumerate(self.holdings):
            temp = sorted(self.holdings[stock]['info'], key=lambda item: item['date'])   # sort prices in contract array by date
            prices = [temp[i]['price'] for i in range(len(temp))]
            calcprices = [round((temp[i]['ask']+temp[i]['bid'])/2,4) for i in range(len(temp))]
            for p in range(len(calcprices)):
                if calcprices[p] == 0:
                    calcprices[p] = calcprices[p-1] # if any prices are zero set them equal to the day before
            returns = [prices[i]/prices[i-1] for i in range(1, len(prices))]
            returns.insert(0, 1)   # adding this for the first day for now, results
            calcreturns = [calcprices[i]/calcprices[i-1] for i in range(1, len(calcprices))]
            calcreturns.insert(0,1)
            res = {(datetime.fromtimestamp(float(temp[i]['date'])).date() -
                    datetime.fromtimestamp(float(temp[i]['expiry'])).date()).days: returns[i] for i in range(len(returns))}
            calcrets = {(datetime.fromtimestamp(float(temp[i]['date'])).date() -
                        datetime.fromtimestamp(float(temp[i]['expiry'])).date()).days: calcreturns[i] for i in range(len(calcreturns))}
            self.holdings[stock]['returns'] = res
            self.holdings[stock]['calcreturns'] = calcrets
            # this is in cumRet*start amount = final
            self.holdings[stock]['cumulative_returns'] = reduce((lambda x, y: x*y), returns)

        if self.holdings[stock]['type'] is 'stock':
            dates = self.holdings[stock]['prices'].keys()
            prices = self.holdings[stock]['prices'].values()
            returns = {dates[i]: prices[i+1] / prices[i] for i in range(len(dates))}
            self.holdings[stock]['returns'] = returns

    def optimize(self, start, end):
        # todo : read in selected assets not all
        contracts = modelTools.contract_screen(self,start,end)
        # todo : add end date of optimization range
        w0 = np.ones([len(contracts), 1]) / len(contracts)    # initial weights equal
        Rave = np.ones([len(contracts), 1])
        for key in contracts:     # get the length of a single contract
            lenH = len(contracts[key]['info'])
            break
        Ri = np.ones([lenH, len(contracts)])
        for i, stock in enumerate(contracts):
            returns = list(contracts[stock]['calcreturns'].values())
            if len(returns) == lenH:
                Ri[:, i] = returns
                Rave[i] = np.mean(returns)
            else:
                print(stock)
        Rstar = sp.minimize(sharpe_ratio, w0, args=(Ri, Rave, self.rf), constraints={'type': 'eq', 'fun': sum_weights})
        self.weights = Rstar['x']

        return Rstar['x'], Ri, contracts

    def find(self, ticker):
        contracts = []
        for k in self.holdings:
            if k.split('1')[0] == ticker:
                contracts.append(k)
        return contracts

    def run(self, start, end):
        # start date is
        self.returns()
        Rstar, Ri, contracts = self.optimize(start, end)
        daily_tot =[]
        for i, day in enumerate(Ri):
            daily_tot.append(reduce((lambda x, y: x+y), day*Rstar))
        total_returns = reduce((lambda x, y: x*y), daily_tot)
        return total_returns, daily_tot


def sharpe_ratio(w,Ri, Rave, Rf):
    return np.sqrt(np.dot(np.dot(np.transpose(w), np.cov(Ri, rowvar=False)), w)) / (np.dot(np.transpose(w), Rave) - Rf)


def sum_weights(w):
    return np.sum(w)-1
