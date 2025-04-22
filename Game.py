from TableService.Table import Table, Record
from abc import abstractmethod

class Game:
    def __init__(self, title: str = "Game", tables: list[Table] = []):
        self.title = title
        self.tables: list[Table] = tables

    def _getTable(self, tableType: type[Table]) -> Table:
        for table in self.tables:
            if isinstance(table, tableType):  # Compare with the class of the singleton
                return table
        raise ValueError(f"Table of type {tableType} not found in game {self.title}.")

    def getRecord(self, tableType: type[Table], results: list[int]) -> Record:
        table = self._getTable(tableType)
        record =  table.getRecord(results)
        if isinstance(record, Record):
            print(record)
            return record
        else:
            raise ValueError(f"Record is not of type {tableType}: {record}")
        
    def rollRecord(self, tableType: type[Table]) -> Record:
        table = self._getTable(tableType)
        results = table.roll()
        record = self.getRecord(tableType, results)
        return record
