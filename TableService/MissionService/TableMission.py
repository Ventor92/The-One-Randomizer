from typing import List, cast
import pandas as pd
from TableService.Record import Record
from utils.singleton import SingletonMeta
from TableService.Table import Table

from Games.TheOneRing.Details.DiceTheOneRing import Dice, DiceTheOneRing, DiceTheOneRingType

from TableService.TableLoader import TableLoader

class TableMission(Table, metaclass=SingletonMeta):
    def __init__(self, recordType: type[Record], path="data/Table.xlsx", sheetName="Missions", dices: list[Dice] = [DiceTheOneRing(DiceTheOneRingType.FEAT), DiceTheOneRing(DiceTheOneRingType.SUCCESS)]):
        super().__init__(recordType, path, sheetName, dices)