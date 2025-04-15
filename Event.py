from dataclasses import dataclass, fields
from pandas import Series
from abc import ABC, abstractmethod

@dataclass
class Event:
    description:str

    def __str__(self):
        return (
            f"Event: {self.description}\n"
        )
    
    @classmethod
    def fromRow(cls, row: Series):
        return cls(
            description = "Default",
        )
    
    @abstractmethod
    def isThisEvent(self, results: list[int]) -> bool:
        pass
    