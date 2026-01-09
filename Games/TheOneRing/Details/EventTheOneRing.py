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
        resultFeat: int = results[0]
        resultSuccess: int = results[1]
        isIt: bool = self.isThisEvent(resultFeat, resultSuccess)
        return isIt
    
    def isThisEvent(self, resultFeat: int, resultSuccess: int):
        
        try:
            if not (1 <= resultFeat <= 12):
                raise ValueError("dieFeatValue not in rage <1:12>")
        except ValueError:
            print("Error, default dieFeatValue 11!")
            resultFeat = 11

        try:
            if not (1 <= resultSuccess <= 6):
                raise ValueError("dieResultSuccess not in rage <1:6>")
        except ValueError:
            print("Error, default dieResultSuccess 1!")
            resultSuccess = 1

        if self.featDieMin <= resultFeat <= self.featDieMax and self.successDie == resultSuccess:
            return True
        else:
            return False

    def toRawDict(self) -> dict:
        return {
            "featDieMin": self.featDieMin,
            "featDieMax": self.featDieMax,
            "event": self.event,
            "testConsequences": self.testConsequences,
            "fatigueGained": self.fatigueGained,
            "successDie": self.successDie,
            "detailedEvent": self.detailedEvent,
            "outcome": self.outcome
        }