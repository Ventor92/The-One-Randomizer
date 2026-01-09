from dataclasses import dataclass

import pandas as pd
from pandas import Series
from TableService.ThreadService.Thread import Thread

@dataclass
class ThreadTOR(Thread):
    dieFeat: int       # wynik z kości działania
    dieSuccess: int    # wynik z kości sukcesu
    action: str        # działanie, które wykonuje postać
    aspect: str        # aspekt sytuacji lub sceny
    subject: str       # podmiot zdarzenia
    motive: str        # motyw lub cel działania

    @classmethod
    def fromRow(cls, row: Series):
        return cls(
            id = "threadId",
            description = "ThreadDscrptn",
            dieFeat=int(row["dieFeat"]),
            dieSuccess=int(row["dieSuccess"]),
            action=str(row["action"]),
            aspect=str(row["aspect"]),
            subject=str(row["subject"]),
            motive=str(row["motive"])
        )

    def __str__(self):
        return (
            f"Thread:\n"
            f"  Feat Die: {self.dieFeat} Success Die: {self.dieSuccess}\n"
            f"  Action: {self.action} Aspect: {self.aspect} Subject: {self.subject} Motive: {self.motive}"
        )
    
    def isThisRecord(self, results: list[int]) -> bool:
        return self.isThisThread(results)
    
    def isThisThread(self, results: list[int]):

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

        if self.dieFeat == dieFeatValue and self.dieSuccess == dieResultSuccess:
            return True
        else:
            return False
        

    def toRawDict(self) -> dict:
        return {
            "dieFeat": self.dieFeat,
            "dieSuccess": self.dieSuccess,
            "action": self.action,
            "aspect": self.aspect,
            "subject": self.subject,
            "motive": self.motive
        }
        


