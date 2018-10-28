import numpy as np
import scipy.optimize as sp


class Portfolio:
    # This will be a general portfolio class
    # price data will be read in out of order, need to format it into
    # holdings = {  SYMBOL-EXPIRY-ID : { price data 1, price data 2 } }
    def __init__(self):
        self.holdings = {}
        self.rf = .5

    def add(self, price):
        if price['contractsymbol'] not in self.holdings:
            self.holdings[price['contractsymbol']] =[{'date': price['pricedate'], 'strike': price['strike'],
                                               'price': price['lastprice'], 'expiry': price['expiration'],
                                               'type': price['optiontype']}]
        else:
            self.holdings[price['contractsymbol']].append({'date': price['pricedate'], 'strike': price['strike'],
                                               'price': price['lastprice'], 'expiry': price['expiration'],
                                               'type': price['optiontype']})

    def optimize(self ):
        w0 = np.ones([len(self.holdings), 1]) / len(self.holdings)    # initial weights equal
        Rave = np.ones([len(self.holdings), 1])
        for key in self.holdings:     # get the length of a single contract
            lenH = len(self.holdings[key])
            break
        Ri = np.ones([lenH, len(self.holdings)])

        for i, stock in enumerate(self.holdings):
            temp = sorted(self.holdings[stock], key=lambda item: item['date'])   # sort prices in contract array by date
            prices = [temp[i]['price'] for i in range(len(temp))]
            returns = [prices[i]/prices[i-1] -1 for i in range(1, len(prices))]
            returns.insert(0, 1)   # adding this for the first day for now, results should be one less day than prices
            Ri[:, i] = returns
            Rave[i] = np.mean(returns)


        Rstar = sp.minimize(sharpe_ratio, w0, args=(Ri, Rave, self.rf), constraints={'type': 'eq', 'fun': sum_weights})
        return Rstar







def sharpe_ratio(w,Ri, Rave, Rf):
    return np.sqrt(np.dot(np.dot(np.transpose(w),np.cov(Ri)[1:, 1:]), w)) / (np.dot(np.transpose(w), Rave) - Rf)


def sum_weights(w):
    return np.sum(w)-1
