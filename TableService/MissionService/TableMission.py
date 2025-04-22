from typing import List, cast
import pandas as pd
from TableService.Record import Record
from utils.singleton import singleton
from TableService.Table import Table
from TheOneRingDetails.DiceTheOneRing import Dice, DiceTheOneRing, DiceTheOneRingType

from TableService.TableLoader import TableLoader

@singleton
class TableMission(Table):
    def __init__(self, recordType: type[Record], path="data/Table.xlsx", sheetName="Missions", dices: list[Dice] = [DiceTheOneRing(DiceTheOneRingType.FEAT), DiceTheOneRing(DiceTheOneRingType.SUCCESS)]):
        super().__init__(recordType, path, sheetName, dices)