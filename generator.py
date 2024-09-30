import os
import sys
import json

from classes.Bitcoin import Bitcoin
from classes.Emercoin import Emercoin


class Generator:

    config_file = 'config.json'
    addresses_file = 'addresses.json'

    def __init__(self):
        f = open(self.config_file)
        content = f.read()
        jsn = json.loads(content)

        self.btc = Bitcoin(jsn['btc']['rpc-host'], jsn['btc']['rpc-port'], jsn['btc']['rpc-user'], jsn['btc']['rpc-password'])
        self.emc = Emercoin(jsn['emc']['rpc-host'], jsn['emc']['rpc-port'], jsn['emc']['rpc-user'], jsn['emc']['rpc-password'])

    def __check_for_file(self):
        return os.path.isfile(self.addresses_file)

    def __generate(self, addr_type: str, ammount: int):
        addresses = []

        for i in range(ammount):
            if (addr_type == 'btc'):
                addresses.append(self.btc.generateAddr())
            elif (addr_type == 'emc'):
                addresses.append(self.emc.generateAddr())

        return addresses

    def __show_addresses(self):
        f = open(self.addresses_file, 'r')
        return json.loads(f.read())

    def generate_and_save(self, ammount: int, addr_type: str):
        if self.__check_for_file():
            addresses = self.__show_addresses()
            if not addr_type in addresses:
                 addresses[addr_type] = []
        else:
            addresses = {addr_type: []}

        difference = ammount - len(addresses[addr_type])

        if difference > 0:
            new_addresses = self.__generate(addr_type, difference)
        else:
            return False

        for address in new_addresses:
            addresses[addr_type].append(address)

        f = open(self.addresses_file, 'w')
        f.write(json.dumps(addresses, indent=4))
        f.close()

        return True

    def show_key(self):
        print("exchange:privateness1:BTC:NESS")

    def show_addresses(self, addr_type: str):
        if self.__check_for_file():
            addresses = self.__show_addresses()[addr_type]
            print( json.dumps(addresses, indent=4) )
            return True
        else:
            return False

    def show_value(self):
        if self.__check_for_file():
            addresses = self.__show_addresses()
            out = {"ratio" : 1000000, "addresses": addresses}

            print( json.dumps(out, indent=4))
            return True
        else:
            print( "File {} does not exist" )
            return False

class Processor:

    def __init__(self):
        self.gen = Generator()

    def __manual(self):
        print("*** Bitcoin addresses generator")
        print("### USAGE:")
        print("#### Generate bitcoin addresses:")
        print("python generator.py generate btc <ammount>")
        print("python generator.py generate emc <ammount>")
        print("#### Show EMC NVS key:")
        print("python generator.py show key")
        print("#### Show EMC NVS value:")
        print("python generator.py show value")
        print("#### Show generated addresses:")
        print("python generator.py show addresses emc")
        print("#### Show generated addresses:")
        print("python generator.py show addresses btc")

    def process(self):
        if len(sys.argv) == 4 and sys.argv[1].lower() == 'generate' and ('btc', 'emc').index(sys.argv[2].lower()) != False and sys.argv[3].isdigit():
            if self.gen.generate_and_save(int(sys.argv[3]), sys.argv[2].lower()):
                print ('OK')
            else:
                print ("Ammount {} is less than olready generated addresses")
        elif len(sys.argv) == 3 and (sys.argv[1].lower() == 'show' and sys.argv[2].lower() == 'key'):
            self.gen.show_key()
        elif len(sys.argv) == 3 and (sys.argv[1].lower() == 'show' and sys.argv[2].lower() == 'value'):
            if not self.gen.show_value():
                print ("Addresses are not generated")
                print ("USE")
                print ("python generator.py generate <emc|btc> <ammount>")
        elif len(sys.argv) == 4 and (sys.argv[1].lower() == 'show' and sys.argv[2].lower() == 'addresses' and sys.argv[3].lower() == 'emc'):
            if not self.gen.show_addresses('btc'):
                print ("Addresses are not generated")
                print ("USE")
                print ("python generator.py generate <emc|btc> <ammount>")
        elif len(sys.argv) == 4 and (sys.argv[1].lower() == 'show' and sys.argv[2].lower() == 'addresses' and sys.argv[3].lower() == 'btc'):
            if not self.gen.show_addresses('emc'):
                print ("Addresses are not generated")
                print ("USE")
                print ("python generator.py generate <emc|btc> <ammount>")

        else:
            self.__manual()

upd = Processor()
upd.process()