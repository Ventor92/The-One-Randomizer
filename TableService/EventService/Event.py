from dataclasses import dataclass, fields
from pandas import Series
from abc import ABC, abstractmethod
from TableService.Record import Record
@dataclass
class Event(Record):
    description:str

    def __str__(self):
        return (
            f"Event: {self.description}\n"
        )
    
    @classmethod
    def fromRow(cls, row: Series):
        return cls(
            id = "eventId",
            description = "Event",
        )
    
    @abstractmethod
    def isThisRecord(self, results: list[int]) -> bool:
        pass