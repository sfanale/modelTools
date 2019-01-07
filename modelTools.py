from Portfolio import Portfolio
import numpy as np
import json
from datetime import datetime
import matplotlib.pyplot as plt
import requests
from scipy import stats
from scipy.optimize import curve_fit
import statsmodels.formula.api as smf
from functools import reduce


def get_one_option(ticker, my_portfolio):
    # get all option data for one underlying asset
    # to init a portfolio object:
    # from Portfolio import Portfolio
    # myport = Portfolio()

    data = requests.get("http://data.fanaleresearch.com:5000/api/options/all/"+ticker)
    data = data.json()
    for price in data:
        my_portfolio.add(price)


def get_one_stock(ticker, my_portfolio):
    # get price data for one asset

    data = requests.get("http://data.fanaleresearch.com:5000/api/quotes/" + ticker)
    data = data.json()
    for price in data:
        my_portfolio.add(price)

# get returns
# my_portfolio.returns()


def get_all_dowjones(my_portfolio):
    DJ = ["AXP", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "XOM", "GS", "HD", "IBM", "INTC", "JNJ",
          "JPM", "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UNH", "UTX", "VZ", "V", "WMT", "WBA", "DIS"]

    for i, ticker in enumerate(DJ):
        data = requests.get("http://data.fanaleresearch.com:5000/api/quotes/" + ticker)
        data = data.json()
        for price in data:
            my_portfolio.add(price)
        print(round(100*((i+.5)/28),1),'%')
        data = requests.get("http://data.fanaleresearch.com:5000/api/options/all/" + ticker)
        data = data.json()
        for price in data:
            my_portfolio.add(price)
        print(round(100*((i+1)/28),1), "%")

def sort_by_cumulative_returns(my_portfolio):
    # contracts sorted by cumulative returns
    # returns sorted list of contract names, these can be used to grab items from portfolio holdings dictionary

    res = sorted(my_portfolio.holdings, key=lambda item: my_portfolio.holdings[item]['cumulative_returns'], reverse=True)
    return res


