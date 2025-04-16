from dataclasses import dataclass
from abc import ABC, abstractmethod

import pandas as pd
from pandas import Series
from Record import Record

@dataclass
class Thread(Record):
    description:str

    @classmethod
    def fromRow(cls, row: Series):
        return cls(
            id = "threadId",
            description = "Default",
        )

    def __str__(self):
        return (
            f"Thread: {self.description}\n"
        )
        
    @abstractmethod
    def isThisRecord(self, results: list[int]) -> bool:
        pass