import requests
import json
from interfaces.privateness import Privateness as IPrivateness

class Privateness(IPrivateness):

    def __init__(self, url: str, port: int, wallet_id: str, wallet_password: str):
        """
        :param url:
        :param port:
        :param wallet_id:
        :param wallet_password:
        """
        self.url = url
        self.port = port
        self.wallet_id = wallet_id
        self.wallet_password = wallet_password

    def __get_url(self, method: str):
        return "http://{}:{}/api/v1/{}".format(self.url, self.port, method)

    def __get(self, method: str):
        url = self.__get_url(method)
        response = requests.get(url)

        return response

    def __post(self, method: str, headers: dict, params):
        url = self.__get_url(method)
        response = requests.request('POST', url, headers=headers, params=params).json()

        return response

    def __post_token(self, method: str, params):
        url = self.__get_url("csrf")
        response = requests.get(url)
        csrf = response.json()['csrf_token']

        url = self.__get_url(method)
        headers = {"X-CSRF-Token": csrf}
        response = requests.request('POST', url, headers=headers, params=params)

        return response.json()

    def __post_token_json(self, method: str, json):
        url = self.__get_url("csrf")
        response = requests.get(url)
        csrf = response.json()['csrf_token']

        url = self.__get_url(method)
        headers = {"Content-Type": "application/json", "X-CSRF-Token": csrf}
        response = requests.request('POST', url, headers=headers, json=json)

        return response.json()

    def get_version(self):
        return self.__get('version')

    def get_info(self):
        return self.__get('blockchain/metadata')

    def check(self):
        try:
            self.get_info()
        except Exception:
            return False

        return True

    def checkAddr(self, addr: str):
         resp = self.__post_token('balance', {"addrs": [addr]})
         return resp["addresses"][addr]

    def generateAddr(self):
        params = {
            'id': self.wallet_id,
            'num': 1,
            'password': self.wallet_password
        }

        return self.__post_token("newAddress")

    def send(self, from_addr: str, to_addr: str, coins: float, hours: int):
        # Transaction
        body = '''
        {{
            "hours_selection": {{
                "type": "manual"
            }},
            "wallet_id": "{}",
            "password": "{}",
            "addresses": ["{}"],
            "to": [{{
                "address": "{}",
                "coins": "{}",
                "hours": "{}"
            }}]
        }}
        '''.format(self.wallet_id, self.wallet_password, from_addr, to_addr, coins, hours)
        jsn = json.loads(body)
        response = self.__post_token_json('wallet/transaction', jsn)
        encoded_transaction = response['encoded_transaction']

        # Inject transaction
        body = '{{"rawtx": "{}"}}'.format(encoded_transaction)
        jsn = json.loads(body)
        response = self.__post_token_json('injectTransaction', jsn)

        return response