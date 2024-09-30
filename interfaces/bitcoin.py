from abc import ABC, abstractmethod

class Bitcoin:
    @abstractmethod
    def generateAddr(self):
        pass

    @abstractmethod
    def checkAddr(self, btc_addr):
        pass