def get_all_stocks(my_portfolio):
    # gets and adds all option data to a portfolio object
    # this will take some time

    SP500 = ['DB', 'AAPL', 'ABT', 'ABBV', 'ACN', 'ACE', 'ADBE', 'ADT', 'AAP', 'AES', 'AET', 'AFL',
             'AMG', 'A', 'GAS', 'ARE', 'APD', 'AKAM', 'AA', 'AGN', 'ALXN', 'ALLE', 'ADS', 'ALL', 'ALTR', 'MO', 'AMZN',
             'AEE', 'AAL',
             'AEP', 'AXP', 'AIG', 'AMT', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'APC', 'ADI', 'AON', 'APA', 'AIV', 'AMAT',
             'ADM', 'AIZ', 'T', 'ADSK', 'ADP', 'AN', 'AZO', 'AVGO', 'AVB', 'AVY', 'BHI', 'BLL', 'BAC', 'BK', 'BCR',
             'BXLT', 'BAX', 'BBT', 'BDX', 'BBBY', 'BRK.B', 'BBY', 'BLX', 'HRB', 'BA', 'BWA', 'BXP', 'BSX', 'BMY',
             'BRCM',
             'BF.B', 'CHRW', 'CA', 'CVC', 'COG', 'CAM', 'CPB', 'COF', 'CAH', 'HSIC', 'KMX', 'CCL', 'CAT', 'CBG', 'CBS',
             'CELG', 'CNP', 'CTL', 'CERN', 'CF', 'SCHW', 'CHK', 'CVX', 'CMG', 'CB', 'CI', 'XEC', 'CINF', 'CTAS', 'CSCO',
             'C', 'CTXS', 'CLX', 'CME', 'CMS', 'COH', 'KO', 'CCE', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CSC', 'CAG', 'COP',
             'CNX', 'ED', 'STZ', 'GLW', 'COST', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DLPH',
             'DAL', 'XRAY', 'DVN', 'DO', 'DTV', 'DFS', 'DISCA', 'DISCK', 'DG', 'DLTR', 'D', 'DOV', 'DOW', 'DPS', 'DTE',
             'DD', 'DUK', 'DNB', 'ETFC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMC', 'EMR', 'ENDP', 'ESV',
             'ETR', 'EOG', 'EQT', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ES', 'EXC', 'EXPE', 'EXPD', 'ESRX', 'XOM', 'FFIV',
             'FB', 'FAST', 'FDX', 'FIS', 'FITB', 'FSLR', 'FE', 'FISV', 'FLIR', 'FLS', 'FLR', 'FMC', 'FTI', 'F', 'FOSL',
             'BEN', 'FCX', 'FTR', 'GME', 'GPS', 'GRMN', 'GD', 'GE', 'GGP', 'GIS', 'GM', 'GPC', 'GNW', 'GILD', 'GS',
             'GT',
             'GOOGL', 'GOOG', 'GWW', 'HAL', 'HBI', 'HOG', 'HAR', 'HRS', 'HIG', 'HAS', 'HCA', 'HCP', 'HCN', 'HP', 'HES',
             'HPQ', 'HD', 'HON', 'HRL', 'HSP', 'HST', 'HCBK', 'HUM', 'HBAN', 'ITW', 'IR', 'INTC', 'ICE', 'IBM', 'IP',
             'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IRM', 'JEC', 'JBHT', 'JNJ', 'JCI', 'JOY', 'JPM', 'JNPR', 'KSU', 'K',
             'KEY', 'GMCR', 'KMB', 'KIM', 'KMI', 'KLAC', 'KSS', 'KRFT', 'KR', 'LB', 'LLL', 'LH', 'LRCX', 'LM', 'LEG',
             'LEN', 'LVLT', 'LUK', 'LLY', 'LNC', 'LLTC', 'LMT', 'L', 'LOW', 'LYB', 'MTB', 'MAC', 'M', 'MNK', 'MRO',
             'MPC',
             'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK', 'MJN', 'MMV', 'MDT', 'MRK', 'MET', 'KORS',
             'MCHP', 'MU', 'MSFT', 'MHK', 'TAP', 'MDLZ', 'MON', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MUR', 'MYL', 'NDAQ',
             'NOV', 'NAVI', 'NTAP', 'NFLX', 'NWL', 'NFX', 'NEM', 'NWSA', 'NEE', 'NLSN', 'NKE', 'NI', 'NE', 'NBL', 'JWN',
             'NSC', 'NTRS', 'NOC', 'NRG', 'NUE', 'NVDA', 'ORLY', 'OXY', 'OMC', 'OKE', 'ORCL', 'OI', 'PCAR', 'PLL', 'PH',
             'PDCO', 'PAYX', 'PNR', 'PBCT', 'POM', 'PEP', 'PKI', 'PRGO', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PBI',
             'PCL', 'PNC', 'RL', 'PPG', 'PPL', 'PX', 'PCP', 'PCLN', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA',
             'PHM',
             'PVH', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RRC', 'RTN', 'O', 'RHT', 'REGN', 'RF', 'RSG', 'RAI', 'RHI', 'ROK',
             'COL', 'ROP', 'ROST', 'RLD', 'R', 'CRM', 'SNDK', 'SCG', 'SLB', 'SNI', 'STX', 'SEE', 'SRE', 'SHW', 'SPG',
             'SWKS', 'SLG', 'SJM', 'SNA', 'SO', 'LUV', 'SWN', 'SE', 'STJ', 'SWK', 'SPLS', 'SBUX', 'HOT', 'STT', 'SRCL',
             'SYK', 'STI', 'SYMC', 'SYY', 'TROW', 'TGT', 'TEL', 'TE', 'TGNA', 'THC', 'TDC', 'TSO', 'TXN', 'TXT', 'HSY',
             'TRV', 'TMO', 'TIF', 'TWX', 'TWC', 'TJX', 'TMK', 'TSS', 'TSCO', 'RIG', 'TRIP', 'FOXA', 'TSN', 'TYC', 'UA',
             'UNP', 'UNH', 'UPS', 'URI', 'UTX', 'UHS', 'UNM', 'URBN', 'VFC', 'VLO', 'VAR', 'VTR', 'VRSN', 'VZ', 'VRTX',
             'VIAB', 'V', 'VNO', 'VMC', 'WMT', 'WBA', 'DIS', 'WM', 'WAT', 'ANTM', 'WFC', 'WDC', 'WU', 'WY', 'WHR',
             'WFM',
             'WMB', 'WEC', 'WYN', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XL', 'XYL', 'YHOO', 'YUM', 'ZBH', 'ZION', 'ZTS', 'IVV',
             'IJR', 'IYE', 'IYF', 'IYJ', 'IYK', 'IYM', 'IYZ', 'IYW']
    for stock in SP500:
        try:
            data = requests.get("http://data.fanaleresearch.com:5000/api/quotes/" + stock)
            data = data.json()
            for row in data:
                my_portfolio.add(row)
        except KeyError:
            print(stock)
            print(data)
        except json.decoder.JSONDecodeError:
            print(stock)
            print(data)


