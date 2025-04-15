from TableEvent import TableEvent, Event
from DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType, Dice

from utils.singleton import singleton

@singleton
class EventService():
    def __init__(self, tableEvent: TableEvent, dices: list[Dice] = [DiceTheOneRing(DiceTheOneRingType.FEAT), DiceTheOneRing(DiceTheOneRingType.SUCCESS)]):
        self.__tableEvent = tableEvent
        self.__dices = dices

    def __getEvent(self, rollResults: list[int]) -> Event:
        event: Event = self.__tableEvent.getEvent(rollResults[0], rollResults[1])
        return event
    
    def __rollDices(self) -> list[int]:
        rollResults: list[int] = []
        for dice in self.__dices:
            result = dice.roll(1)[0]
            rollResults.append(result)
        return rollResults
    
    def getEvent(self, valueFeat: int, valueSuccess: int) -> Event:
        event: Event = self.__getEvent([valueFeat, valueSuccess])
        print(event)
        return event
    
    def rollEvent(self) -> Event:
        rollResults: list[int] = self.__rollDices()
        event: Event = self.__getEvent(rollResults)
        print(event)
        return event


        