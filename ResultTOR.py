from dataclasses import dataclass
from enum import Enum
from DiceSet import DiceSet
from DiceTheOneRing import DiceFeatType

class SuccessTORType(Enum):
    NORMAL = 0
    GREAT = 1
    EXTRAORDINARY = 2
    CRITICAL = 3
    FAILURE = 4
    
@dataclass
class ResultTOR:
    """
    A class to represent the result of a TOR (The One Ring) dice roll result.
    """
    resultsSuccess: list[int]
    resultsFeat: list[int]
    valueFeat: int
    valueSuccess: int
    valueTotal: int
    specSuccNum: int
    targetNumber: int = 20
    diceFeat: DiceFeatType = DiceFeatType.NORMAL
    success: SuccessTORType = SuccessTORType.FAILURE

    def __init__(self, resultsFeat: list[int], resultsSuccess: list[int], diceFeat: DiceFeatType, targetNumber: int = 20):
        self.resultsSuccess = resultsSuccess
        self.resultsFeat = resultsFeat
        self.diceFeat = diceFeat

        resultFeatTemp: list[int] = [0 if value == 11 else value for value in resultsFeat]
        match diceFeat:
            case DiceFeatType.NORMAL:
                self.valueFeat = resultsFeat[0]
                self.resultsFeat = [resultsFeat[0]]
            case DiceFeatType.FAVOURED:
                self.valueFeat = max(resultFeatTemp)
            case DiceFeatType.ILL | _:
                self.valueFeat = min(resultFeatTemp)

        self.valueSuccess = sum(resultsSuccess)
        self.valueTotal = self.valueFeat + self.valueSuccess
        self.specSuccNum = resultsSuccess.count(6)
        self.targetNumber = targetNumber
        if (self.valueTotal >= self.targetNumber) or (self.valueFeat == 12):
            specSuccNum = min(self.specSuccNum, SuccessTORType.EXTRAORDINARY.value)
            self.success = SuccessTORType(specSuccNum)
        else:
            self.success = SuccessTORType.FAILURE

    def __str__(self):
        result_str = (
            f"ResultRollTOR:\n"
            f"  Result of Feat:{self.diceFeat.name} -> {self.success.name} "
        )
        if self.success != SuccessTORType.FAILURE:
            result_str += f"SUCCESS τ:{self.specSuccNum}\n"
        else:
            result_str += f"\n"
        result_str += (
            f"  Details:\n"
            f"    TN: {self.targetNumber} vs Total: {self.valueTotal} + τ:{self.specSuccNum}\n"
            f"    Feat: {self.resultsFeat}->{self.valueFeat} Success: {self.resultsSuccess}->{self.valueSuccess}\n"
        )
        return result_str

