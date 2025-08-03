import pandas as pd
# from Event import Event
from TableService.Record import Record

from abc import ABC, abstractmethod
class TableLoaderV2:

    @abstractmethod
    def loadRecords(self) -> list[Record]:
        ...

class TableLoaderExcel(TableLoaderV2):
    def __init__(self, recordType: type[Record], path: str, sheet_name:str) -> None:
        super().__init__()
        self._path:str = path
        self._sheet_name:str = sheet_name
        self._recordType: type[Record] = recordType

    @staticmethod
    def _loadRecords(recordType: type[Record], path: str, sheet_name:str) -> list[Record]:
        table = pd.read_excel(path, sheet_name)
        events = []
        for _, row in table.iterrows():
            e = recordType.fromRow(row)
            events.append(e)
        return events
    
    def loadRecords(self) -> list[Record]:
        return self._loadRecords(self._recordType, self._path, self._sheet_name)
    
class TableLoader:

    @staticmethod
    def loadRecords(recordType: type[Record], path: str, sheet_name:str) -> list[Record]:
        loader = TableLoaderExcel(recordType, path, sheet_name)
        records = loader.loadRecords()
        return records  
