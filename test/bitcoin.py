import os
import sys
import json

from classes.Bitcoin import Bitcoin

class TEST:

    config_file = 'config.json'

    def process(self):

        if not os.path.isfile(self.config_file):
            print("*** Error:")
            print("File '{}' does not exist".format(self.config_file))
            return False
        else:
            f = open(self.config_file)
            content = f.read()
            jsn = json.loads(content)

            btc = Bitcoin(jsn['btc']['rpc-host'], jsn['btc']['rpc-port'], jsn['btc']['rpc-user'], jsn['btc']['rpc-password'])
            if btc.check():
                print ("BITCOIN Check OK")
                # Create addr
                addr = btc.generateAddr()
                print ("Generated addr: " + addr)
                # Check addr
                balance = btc.checkAddr(addr)
                print ("Balance of {}: {}".format(addr, balance))
            else:
                print ("BITCOIN Check FAILED")

upd = TEST()
upd.process()