import os
import sys
import json

from classes.Privateness import Privateness

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

            ness = Privateness(jsn['ness']['host'], jsn['ness']['port'], jsn['ness']['wallet-id'], jsn['ness']['wallet-password'])
            
            if ness.check():
                print("NESS Check OK")
                print (json.loads(ness.get_info().content))
                # Check from_addr
                print("Balance of {}:".format(jsn['ness']['test-addr-from']))
                print(ness.checkAddr(jsn['ness']['test-addr-from']))
                # Send from addr to addr
                print("Sending from: {} to: {}".format(jsn['ness']['test-addr-from'], jsn['ness']['test-addr-to']))
                ness.send(jsn['ness']['test-addr-from'], jsn['ness']['test-addr-to'], jsn['ness']['test-coins'], jsn['ness']['test-hours'])
                # Check to_addr
                print("Balance of {}:".format(jsn['ness']['test-addr-to']))
                print(ness.checkAddr(jsn['ness']['test-addr-to']))
            else:
                print ("NESS Check FAILED")

upd = TEST()
upd.process()