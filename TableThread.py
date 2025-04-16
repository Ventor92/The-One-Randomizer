from typing import List, cast
import pandas as pd
from Thread import Thread  # zakładam, że masz klasę Thread w osobnym pliku
from utils.singleton import singleton
from Table import Table
from Record import Record
from DiceTheOneRing import Dice, DiceTheOneRing, DiceTheOneRingType
from DiceSet import DiceSet

from TableLoader import TableLoader

@singleton
class TableThread(Table):
    def __init__(self, threadClassId:int , path="data/Table.xlsx", sheetName="Wątki", dices: list[Dice] = [DiceTheOneRing(DiceTheOneRingType.FEAT), DiceTheOneRing(DiceTheOneRingType.SUCCESS)]):
        super().__init__(threadClassId, path, sheetName, dices)  # Call the parent class's __init__

    def getThread(self, results: list[int]) -> Thread | None:
        for t in self._records:  # Changed __records to _records
            if isinstance(t, Thread) and t.isThisRecord(results):  # Sprawdzenie, czy t jest typu Thread
                print(t)
                return t
        return None
    
    def rollThread(self) -> Thread | None:
        results: list[int] = self.roll()
        thread: Thread | None = self.getThread(results)
        return thread
    
    # def getThreadsByFeat(self, dieFeatValue: int) -> List[Thread]:
    #     return [t for t in self.__records if t.dieFeat == dieFeatValue]