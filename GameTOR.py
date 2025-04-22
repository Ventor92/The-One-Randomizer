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

        tables: list[Table] = [
            TableEvent(id(EventTheOneRing)),
            # Table(EventTheOneRing, diceSet),
            TableThread(id(ThreadTOR)),
            TableMission(id(MissionTOR)),
        ]

        super().__init__(title, tables)

    def _getTable(self, tableType: type[Table] = TableEvent) -> Table:
        for table in self.tables:
            if isinstance(table, tableType):  # Compare with the class of the singleton
                return table
        raise ValueError(f"Table of type {tableType} not found in game {self.title}.")
    
    def getEvent(self, results: list[int]) -> EventTheOneRing:
        table = self._getTable(TableEvent)
        record = table.getRecord(results)
        if isinstance(record, EventTheOneRing):
            return record
        else:
            raise ValueError(f"Record is not of type EventTheOneRing: {record}")
    
        
    def getRecord(self, tableType: type[Table], results: list[int]) -> Record:
        table = self._getTable(tableType)
        record =  table.getRecord(results)
        if isinstance(record, Record):
            return record
        else:
            raise ValueError(f"Record is not of type {tableType}: {record}")
        
    def rollRecord(self, tableType: type[Table]) -> Record:
        table = self._getTable(tableType)
        results = table.roll()
        record = self.getRecord(tableType, results)
        print(record)
        return record