def get_all_options(my_portfolio):
    # gets and adds all option data to a portfolio object
    # this will take some time

        data = requests.get("http://data.fanaleresearch.com:5000/api/options/all/*")
        data = data.json()
        for row in data:
            my_portfolio.add(row)


def predicted_prices(myport, ticker):
    dates = list(myport.holdings[ticker]['prices'].keys())
    # lets see what one date looks like
    slopesResults ={}
    startdate = dates[0]
    contracts = list(myport.holdings.keys())
    q=1
    for date in dates:
        resultsDates = []
        resultsPrices = []
        resultsActualPrices =[]
        for c in contracts:
            if c == ticker:
                resultsDates.append(0)
                resultsPrices.append(myport.holdings[c]['prices'][date])
                resultsActualPrices.append(1)
            else:
                try:
                    if myport.holdings[c]['info'][0]['type'] == 'call':
                        resultsPrices.append(myport.holdings[c]['prices'][date] + myport.holdings[c]['info'][0]['strike'])
                        d2 = datetime.fromtimestamp(float(myport.holdings[c]['info'][0]['expiry'])).date()
                        d1 = datetime.fromtimestamp(float(myport.holdings[c]['info'][0]['date'])).date()
                        resultsActualPrices.append(myport.holdings[c]['prices'][date])
                        resultsDates.append((d2 - d1).days)

                    elif myport.holdings[c]['info'][0]['type'] == 'put':
                        resultsPrices.append(myport.holdings[c]['info'][0]['strike'] - myport.holdings[c]['prices'][date])
                        d2 = datetime.fromtimestamp(float(myport.holdings[c]['info'][0]['expiry'])).date()
                        d1 = datetime.fromtimestamp(float(myport.holdings[c]['info'][0]['date'])).date()
                        resultsActualPrices.append(myport.holdings[c]['prices'][date])
                        resultsDates.append((d2-d1).days)
                except KeyError:
                    # this means there isnt a price for that date
                    continue
        datesUni = list(set(resultsDates))
        datesUni.sort()
        temp = {date: [] for date in datesUni}
        i = 0
        while i < len(resultsPrices):
            k = resultsDates[i]
            j = resultsPrices[i]
            w = resultsActualPrices[i]
            temp[k].append([j,w])
            i += 1
        averages = {0: myport.holdings[ticker]['prices'][date]}
        for k in temp:
            t = np.asarray(temp[k])
            averages[k] = np.average(t[:,0], weights =t[:,1] )
        slope, intercept, r_value, p_value, std_err = stats.linregress(list(averages.keys()), list(averages.values()))
        slopesResults[(date-startdate).days] = slope
        plt.figure(figsize=(30, 30))
        plt.title(date.strftime('%D'))
        plt.ylim((0, 500))
        plt.plot(resultsDates, resultsPrices, 'r*')
        plt.plot(resultsDates, list(map(lambda d: d*slope + intercept, resultsDates)), 'g-')
        plt.plot(averages.keys(), averages.values(), 'kx-')
        plt.savefig('pricemap'+str(q)+'.png')
        q += 1
    plt.figure(figsize=(20, 10))
    plt.plot(slopesResults.keys(), slopesResults.values(), 'g*')
    x = list(slopesResults.keys())
    y = list(slopesResults.values())
    s, i, r, p, std = stats.linregress(x, y)
    y = list(map(lambda d: d*s + i, x))
    plt.plot(x, y, 'k-', label=str(s))
    #y2 = [ i/(myport.holdings[c]['prices'][date])]
    x2 = [(i - startdate).days for i in list(myport.holdings[ticker]['returns'].keys())]
    plt.plot(x2, [i-1 for i in list(myport.holdings[ticker]['returns'].values())], 'rx-')
    plt.legend()
    plt.title("slope of price map vs date")
    plt.savefig('aaplPriceMapSlopes.png')


