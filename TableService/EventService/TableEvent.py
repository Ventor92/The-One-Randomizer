import pandas as pd
from TableService.EventService.Event import Event
from utils.singleton import SingletonMeta
from DiceService.Dice import Dice
from DiceService.DiceSet import DiceSet
from TheOneRingDetails.DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType
from TableService.TableLoader import TableLoader
from TableService.Table import Table, Record


class TableEvent(Table, metaclass=SingletonMeta):
    def __init__(self, recordType: type[Record], diceSet: DiceSet, path="data/Table.xlsx", sheetName="Zdarzenia"):
        super().__init__(recordType, path, sheetName, diceSet.getDiceSet())

