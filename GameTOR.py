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

        tableEvent = TableEvent(EventTheOneRing, diceSet = diceSet, path="data/Table.xlsx", sheetName="Zdarzenia")
        tableThread = TableThread(ThreadTOR, path="data/Table.xlsx", sheetName="Wątki", dices = diceSet.getDiceSet())
        tableMission = TableMission(MissionTOR, path="data/Table.xlsx", sheetName="Missions", dices = diceSet.getDiceSet())

        tables: list[Table] = [
            tableEvent,
            tableMission,
            tableThread
        ]

        super().__init__(title, tables)
  
    def getEvent(self, results: list[int]) -> EventTheOneRing:
        table = self._getTable(TableEvent)
        record = table.getRecord(results)
        if isinstance(record, EventTheOneRing):
            return record
        else:
            raise ValueError(f"Record is not of type EventTheOneRing: {record}")

