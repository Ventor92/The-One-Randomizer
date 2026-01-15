from pandas import Series
from dataclasses import dataclass
from abc import ABC, abstractmethod

import random
import string

@dataclass
class GenericRecord:
    id:str
    data: list[str]

    def __post_init__(self):
        if self.id is None or self.id == "" or len(self.id) != 8:
            self.id = Record.hashGen(8)

    @staticmethod
    def hashGen(len:int = 8) -> str:
        output = ''.join(random.choices(string.ascii_lowercase + string.digits, k=len))
        print(f"Generated hash: {output}")
        return output

    @classmethod
    def fromRow(cls, row: list[str]):
        return cls(
            id = "1",
            data = row,
        )
@dataclass
class Record:
    id:str

    def __post_init__(self):
        if self.id is None or self.id == "" or len(self.id) != 8:
            self.id = Record.hashGen(8)

    @staticmethod
    def hashGen(len:int = 8) -> str:
        output = ''.join(random.choices(string.ascii_lowercase + string.digits, k=len))
        print(f"Generated hash: {output}")
        return output
    
    @classmethod
    def fromRow(cls, row: Series):
        return cls(
            id = row['id'],
        )
    pass

    @abstractmethod
    def toRow(self) -> Series:
        pass
        # row = Series({
        #     'id': self.id,
        # })
        # return row

    @abstractmethod
    def isThisRecord(self, results: list[int]) -> bool:
        pass

    @abstractmethod
    def toRawDict(self) -> dict:
        pass