import pandas as pd
from utils.singleton import singleton
from DiceService.DiceSet import DiceSet, Dice
from TheOneRingDetails.DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType
from TableService.TableLoader import TableLoader
from TableService.Record import Record

class Table:
    def __init__(self, eventClassId: int, path="data/Table.xlsx", sheetName="Zdarzenia", dices: list[Dice] = [DiceTheOneRing(DiceTheOneRingType.FEAT), DiceTheOneRing(DiceTheOneRingType.SUCCESS)]):
        self._records = TableLoader.loadRecords(eventClassId, path, sheetName)  # Changed __records to _records
        self._diceSet: DiceSet = DiceSet(dices)

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

