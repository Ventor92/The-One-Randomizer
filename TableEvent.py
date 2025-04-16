import pandas as pd
from Event import Event
from utils.singleton import singleton
from Dice import Dice
from DiceSet import DiceSet
from DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType
from TableLoader import TableLoader
from Table import Table

@singleton
class TableEvent(Table):
    def __init__(self, eventClassId: int, path="data/Table.xlsx", sheetName="Zdarzenia", dices: list[Dice] = [DiceTheOneRing(DiceTheOneRingType.FEAT), DiceTheOneRing(DiceTheOneRingType.SUCCESS)]):
        super().__init__(eventClassId, path, sheetName, dices)  # Call the parent class's __init__

    # def getDiceSet(self) -> DiceSet:
    #     return self.__diceSet
    
    # def __roll(self) -> list[int]:
    #     results: list[int] = self.__diceSet.roll()
    #     return results
    
    def rollEvent(self) -> Event | None:
        results: list[int] = self.roll()
        event: Event | None = self.getEvent(results)
        return event
    
    def getEvent(self, results: list[int]) -> Event | None:
        for e in self._records:
            if isinstance(e, Event):
                if e.isThisRecord(results):  # Sprawdzenie, czy e jest typu Event
                    print(e)
                    return e
        return None

