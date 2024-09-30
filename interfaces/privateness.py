from abc import ABC, abstractmethod

class Privateness(ABC):
    @abstractmethod
    def generateAddr(self):
        pass

    @abstractmethod
    def checkAddr(self, addr: str):
        pass

    @abstractmethod
    def send(self, from_addr: str, to_addr: str, coins: float, hours: int):
        pass