from typing import List, cast
import pandas as pd
from TableService.ThreadService.Thread import Thread  # zakładam, że masz klasę Thread w osobnym pliku
from utils.singleton import SingletonMeta
from TableService.Table import Table
from TableService.Record import Record
from DiceService.DiceSet import DiceSet

from TableService.TableLoader import TableLoader

from Games.TheOneRing.Details.DiceTheOneRing import Dice, DiceTheOneRing, DiceTheOneRingType

class TableThread(Table, metaclass=SingletonMeta):
    def __init__(self, recordType: type[Record], path="data/Table.xlsx", sheetName="Wątki", dices: list[Dice] = [DiceTheOneRing(DiceTheOneRingType.FEAT), DiceTheOneRing(DiceTheOneRingType.SUCCESS)]):
        super().__init__(recordType, path, sheetName, dices)