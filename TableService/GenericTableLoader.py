import pandas as pd
# from Event import Event
from TableService.Record import GenericRecord, Record

from abc import ABC, abstractmethod

class GenericTableLoaderExcel:
    def __init__(self, path: str, sheet_name:str) -> None:
        super().__init__()
        self._path:str = path
        self._sheet_name:str = sheet_name

    @staticmethod
    def _loadRecords(path: str, sheet_name:str) -> list[GenericRecord]:
        table = pd.read_excel(path, sheet_name)
        records: list[GenericRecord] = []
        for _, row in table.itertuples():
            e = GenericRecord.fromRow(row)
            records.append(e)
        return records

    def loadGenericRecords(self) -> pd.DataFrame:
        dataFrame: pd.DataFrame = pd.read_excel(self._path, self._sheet_name)
        return dataFrame
    
class GenericTableLoader:
    @staticmethod
    def loadRecords(path: str, sheet_name:str) -> pd.DataFrame:
        loader = GenericTableLoaderExcel(path, sheet_name)
        dataFrame = loader.loadGenericRecords()
        return dataFrame  
