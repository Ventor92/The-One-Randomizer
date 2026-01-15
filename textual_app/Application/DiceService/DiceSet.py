import random

from Application.DiceService.Dice import Dice, DiceType

# class DiceSetFactory():
#     _creators = {}

#     @classmethod
#     def register(cls, classId: int, creator_func):
#         cls._creators[classId] = creator_func

#     @classmethod
#     def create(cls, classId: int, row: Series) -> Event:
#         if classId not in cls._creators:
#             raise ValueError(f"Unknown class id: {classId}")
#         return cls._creators[eventClassId](row)


class DiceSet():
    def __init__(self, dices: list[Dice] = [Dice(DiceType.D12), Dice(DiceType.D6)]):
        self.__dices: list[Dice] = dices

    def getDiceSet(self) -> list[Dice]:
        return self.__dices
    
    def roll(self) -> list[int]:
        results: list[int] = []
        for dice in self.__dices:
            result: int = dice.roll(numDice=1)[0]
            results.append(result)
        return results
    
