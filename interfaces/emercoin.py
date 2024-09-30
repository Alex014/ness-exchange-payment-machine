from abc import ABC, abstractmethod

class Emercoin(ABC):
    @abstractmethod
    def showToken(self, ness_addr):
        pass

    @abstractmethod
    def getTokens(self):
        pass