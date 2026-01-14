from enum import Enum, auto
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Literal, Union, Annotated, Optional

from pydantic import BaseModel

from web_app.backend.models.chatRecord import RecordBase
from DiceService.Dice import Dice, DiceType, DiceResults
from TableService.Record import Record
from TableService.TableLoader import TableLoaderV2

from Games.TheOneRing.Details.EventTheOneRing import EventTheOneRing

class RecordTableType(Enum):
    UNKNOWN = auto()
    TOR = auto()

class TableType(Enum):
    UNKNOWN = auto()
    EVENT = auto()
    THREAD = auto()
    MISSION = auto()

class RecordTable_DTO(BaseModel):
    def __init__(self, recordType: RecordTableType = RecordTableType.UNKNOWN, dices: list[Dice] = [], 
                 description: str = "Meaning less description", note: str = "User note"):
        self.recordType: RecordTableType = recordType
        self.dices: list[Dice] = dices
        self.description: str = description
        self.note: str = note

class Table():
    def __init__(self, diceTypes: list[DiceType], description: str):
        self.dices: list[Dice] = []
        self.description: str = description

        for diceType in diceTypes:
            dice = Dice(diceType)
            self.dices.append(dice)

        self._records: list[Record] = []
        self._setRecords()

        self._recordType: Optional[type[Record]] = None 

    def getRecordType(self) -> Optional[type[Record]]: 
        return self._recordType
    
    def _setRecordType(self, recordType: type[Record]):
        self._recordType = recordType

    def roll(self) -> DiceResults:
        rollResults: DiceResults = {}
        for dice in self.dices:
            result = dice.roll(1)
            type = dice.getType()
            rollResults[type] = result.copy()

        return rollResults
    
    @staticmethod
    def _convertDiceResults2FlatList(diceResult: DiceResults) -> list[int]:
        diceResultList: list[int] = []
        try: 
            diceResultList.append(diceResult[DiceType.D12][0])
            diceResultList.append(diceResult[DiceType.D6][0])
        except:
            diceResultList: list[int] = [11,1]

        return diceResultList
        
    def getRecord(self, results: DiceResults) -> Optional[Record]:
        results_: list[int] = self._convertDiceResults2FlatList(results)

        recordOutput: Optional[Record] = None
        for record in self._records:
                isIt = record.isThisRecord(results_)
                if isIt is True:
                    recordOutput = record
                    break
                else:
                    recordOutput = None

        return recordOutput

    def rollRecord(self) -> Optional[Record]:
        results = self.roll()
        record: Optional[Record] = self.getRecord(results)

        return record

    @abstractmethod
    def loadRecords(self) -> list[Record]:
        ...

    def _setRecords(self):
        self._records = self.loadRecords()
    
    # def _loadRecords(self, loader: TableLoaderV2) -> list[Record]:
    #     return loader.loadRecords()

class RandomTable(Table):
    def __init__(self, loader: TableLoaderV2, diceTypes: list[DiceType], description: str):
        self.loader = loader
        super().__init__(diceTypes, description)
                         
        self._setRecordType(loader.getRecordType())

    def loadRecords(self) -> list[Record]:
        return self.loader.loadRecords()


