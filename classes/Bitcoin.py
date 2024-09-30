import requests
import json
from interfaces.bitcoin import Bitcoin as IBitcoin

class Bitcoin(IBitcoin):

    def __init__(self, url: str, port: int, login: str, password: str):
        """
        :param url:
        :param port:
        :param login:
        :param password:
        """
        self.url = url
        self.port = port
        self.login = login
        self.password = password

    def get_info(self):
        return self.__method("getblockchaininfo", [])

    def check(self):
        try:
            self.get_info()
        except Exception:
            return False

        return True


    def __get_url(self):
        return "http://{}:{}@{}:{}/".format(self.login, self.password, self.url, self.port)

    def __method(self, method, params):
        url = self.__get_url()

        payload = {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": 0,
        }

        response = requests.post(url, json=payload)

        return response.json()['result']

    def generateAddr(self):
        return self.__method("getnewaddress", [])

    def checkAddr(self, btc_addr):
        return self.__method("getreceivedbyaddress", [btc_addr, 0])