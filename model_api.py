import modelTools as mT
from Portfolio import Portfolio
import flask
import datetime


def get_returns(asset_list, type ,returns_style='calc'):
    """
    Inputs: list of assests and returns style
    default returns are calculated returns
    :return: dictionary of assets and their returns
    """
    myport = Portfolio()
    rets = 'calcreturns'
    # for asset in list, get them, and add to portfolio
    for contract in asset_list:
        if type is 'singlecontracts':
            mT.get_one_contract(contract, myport)
        elif type is 'allcontracts':
            mT.get_one_option(contract, myport)
        elif type is 'stock':
            mT.get_one_stock(contract, myport)
    # calculate returns
    myport.returns()
    if returns_style is 'true':
        rets = 'returns'
    result_dict = {contract:[rets] for contract in myport.holdings.keys()}
    return flask.jsonify(result_dict)


def parse_model_params(info):
    # todo : this is horrible form, make this temp
    inputs = info.split('&')
    print(inputs)
    asset_list = inputs[0].split('+')
    opt_range = int(inputs[1])
    expiry_range =int(inputs[2])
    reopt_freq = int(inputs[3])
    asset_types = inputs[4]
    return run_model(asset_list, opt_time_range=opt_range, expiry_range=expiry_range, reopt_freq=reopt_freq, asset_types=asset_types)



def run_model(asset_list, returns_style='calc', optimization_style='sharpe', opt_window_start=datetime.date(2018,10,28),
              opt_time_range=4, filter_type='expirydate', expiry_range=52, reopt_freq=2, leverage=1, asset_types='options'):
    """
    Inputs: list of assets, returns style, optimization style, optimmization window start date, optimization time range,
        filter type, expriry_range, re-optimization frequency, leverage
        date ranges are in weeks
    :return:
    """
    myport = Portfolio()

    rets = 'calcreturns'
    print(asset_types)
    for contract in asset_list:
        print(contract)
        if asset_types == 'options':
            mT.get_one_option(contract, myport)
        elif asset_types == 'stocks':
            mT.get_one_stock(contract, myport)
        elif asset_types == 'mixed':
            mT.get_one_option(contract, myport)
            mT.get_one_stock(contract, myport)

    if optimization_style is 'sharpe':
        print('modeling')
        result_dict = myport.run(opt_window_start, opt_time_range,
                                           opt_window_start + datetime.timedelta(days=7*expiry_range),
                                           reopt_freq)

    return flask.jsonify(result_dict)


