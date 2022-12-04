import requests
import configparser
from datetime import datetime
from http.client import IncompleteRead
import http.client as http
import urllib3
import socket
main_config = configparser.ConfigParser()
main_config.read('./configs/mainconf.ini')
api_version = main_config.get('ADSBX', 'API_VERSION')

def pull_adsbx(planes):
    api_version = int(main_config.get('ADSBX', 'API_VERSION'))
    if api_version not in [1, 2]:
        raise ValueError("Bad ADSBX API Version")
    if main_config.getboolean('ADSBX', 'ENABLE_PROXY') is False:
        if api_version ==  1:
            if len(planes) > 1:
                        url = "https://adsbexchange.com/api/aircraft/json/"
            elif len(planes) == 1:
                        url = "https://adsbexchange.com/api/aircraft/icao/" +    str(list(planes.keys())[0]) + "/"
        elif api_version == 2:
            url = "https://adsbexchange.com/api/aircraft/v2/all"
    else:
        if main_config.has_option('ADSBX', 'PROXY_HOST'):
            if api_version ==  1:
                url = main_config.get('ADSBX', 'PROXY_HOST') + "/api/aircraft/json/all"
            if api_version ==  2:
                url = main_config.get('ADSBX', 'PROXY_HOST') + "/api/aircraft/v2/all"
        else:
            raise ValueError("Proxy enabled but no host")
    headers = {
        'api-auth': main_config.get('ADSBX', 'API_KEY'),
        'Accept-Encoding': 'gzip'
    }
    try:
        response = requests.get(url, headers = headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        if "msg" in data.keys() and data['msg'] != "No error":
            raise ValueError("Error from ADSBX: msg = ", data['msg'])
        if "ctime" in data.keys():
            data_ctime = float(data['ctime']) / 1000.0
            print("Data ctime:",datetime.utcfromtimestamp(data_ctime))
        if "now" in data.keys():
            data_now = float(data['now']) / 1000.0
            print("Data now time:",datetime.utcfromtimestamp(data_now))
    print("Current UTC:", datetime.utcnow())
    return data
    except Exception as e:
            print('Error calling ADSBExchange', e)
    return None

def pull_date_ras(date):
    url = f"https://globe.adsbexchange.com/globe_history/{date}/acas/acas.json"
    headers = {
                'Accept-Encoding': 'gzip'
    }
    try:
        response = requests.get(url, headers = headers, timeout=30)
        response.raise_for_status()
        return response.text.splitlines()
    except Exception as e:
            print('Error pulling date ras', e)
    return None