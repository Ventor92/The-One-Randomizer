from dataclasses import dataclass
from TableService.Record import Record
from pandas import Series

@dataclass
class MissionTOR(Record):
    dieFeat: int
    dieSuccessRangeMin: int
    dieSuccessRangeMax: int
    mission: str

    def __str__(self):  
        return (
            f"{self.id} Mission :\n"
            f"  Feat Die: {self.dieFeat} Success Die: {self.dieSuccessRangeMin}-{self.dieSuccessRangeMax}\n"
            f"  Mission: {self.mission}\n"
        )
    
    @classmethod
    def fromRow(cls, row: Series):
        return cls(
            id = "The One Ring",
            dieFeat=int(row["dieFeat"]),
            dieSuccessRangeMin=int(row["dieSuccessRangeMin"]),
            dieSuccessRangeMax=int(row["dieSuccessRangeMax"]),
            mission=str(row["mission"]),
        )
    
    def isThisRecord(self, results: list[int]) -> bool:
        return self.isThisMission(results)
    
    def isThisMission(self, results: list[int]):

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

        if self.dieSuccessRangeMin <= dieResultSuccess <= self.dieSuccessRangeMax and self.dieFeat == dieFeatValue:
            return True
        else:
            return False
        
    def toRawDict(self) -> dict:
        return {
            "dieFeat": self.dieFeat,
            "dieSuccessRangeMin": self.dieSuccessRangeMin,
            "dieSuccessRangeMax": self.dieSuccessRangeMax,
            "mission": self.mission
        }