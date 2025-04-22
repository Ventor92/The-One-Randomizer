from Game import Game
from TableService.Table import Table, Record

from TableService.MissionService.TableMission import TableMission
from TableService.EventService.TableEvent import TableEvent
from TableService.ThreadService.TableThread import TableThread

from TheOneRingDetails.EventTheOneRing import EventTheOneRing
from TheOneRingDetails.ThreadTheOneRing import ThreadTOR
from TheOneRingDetails.MissionTOR import MissionTOR
from TheOneRingDetails.DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType

from DiceService.DiceSet import DiceSet, Dice

from utils.singleton import singleton

@singleton
class GameTOR(Game):
    def __init__(self, title: str = "The One Ring"):
        dices: list[Dice] = [DiceTheOneRing(DiceTheOneRingType.FEAT), DiceTheOneRing(DiceTheOneRingType.SUCCESS)]
        diceSet = DiceSet(dices) 

        # tableEvent = TableEvent(id(EventTheOneRing)),
        # tableThread = TableEvent(id(ThreadTOR)),
        # tableMission = TableEvent(id(MissionTOR)),

        tableEvent = TableEvent(id(EventTheOneRing), dices = dices)

        tables: list[Table] = [
            tableEvent,
            # Table(EventTheOneRing, diceSet),
            TableThread(id(ThreadTOR)),
            TableMission(id(MissionTOR)),
        ]

        super().__init__(title, tables)
  
    def getEvent(self, results: list[int]) -> EventTheOneRing:
        table = self._getTable(TableEvent)
        record = table.getRecord(results)
        if isinstance(record, EventTheOneRing):
            return record
        else:
            raise ValueError(f"Record is not of type EventTheOneRing: {record}")

