import pandas as pd

from DiceService.DiceSet import DiceSet, Dice
from TableService.TableLoader import TableLoader
from TableService.Record import Record

class Table:
    def __init__(self, recordType: type[Record], path, sheetName, dices: list[Dice]):
        self._name = sheetName
        self._recordType = recordType
        self._path = path
        # self._records: list[Record] = TableLoader.loadRecords(recordType, path, sheetName)  # Changed __records to _records
        self._records: list[Record] = []  # Changed __records to _records
        self._diceSet: DiceSet = DiceSet(dices)
        print(f"Table __init__")

    def isRecordType(self, recordType: type[Record]) -> bool:

        if isinstance(self._records[0], recordType):
            return True
        else:
            return False

    def getDiceSet(self) -> DiceSet:
        return self._diceSet
    
    def roll(self) -> list[int]:
        results: list[int] = self.getDiceSet().roll()
        return results
    
    def getRecord(self, results: list[int]) -> Record | None:
        for record in self._records:  # Changed __records to _records
            if True == record.isThisRecord(results):
                return record
            else:
                pass

    def getName(self) -> str:
        return self._name
    
    def getAllRecords(self) -> list[Record]:
        return self._records
    
    def getRecordType(self) -> type[Record]:
        return self._recordType
    
    def loadRecords(self) -> list[Record]:
        self._records = TableLoader.loadRecords(self._recordType, self._path, self._name)
        return self._records