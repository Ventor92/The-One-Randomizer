from dataclasses import dataclass

import pandas as pd
from pandas import Series

from TableService.Record import Record
from .SkillTOR import SkillTypeTOR

@dataclass
class BenefitTOR(Record):
    dieSuccess1: int = 0  # KOŚĆ SUKCESU 1
    dieSuccess2Min: int = 0 # KOŚĆ SUKCESU 2 MIN
    dieSuccess2Max: int = 0 # KOŚĆ SUKCESU 2 MAX
    benefit: SkillTypeTOR = SkillTypeTOR.NONE  # SKILL

    @classmethod
    def fromRow(cls, row: Series):
        return cls(
            id = "BenefitTORId",
            dieSuccess1=int(row['dieSuccess1']),
            dieSuccess2Min=int(row['dieSuccess2Min']),
            dieSuccess2Max=int(row['dieSuccess2Max']),
            
            benefit=SkillTypeTOR[row['benefit']] if row['benefit'] in SkillTypeTOR.__members__ else SkillTypeTOR.NONE,
        )
    
    def __str__(self):
        return (
            f"Benefit: {self.benefit.name} || "
            f"Die Success 1: {self.dieSuccess1} || "
            f"Die Success 2: ({self.dieSuccess2Min}-{self.dieSuccess2Max})\n"
            f"Record ID: {self.id}\n"
        )
    
    def isThisRecord(self, results: list[int]) -> bool:
        return self.isThisBenefit(results)
    
    def isThisBenefit(self, results: list[int]) -> bool:
        dieSuccess1: int = results[0]
        dieSuccess2: int = results[1]

        if not (1 <= dieSuccess1 <= 6):
            raise ValueError("dieSuccess1 not in range <1:6>")
        
        if not (1 <= dieSuccess2 <= 6):
            raise ValueError("dieSuccess2 not in range <1:6>")

        if (dieSuccess1 == self.dieSuccess1) & (self.dieSuccess2Min <= dieSuccess2 <= self.dieSuccess2Max):
            return True
        else:
            return False

