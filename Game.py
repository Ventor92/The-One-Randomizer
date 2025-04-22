from TableService.Table import Table, Record
from abc import abstractmethod

class Game:
    def __init__(self, title: str = "Game", tables: list[Table] = []):
        self.title = title
        self.tables: list[Table] = tables

    @abstractmethod
    def getRecord(self, tableType, results: list[int]) -> Record:
        pass

    @abstractmethod
    def rollRecord(self, tableType) -> Record:
        pass
