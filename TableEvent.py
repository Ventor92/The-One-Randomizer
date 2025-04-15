import pandas as pd
from Event import Event
from utils.singleton import singleton
from Dice import Dice
from DiceSet import DiceSet
from DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType
from EventTableLoader import EventTableLoader



@singleton
class TableEvent:
    def __init__(self, eventClassId: int, path="data/TableEvent.xlsx", sheetName="Zdarzenia", dices: list[Dice] = [DiceTheOneRing(DiceTheOneRingType.FEAT), DiceTheOneRing(DiceTheOneRingType.SUCCESS)]):
        self.__events = EventTableLoader.loadEvents(eventClassId, path, sheetName)
        self.__diceSet: DiceSet = DiceSet(dices)

    def getDiceSet(self) -> DiceSet:
        return self.__diceSet
    
    def __roll(self) -> list[int]:
        results: list[int] = self.__diceSet.roll()
        return results
    
    def randomEvent(self) -> Event | None:
        results: list[int] = self.__roll()
        event: Event | None = self.getEvent(results)
        return event
    
    def getEvent(self, results: list[int]) -> Event | None:
        for event in self.__events:
            if True == event.isThisEvent(results):
                return event
            else:
                pass

