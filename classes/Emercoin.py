import requests
import json
from interfaces.emercoin import Emercoin as IEmercoin

class Emercoin(IEmercoin):

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
        return self.__method("getinfo", [])

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
        # print(url)
        payload = {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": 0,
        }

        response = requests.post(url, json=payload)
        # print(response.text)
        # print(response.status_code)
        return response.json()['result']
        # jsn = response.json()
        # return jsn

    def showToken(self, ness_addr):
        return self.__method("name_show", ['^token:exchange:privateness1:' + ness_addr, '', 'base64'])

    def getTokens(self):
        return self.__method("name_filter", ['^token:exchange:privateness1:.+', 0, 0, 0, '', ''])

    def generateAddr(self):
        return self.__method("getnewaddress", ['exchange:privateness1'])
  