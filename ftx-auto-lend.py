import fire
import math
import logging
import os
from typing import Dict, List
from modules.FTX import FTXClient

# Logging to where this script is at
os.chdir(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(filename='run.log', filemode='a', format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

def _get_coin_lending_rates(api_key=None, api_secret=None, subaccount_name=None, coin=None) -> List[dict]:
    client = FTXClient(api_key, api_secret, subaccount_name)
    response = client.get(f'/spot_margin/lending_rates')
    result = []
    for asset in response:
        if coin:
            if asset['coin'] == coin:
                result.append(asset)
                break
        else:
            result.append(asset)
    return result

def _get_coin_lending_info(api_key=None, api_secret=None, subaccount_name=None, coin=None) -> List[dict]:
    client = FTXClient(api_key, api_secret, subaccount_name)
    response = client.get(f'/spot_margin/lending_info')
    result = []
    for asset in response:
        if coin:
            if asset['coin'] == coin:
                result.append(asset)
                break
        else:
            result.append(asset)
    return result

def _submit_lending_offer(api_key, api_secret, subaccount_name, coin, size, rate) -> dict:
    client = FTXClient(api_key, api_secret, subaccount_name)
    response = client.post(f'/spot_margin/offers',{'coin': coin,'size': size, 'rate': rate})
    return response

def _print_lending_rates_details(coin: dict) -> None:
    print('Coin: ' + str(coin['coin']))
    print('     Estimate (APY): ' + str(truncate(coin['estimate']*24*36500,2)) + '%')
    print('     Previous (APY): ' + str(truncate(coin['previous']*24*36500,2)) + '%')

def _print_lending_details(coin: dict) -> None:
    print('Coin: ' + str(coin['coin']))
    print('     Locked   : ' + str(truncate(coin['locked'],8)))
    print('     Offered  : ' + str(truncate(coin['offered'],8)))
    print('     Lendable : ' + str(truncate(coin['lendable'],8)))
    print('     Rate (APY): ' + str(truncate(coin['minRate']*24*36500,2)) + '%')

def _print_lending_offer_details(coin: dict) -> None:
    print('Coin: ' + str(coin['coin']))
    print('     Amount (old): ' + str(truncate(coin['locked'],8)))
    print('     Amount (new): ' + str(truncate(coin['lendable'],8)))
    print('     Rate (APY)  : ' + str(truncate(coin['minRate']*24*36500,2)) + '%')

def get_coin_lending_rates(api_key=None, api_secret=None, subaccount_name=None, coin=None) -> None:
    wallet = 'Main account'
    if subaccount_name:
        wallet = 'Subaccount ' + subaccount_name
    print(wallet)
    if isinstance(coin, str):
        coin = tuple([coin])
    try:
        for x in coin:
            result = _get_coin_lending_rates(api_key, api_secret, subaccount_name, x)
            for asset in result:
                logging.info(wallet + ' | Getting Lending Rates for ' + asset['coin'])
                _print_lending_rates_details(asset)
    except Exception as e:
        logging.error(wallet + ' - Error getting Lending Rates.')
        logging.error(wallet + ' - ' + str(e))
        print('Error getting Lending Rates.')
        print(e)

def get_coin_lending_info(api_key=None, api_secret=None, subaccount_name=None, coin=None) -> None:
    wallet = 'Main account'
    if subaccount_name:
        wallet = 'Subaccount ' + subaccount_name
    print(wallet)
    if isinstance(coin, str):
        coin = tuple([coin])
    try:
        for x in coin:
            result = _get_coin_lending_info(api_key, api_secret, subaccount_name, x)
            for asset in result:
                if asset['lendable'] > 0:
                    logging.info(wallet + ' - Getting Lending Info for ' + asset['coin'])
                    _print_lending_details(asset)
    except Exception as e:
        logging.error(wallet + ' - Error getting Lending Info.')
        logging.error(wallet + ' - ' + str(e))
        print('Error getting Lending Info.')
        print(e)

def compound_lending(api_key=None, api_secret=None, subaccount_name=None, coin=None) -> None:
    if coin:
        wallet = 'Main account'
        if subaccount_name:
            wallet = 'Subaccount ' + subaccount_name
        print(wallet)
        if isinstance(coin, str):
            coin = tuple([coin])
        for x in coin:
            coin_detail = _get_coin_lending_info(api_key, api_secret, subaccount_name, x)
            if coin_detail[0]:
                if truncate(coin_detail[0]['lendable'],8)  > truncate(coin_detail[0]['locked'],8):
                    try:
                        result = _submit_lending_offer(api_key, api_secret, subaccount_name, coin_detail[0]['coin'], truncate(coin_detail[0]['lendable'],8), coin_detail[0]['minRate'])
                        logging.info(wallet + ' - Updated Lending Offer for ' + str(coin_detail[0]['coin']) + ' from ' + str(truncate(coin_detail[0]['locked'],8)) + ' to ' + str(coin_detail[0]['lendable']) + ' at ' + str(truncate(coin_detail[0]['minRate']*24*36500,2)) + '% APY')
                        _print_lending_offer_details(coin_detail[0])
                    except Exception as e:
                        logging.error(wallet + ' - Error updating Lending Offer for ' + str(coin_detail[0]['coin']))
                        logging.error(wallet + ' - ' + str(e))
                        print('Error updating Lending Offer for ' + str(coin_detail[0]['coin']))
                        print(e)
                else:
                    logging.info(wallet + ' - No changes to Lending Offer for ' + str(coin_detail[0]['coin']) + ' ' + str(coin_detail[0]['lendable']) + ' at ' + str(truncate(coin_detail[0]['minRate']*24*36500,2)) + '% APY')
                    _print_lending_offer_details(coin_detail[0])
                    print('     No need to update lending amount.')

if __name__ == '__main__':
    fire.Fire({
        'info': get_coin_lending_info,
        'compound': compound_lending,
        'rates': get_coin_lending_rates,
    })
