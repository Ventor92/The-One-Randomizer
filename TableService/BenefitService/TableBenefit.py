import pandas as pd
from TableService.EventService.Event import Event
from utils.singleton import SingletonMeta
from DiceService.Dice import Dice
from DiceService.DiceSet import DiceSet
from TheOneRingDetails.DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType
from TableService.TableLoader import TableLoader
from TableService.Table import Table, Record

from TheOneRingDetails.BenefitTOR import BenefitTOR


class TableBenefit(Table, metaclass=SingletonMeta):
    def __init__(self, path="data/Table.xlsx", sheetName="Benefits"):
        self.diceSet = DiceSet([DiceTheOneRing(DiceTheOneRingType.SUCCESS), DiceTheOneRing(DiceTheOneRingType.SUCCESS)])
        super().__init__(BenefitTOR, path, sheetName, self.diceSet.getDiceSet())
