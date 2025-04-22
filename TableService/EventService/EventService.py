from TableService.EventService.TableEvent import TableEvent, Event
from TheOneRingDetails.DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType, Dice

from utils.singleton import singleton

@singleton
class EventService():
    def __init__(self, tableEvent: TableEvent, dices: list[Dice] = [DiceTheOneRing(DiceTheOneRingType.FEAT), DiceTheOneRing(DiceTheOneRingType.SUCCESS)]):
        self.__tableEvent = tableEvent
        self.__dices = dices

    def __getEvent(self, rollResults: list[int]) -> Event | None:
        event: Event | None = self.__tableEvent.getEvent(rollResults)
        return event
    
    def __rollEventDices(self) -> list[int]:
        rollResults: list[int] = []
        for dice in self.__dices:
            result = dice.roll(1)[0]
            rollResults.append(result)
        return rollResults
    
    def getEvent(self, valueFeat: int, valueSuccess: int) -> Event | None:
        event: Event | None = self.__getEvent([valueFeat, valueSuccess])
        print(event)
        return event
    
    def rollEvent(self) -> Event | None:
        event: Event | None = self.__tableEvent.rollEvent()
        print(event)
        return event


        