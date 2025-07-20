import random
from typing import List

from enum import Enum

class DiceType(Enum):
    D2 = "D2"
    D3 = "D3"
    D4 = "D4"
    D6 = "D6"
    D8 = "D8"
    D10 = "D10"
    D12 = "D12"
    D20 = "D20"
    D100 = "D100"

class Dice:
    def __init__(self, diceType=DiceType.D6):
        self.__diceType = diceType
        self.__lastRoll = [0]

    def _roll(self, numDice: int) -> List[int]:
        roll = [random.randint(1, self.__diceType.value) for _ in range(numDice)]
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