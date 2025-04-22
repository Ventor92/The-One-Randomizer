from TableService.Table import Table, Record
from abc import abstractmethod

class Game:
    def __init__(self, title: str = "Game"):
        self.title = title
        self.tables: list[Table] = []

    @abstractmethod
    def getRecord(self, tableType, results: list[int]) -> Record:
        pass

    @abstractmethod
    def rollRecord(self, tableType) -> Record:
        pass
