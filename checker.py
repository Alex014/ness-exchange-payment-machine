import os
import sys
import json
import datetime

from classes.Privateness import Privateness
from classes.Bitcoin import Bitcoin
from classes.Emercoin import Emercoin


class Checker:

    config_file = 'config.json'
    config = {}
    exceptions = {}

    def __init__(self):
        f = open(self.config_file)
        content = f.read()
        jsn = json.loads(content)

        self.ness = Privateness(jsn['ness']['host'], jsn['ness']['port'], jsn['ness']['wallet-id'], jsn['ness']['wallet-password'])
        self.btc = Bitcoin(jsn['btc']['rpc-host'], jsn['btc']['rpc-port'], jsn['btc']['rpc-user'], jsn['btc']['rpc-password'])
        self.emc = Emercoin(jsn['emc']['rpc-host'], jsn['emc']['rpc-port'], jsn['emc']['rpc-user'], jsn['emc']['rpc-password'])

    def load_tokens(self):
        return self.emc.getTokens()

    def check_token(self, token: dict):
        try:
            name = token['name'].split(':')
            value = json.loads(token['value'])
            ness_addr = name[3]
            btc_addr = value['btc_addr']
            ratio = self.config['ness']['ratio']
            btc_balance = self.btc.checkAddr(btc_addr)
            ness_balance = self.ness.checkAddr(ness_addr)['predicted']['coins']

            print(" * {:15} - BTC {}:{} NESS {}:{}".format(value['name'], btc_addr, btc_balance, ness_addr, ness_balance), flush=True)

            if btc_balance > 0:
                if ness_balance == 0:
                    return True
                else:
                    return btc_balance*ratio > ness_balance
            else:
                return False

        except Exception as e:
            self.exceptions[token['name']] = repr(e)
            return False

    def pay_token(self, token: dict):
        try:
            name = token['name'].split(':')
            value = json.loads(token['value'])
            ness_addr_pay_from = self.config['ness']['addr-from']
            ness_addr = name[3]
            btc_addr = value['btc_addr']
            ratio = self.config['ness']['ratio']
            btc_balance = self.btc.checkAddr(btc_addr)
            ness_balance = self.ness.checkAddr(ness_addr)['predicted']['coins']

            ness_need_balance = btc_balance*ratio

            ness_pay_balance = btc_balance*ratio - ness_balance

            self.ness.send(ness_addr_pay_from, ness_addr, ness_pay_balance, ness_pay_balance)

            print("\n + {:15} - {}: {} NESS\n".format(value['name'], ness_addr, ness_pay_balance), flush=True)

        except Exception as e:
            self.exceptions[token['name']] = repr(e)
            return False

    def process_tokens(self):
        if not os.path.isfile(self.config_file):
            print("*** Error:")
            print("File '{}' does not exist".format(self.config_file))
            return False
        else:
            f = open(self.config_file)
            content = f.read()
            self.config = json.loads(content)

        tokens = self.load_tokens()

        if tokens != False:
            for token in tokens:
                if self.check_token(token):
                    self.pay_token(token)

        return True


class Processor:

    def __init__(self):
        self.chk = Checker()

    def process(self):
        self.chk.process_tokens()
        
        f = open('log/' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.json', 'w')
        f.write(json.dumps(self.chk.exceptions))
        f.close()


upd = Processor()
upd.process()