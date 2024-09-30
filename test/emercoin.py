import os
import sys
import json

from classes.Emercoin import Emercoin

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

            emc = Emercoin(jsn['emc']['rpc-host'], jsn['emc']['rpc-port'], jsn['emc']['rpc-user'], jsn['emc']['rpc-password'])
            if emc.check():
                print ("EMERCOIN Check OK")
                print ("List of tokens:")
                print(emc.getTokens())
            else:
                print ("EMERCOIN Check FAILED")

upd = TEST()
upd.process()