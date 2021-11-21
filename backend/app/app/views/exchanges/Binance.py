#!/usr/bin/env python3

import requests
import hmac
import time
from hashlib import sha256
from urllib.parse import urlencode

from requests import api


class Binance:
    def __init__(self, api_key, api_secret):
        self._api_url = "http://api.binance.com"
        self._api_key = api_key
        self._api_secret = api_secret

    def _gen_sig(self, params):
        return hmac.new(self._api_secret.encode(), urlencode(params).encode(), sha256).hexdigest()

    def _create_request(self, api, params, use_sig=True, use_timestamp=True):
        headers = {
            "Accept": "application/json"
        }
        headers["X-MBX-APIKEY"] = self._api_key
        if use_timestamp:
            params["timestamp"] = int(time.time()*1000)
        if use_sig:
            params["signature"] = self._gen_sig(params)
        return requests.get(api, params=params, headers=headers)
    
    def check_connection(self):
        api = f"{self._api_url}/sapi/v1/system/status"
        return self._create_request(api, {}, use_sig=False).json()

    def get_deposit_record(self):
        api = f"{self._api_url}/sapi/v1/capital/deposit/hisrec"
        return self._create_request(api, {}).json()

    def get_tx_history(self, pair, **kwargs):
        """Get transaction history for pair

        Args:
            pair (String): coin/base pair

        Returns:
            List: List of transaction history
        """
        api = f"{self._api_url}/api/v3/myTrades"
        param = {"symbol": pair}
        for k,v in kwargs.items():
            param[k] = v
        return self._create_request(api, param).json()
    
    def get_current_price(self, pair):
        """Get current price for pair

        Args:
            pair (String): coin/base pair

        Returns:
            float: Current price for pair
        """
        api = f"{self._api_url}/api/v3/ticker/price"
        param = {"symbol": pair}
        return float(self._create_request(api, param, use_sig=False, use_timestamp=False).json()["price"])
    
    def get_history_price(self, pair, start_time):
        """Get Binance history price

        Args:
            pair (String): code/base prir
            start_time (Long): UNIX timestamp

        Returns:
            float: History price at start_time for pair
        """
        api = f"{self._api_url}/api/v3/klines "
        param = {
            "symbol": pair,
            "interval": "1m",
            "limit": 1,
            "startTime": start_time
        }
        req = _create_request(api, param).json()
        return (float(req[0][2]) + float(req[0][3])) / 2

    def check_account_status(self):
        """Check Binance account status

        Returns:
            Boolean: account status
        """
        api = f"{self._api_url}/sapi/v1/account/status"
        return self._create_request(api, {}).json()["data"] == "Normal"

    def get_deposit_record(self):
        """Get deposit record

        Returns:
            json: Deposit records
        """
        api = f"{self._api_url}/sapi/v1/capital/deposit/hisrec"
        return self._create_request(api, {}).json()