def pricing_model(myport):
    # underlying daily returns
    # option type the strike-price/ price
    # days till expiration
    # daily slope of trendline?

    SP500 = ['DB', 'AAPL', 'ABT', 'ABBV', 'ACN', 'ACE', 'ADBE', 'ADT', 'AAP', 'AES', 'AET', 'AFL',
             'AMG', 'A', 'GAS', 'ARE', 'APD', 'AKAM', 'AA', 'AGN', 'ALXN', 'ALLE', 'ADS', 'ALL', 'ALTR', 'MO', 'AMZN',
             'AEE', 'AAL',
             'AEP', 'AXP', 'AIG', 'AMT', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'APC', 'ADI', 'AON', 'APA', 'AIV', 'AMAT',
             'ADM', 'AIZ', 'T', 'ADSK', 'ADP', 'AN', 'AZO', 'AVGO', 'AVB', 'AVY', 'BHI', 'BLL', 'BAC', 'BK', 'BCR',
             'BXLT', 'BAX', 'BBT', 'BDX', 'BBBY', 'BRK.B', 'BBY', 'BLX', 'HRB', 'BA', 'BWA', 'BXP', 'BSX', 'BMY',
             'BRCM',
             'BF.B', 'CHRW', 'CA', 'CVC', 'COG', 'CAM', 'CPB', 'COF', 'CAH', 'HSIC', 'KMX', 'CCL', 'CAT', 'CBG', 'CBS',
             'CELG', 'CNP', 'CTL', 'CERN', 'CF', 'SCHW', 'CHK', 'CVX', 'CMG', 'CB', 'CI', 'XEC', 'CINF', 'CTAS', 'CSCO',
             'C', 'CTXS', 'CLX', 'CME', 'CMS', 'COH', 'KO', 'CCE', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CSC', 'CAG', 'COP',
             'CNX', 'ED', 'STZ', 'GLW', 'COST', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DLPH',
             'DAL', 'XRAY', 'DVN', 'DO', 'DTV', 'DFS', 'DISCA', 'DISCK', 'DG', 'DLTR', 'D', 'DOV', 'DOW', 'DPS', 'DTE',
             'DD', 'DUK', 'DNB', 'ETFC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMC', 'EMR', 'ENDP', 'ESV',
             'ETR', 'EOG', 'EQT', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ES', 'EXC', 'EXPE', 'EXPD', 'ESRX', 'XOM', 'FFIV',
             'FB', 'FAST', 'FDX', 'FIS', 'FITB', 'FSLR', 'FE', 'FISV', 'FLIR', 'FLS', 'FLR', 'FMC', 'FTI', 'F', 'FOSL',
             'BEN', 'FCX', 'FTR', 'GME', 'GPS', 'GRMN', 'GD', 'GE', 'GGP', 'GIS', 'GM', 'GPC', 'GNW', 'GILD', 'GS',
             'GT',
             'GOOGL', 'GOOG', 'GWW', 'HAL', 'HBI', 'HOG', 'HAR', 'HRS', 'HIG', 'HAS', 'HCA', 'HCP', 'HCN', 'HP', 'HES',
             'HPQ', 'HD', 'HON', 'HRL', 'HSP', 'HST', 'HCBK', 'HUM', 'HBAN', 'ITW', 'IR', 'INTC', 'ICE', 'IBM', 'IP',
             'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IRM', 'JEC', 'JBHT', 'JNJ', 'JCI', 'JOY', 'JPM', 'JNPR', 'KSU', 'K',
             'KEY', 'GMCR', 'KMB', 'KIM', 'KMI', 'KLAC', 'KSS', 'KRFT', 'KR', 'LB', 'LLL', 'LH', 'LRCX', 'LM', 'LEG',
             'LEN', 'LVLT', 'LUK', 'LLY', 'LNC', 'LLTC', 'LMT', 'L', 'LOW', 'LYB', 'MTB', 'MAC', 'M', 'MNK', 'MRO',
             'MPC',
             'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK', 'MJN', 'MMV', 'MDT', 'MRK', 'MET', 'KORS',
             'MCHP', 'MU', 'MSFT', 'MHK', 'TAP', 'MDLZ', 'MON', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MUR', 'MYL', 'NDAQ',
             'NOV', 'NAVI', 'NTAP', 'NFLX', 'NWL', 'NFX', 'NEM', 'NWSA', 'NEE', 'NLSN', 'NKE', 'NI', 'NE', 'NBL', 'JWN',
             'NSC', 'NTRS', 'NOC', 'NRG', 'NUE', 'NVDA', 'ORLY', 'OXY', 'OMC', 'OKE', 'ORCL', 'OI', 'PCAR', 'PLL', 'PH',
             'PDCO', 'PAYX', 'PNR', 'PBCT', 'POM', 'PEP', 'PKI', 'PRGO', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PBI',
             'PCL', 'PNC', 'RL', 'PPG', 'PPL', 'PX', 'PCP', 'PCLN', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA',
             'PHM',
             'PVH', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RRC', 'RTN', 'O', 'RHT', 'REGN', 'RF', 'RSG', 'RAI', 'RHI', 'ROK',
             'COL', 'ROP', 'ROST', 'RLD', 'R', 'CRM', 'SNDK', 'SCG', 'SLB', 'SNI', 'STX', 'SEE', 'SRE', 'SHW', 'SPG',
             'SWKS', 'SLG', 'SJM', 'SNA', 'SO', 'LUV', 'SWN', 'SE', 'STJ', 'SWK', 'SPLS', 'SBUX', 'HOT', 'STT', 'SRCL',
             'SYK', 'STI', 'SYMC', 'SYY', 'TROW', 'TGT', 'TEL', 'TE', 'TGNA', 'THC', 'TDC', 'TSO', 'TXN', 'TXT', 'HSY',
             'TRV', 'TMO', 'TIF', 'TWX', 'TWC', 'TJX', 'TMK', 'TSS', 'TSCO', 'RIG', 'TRIP', 'FOXA', 'TSN', 'TYC', 'UA',
             'UNP', 'UNH', 'UPS', 'URI', 'UTX', 'UHS', 'UNM', 'URBN', 'VFC', 'VLO', 'VAR', 'VTR', 'VRSN', 'VZ', 'VRTX',
             'VIAB', 'V', 'VNO', 'VMC', 'WMT', 'WBA', 'DIS', 'WM', 'WAT', 'ANTM', 'WFC', 'WDC', 'WU', 'WY', 'WHR',
             'WFM',
             'WMB', 'WEC', 'WYN', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XL', 'XYL', 'YHOO', 'YUM', 'ZBH', 'ZION', 'ZTS', 'IVV',
             'IJR', 'IYE', 'IYF', 'IYJ', 'IYK', 'IYM', 'IYZ', 'IYW']
    DJ = ["AXP", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "XOM", "GS", "HD", "IBM", "INTC", "JNJ",
          "JPM", "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UNH", "UTX", "VZ", "V", "WMT", "WBA", "DIS"]
    calls = []  # returns, underlying returns, in/out%, days til expiry, constant 1
    puts = []
    L = ['AAPL']
    for ticker in DJ:
        try:
            contracts = myport.find(ticker)
            dates = list(myport.holdings[ticker]['returns'].keys())
            for date in dates:
                for c in contracts:
                    if c == ticker:
                        continue
                    else:
                        try:
                            if myport.holdings[c]['info'][date]['type'] == 'call':
                                percent_ITM = 100 * ((myport.holdings[c]['prices'][date] / myport.holdings[c]['info'][date]['strike']) - 1)
                                underlying_returns = 100 * (myport.holdings[ticker]['returns'][date]-1)
                                d2 = datetime.fromtimestamp(float(myport.holdings[c]['info'][date]['expiry'])).date()
                                d1 = date
                                #option_returns = 100 * (myport.holdings[c]['returns'][date]-1)
                                option_returns = 100*(myport.holdings[c]['calcreturns'][date]-1)
                                if (d2 - d1).days > 0 and len(myport.holdings[c]['returns']) > 10:
                                    days_til_expiry = 1/((d2 - d1).days)
                                    calls.append([option_returns, underlying_returns, percent_ITM, days_til_expiry, 1])

                            elif myport.holdings[c]['info'][date]['type'] == 'put':
                                percent_ITM = 100 * (1 - (myport.holdings[c]['prices'][date] / myport.holdings[c]['info'][date]['strike']))
                                underlying_returns = 100 * (myport.holdings[ticker]['returns'][date]-1)
                                d2 = datetime.fromtimestamp(float(myport.holdings[c]['info'][date]['expiry'])).date()
                                d1 = date
                                #option_returns = 100 * (myport.holdings[c]['returns'][date] - 1)
                                option_returns = 100*(myport.holdings[c]['calcreturns'][date]-1)
                                if (d2 - d1).days >0 and len(myport.holdings[c]['returns']) > 10:
                                    days_til_expiry = 1/((d2 - d1).days)
                                    puts.append([option_returns, underlying_returns, percent_ITM, days_til_expiry, 1])
                        except KeyError:
                            # this means there isnt a price for that date
                            continue
        except KeyError:
            continue
            # this asset is not in the data set

    calls = np.asarray(calls)
    puts = np.asarray(puts)

    results = smf.OLS(calls[:,0], calls[:,1:]).fit()
    print("Calls")
    print(results.summary())

    results = smf.OLS(puts[:,0], puts[:,1:]).fit()
    print("Puts")
    print(results.summary())
    return calls, puts


def contract_screen(myport, start_date, end_date):
    # enter in start and end as datetimes
    results = {}
    for contract_name in myport.holdings:
        contract = myport.holdings[contract_name]
        dates = list(contract['info'].keys())
        dates.sort()
        expiry = datetime.fromtimestamp(float(contract['info'][dates[0]]['expiry'])).date()
        if dates[0] < start_date and expiry > end_date:
            results[contract_name] = contract
    return results