from pandas import Series
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Record:
    id:str
    
    @classmethod
    def fromRow(cls, row: Series):
        return cls(
            id = "recordId",
        )
    pass

    @abstractmethod
    def isThisRecord(self, results: list[int]) -> bool:
        pass