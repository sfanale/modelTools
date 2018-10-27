import numpy as np
import scipy.optimize as sp


class Portfolio:
    # This will be a general portfolio class
    # price data will be read in out of order, need to format it into
    # holdings = {  SYMBOL-EXPIRY-ID : { price data 1, price data 2 } }
    def __init__(self):
        self.holdings = {}


    def add(self, price):
        if price['contractsymbol'] not in self.holdings:
            self.holdings['contractsymbol'] =[{'date': price['pricedate'], 'strike': price['strike'],
                                               'price': price['lastprice'], 'expiry': price['expiration'],
                                               'type': price['optiontype']}]
        else:
            self.holdings['contractsymbol'].append({'date': price['pricedate'], 'strike': price['strike'],
                                               'price': price['lastprice'], 'expiry': price['expiration'],
                                               'type': price['optiontype']})


    def optimize(self, start_date, end_date ):
        w0 = np.ones(len(self.holdings)) / len(self.holdings)    # initial weights equal
        for stock in self.holdings:
            temp = sorted(stock, key=lambda item: item['date'])   # sort prices in contract array by date
            prices = [temp[i]['price'] for i in range(len(temp))]
            returns = [temp[i]/temp[i-1] -1 for i in range(1, len(prices))]




def sharpe_ratio(w,Ri, Rave, Rf):
    return np.sqrt(np.dot(np.transpose(w), np.dot(np.cov(Ri), w))) / (np.dot(np.transpose(w), Rave) - Rf)




result = sp.minimize(sharpe_ratio, w0, args=(Ri, Rave, Rf))
