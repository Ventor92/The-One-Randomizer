from dataclasses import dataclass
from TableService.EventService.Event import Event

import pandas as pd
from pandas import Series

@dataclass
class EventTheOneRing(Event):
    featDieMin: int                  # KOŚĆ DZIAŁANIA
    featDieMax: int                  # KOŚĆ DZIAŁANIA
    event: str                      # ZDARZENIE
    testConsequences: str          # KONSEKWENCJE TESTU
    fatigueGained: int             # OTRZYMANE ZNUŻENIE
    successDie: int                # KOŚĆ SUKCESU
    detailedEvent: str             # ZDARZENIE SZCZEGÓŁOWE
    outcome: str                   # SKUTEK

    @classmethod
    def fromRow(cls, row: Series):
        return cls(
            id = "eventTheOneRingId",
            description = "The One Ring",
            featDieMin=int(row['featDieMin']),
            featDieMax=int(row['featDieMax']),
            event=row['event'],
            testConsequences=row['testConsequences'],
            fatigueGained=int(row['fatigueGained']),
            successDie=int(row['successDie']),
            detailedEvent=row['detailedEvent'],
            outcome=row['outcome']
        )

    def __str__(self):
        return (
            f"Event: {self.event} || Detailed: {self.detailedEvent}\n"
            f"  Test Consequences: {self.testConsequences}\n"
            f"  Outcome: {self.outcome} || Fatigue Gained: {self.fatigueGained}\n"
            f"  Feat Die: ({self.featDieMin}-{self.featDieMax}) Success Die: {self.successDie}\n"
            f"  Def Desc: {self.description}\n"
        )
    
    def isThisRecord(self, results: list[int]) -> bool:
        return self.isThisEvent(results)
    
    def isThisEvent(self, results: list[int]):

        dieFeatValue: int = results[0]
        dieResultSuccess: int = results[1]
        
        try:
            if not (1 <= dieFeatValue <= 12):
                raise ValueError("dieFeatValue not in rage <1:12>")
        except ValueError:
            print("Error, default dieFeatValue 1!")
            dieFeatValue = 1

        try:
            if not (1 <= dieResultSuccess <= 6):
                raise ValueError("dieResultSuccess not in rage <1:6>")
        except ValueError:
            print("Error, default dieResultSuccess 1!")
            dieFeatValue = 1

        if self.featDieMin <= dieFeatValue <= self.featDieMax and self.successDie == dieResultSuccess:
            return True
        else:
            return False

