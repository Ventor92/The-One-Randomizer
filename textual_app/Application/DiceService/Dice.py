import random
from typing import List
from dataclasses import dataclass

from enum import Enum

class DiceType(Enum):
    D2 = 2
    D3 = 3
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20
    D100 = 100

@dataclass
class RollResult():
    diceType: DiceType
    result: int

DiceResults = dict[DiceType, list[int]]

class Dice:
    def __init__(self, diceType=DiceType.D6, numDice: int = 1):
        self.__diceType = diceType
        self.__numDice = numDice
        self.__lastRoll = [0]

    def __random(self) -> int:
        return random.randint(1, self.__diceType.value)

    def _roll(self, numReroll: int) -> List[int]:

        roll = [sum([self.__random() for _ in range(self.__numDice)]) for _ in range(numReroll)]
        roll.sort()
        self.__lastRoll = roll
        return roll
    
    def getLastRoll(self) -> List[int]:
        return self.__lastRoll
    
    def getType(self) -> DiceType:
        return self.__diceType
    
    def roll(self, numDice: int) -> List[int]:
        roll:List[int] = self._roll(numDice)
        return roll
    
    @classmethod
    def fromString(cls, dieStr: str) -> 'Dice':
        dieStr = dieStr.upper().strip()
        if dieStr.startswith("D"):
            try:
                sides = int(dieStr[1:])
                diceType = DiceType(sides)
                numDice = 1
                return cls(diceType, numDice)
            except (ValueError, KeyError):
                raise ValueError(f"Invalid die string: {dieStr}")
        elif "D" in dieStr:
            try:
                parts = dieStr.split("D")
                numDice = int(parts[0]) if parts[0] else 1
                sides = int(parts[1])
                diceType = DiceType(sides)
                return cls(diceType, numDice)
            except (ValueError, KeyError):
                raise ValueError(f"Invalid die string: {dieStr}")
        else:
            raise ValueError(f"Invalid die string: {dieStr}")
    