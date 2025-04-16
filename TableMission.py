from typing import List, cast
import pandas as pd
from Record import Record
from utils.singleton import singleton
from Table import Table
from DiceTheOneRing import Dice, DiceTheOneRing, DiceTheOneRingType

from TableLoader import TableLoader

@singleton
class TableMission(Table):
    def __init__(self, missionClassId:int , path="data/Table.xlsx", sheetName="Missions", dices: list[Dice] = [DiceTheOneRing(DiceTheOneRingType.FEAT), DiceTheOneRing(DiceTheOneRingType.SUCCESS)]):
        super().__init__(missionClassId, path, sheetName, dices)  # Call the parent class's __init__

    def getMission(self, results: list[int]) -> Record | None:
        for m in self._records:
            if m.isThisRecord(results):
                print(m)
                return m
        return None
    
    def rollMission(self) -> Record | None:
        results: list[int] = self.roll()
        mission: Record | None = self.getMission(results)
        return mission