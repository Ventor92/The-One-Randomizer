import pandas as pd

from abc import ABC, abstractmethod

class GenericTableLoaderExcel:
    def __init__(self, path: str, sheet_name:str) -> None:
        super().__init__()
        self._path:str = path
        self._sheet_name:str = sheet_name

    def loadGenericRecords(self) -> pd.DataFrame:
        dataFrame: pd.DataFrame = pd.read_excel(self._path, self._sheet_name)
        return dataFrame
    
class GenericTableLoader:
    @staticmethod
    def loadRecords(path: str, sheet_name:str) -> pd.DataFrame:
        loader = GenericTableLoaderExcel(path, sheet_name)
        dataFrame = loader.loadGenericRecords()
        return dataFrame
