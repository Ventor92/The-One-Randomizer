from enum import Enum
from DiceService.Dice import Dice, DiceType

class DiceTheOneRingType(Enum):
    FEAT = DiceType.D12
    SUCCESS = DiceType.D6

class DiceFeatType(Enum):
    NORMAL = 1
    ILL = 2
    FAVOURED = 3

class DiceTheOneRing(Dice):
    def __init__(self, type: DiceTheOneRingType):
        super().__init__(type.value)  # wywołujemy konstruktor klasy bazowej

    @staticmethod
    def log(type: DiceTheOneRingType, roll: int):
        if type == DiceTheOneRingType.SUCCESS and roll == 6:
            string:str =  " — Elfi Znak τ!"
        elif type == DiceTheOneRingType.FEAT and roll == 11:
            string:str =  " — Oko Saurona!"
        elif type == DiceTheOneRingType.FEAT and roll == 12:
            string:str =  " — Runa Gandalfa!"
        else:
            string:str =  ""

        print(f"Typ: {type.name} Wynik: {roll}{string}")

    def roll(self, numDice = 1):
        rolls = self._roll(numDice)
        for roll in rolls:
            nativeType = self.getType()
            type:DiceTheOneRingType = DiceTheOneRingType(nativeType)
            self.log(type, roll)

        return rolls