from MissionRosterBand import MissionRosterBand, DispositionsType
from SheetMissionRoster import SheetMissionRoster
from DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType, DiceFeatType
from ResultTOR import ResultTOR, SuccessTORType

class DispositionsService:
    def __new__(cls, *args, **kwargs):
        raise TypeError(f"{cls.__name__} is a static utility class and cannot be instantiated.")

    # @staticmethod
    # def init():
    #     if (sheetMissionRoster == None):
    #         sheetMissionRoster = SheetMissionRoster()
    #     else:
    #         pass
    #     pass 
    
    @staticmethod
    def test(missionRosterBand: MissionRosterBand, dispositions: DispositionsType, featType: DiceFeatType) -> bool:

        match dispositions:
            case DispositionsType.RALLY:
                levelDisposition:int = missionRosterBand.getRally()
                strDisposition = "Rally (Dzielność)"
            case _:
                # raise TypeError(f"{cls.__name__} Zły typ Kompenencji.")
                levelDisposition:int = 0
                strDisposition = "UNKNOWN (Nieznany)"
                pass
        # Twoja logika ładowania danych
        print(f"{strDisposition} {levelDisposition}")
        diceFeat = DiceTheOneRing(DiceTheOneRingType.FEAT)
        diceSuccess = DiceTheOneRing(DiceTheOneRingType.SUCCESS)
        targetNumber:int = missionRosterBand.getTN()
        
        if (featType == DiceFeatType.FAVOURED) or (featType ==  DiceFeatType.ILL):
            featDiceNum = 2
        else:
            featDiceNum = 1
        
        rollsFeat:list[int] = diceFeat.roll(featDiceNum)
        rollsSuccess:list[int] = diceSuccess.roll(levelDisposition)

        result = ResultTOR(rollsFeat, rollsSuccess, featType, targetNumber)
        
        if result.success != SuccessTORType.FAILURE:
            retSuccess = True
        else:
            retSuccess = False
            
        print(result)
        return retSuccess

    @staticmethod
    def chooseMissionRoster(sheetMissionRoster: SheetMissionRoster):
        list = sheetMissionRoster.getMissionRosters()
        print(list)
        strNumber:str = input("Wybierz MissionRoster >> ")
        number:int = int(strNumber)
        actualMissionRosterBand = list[number]
        print("Your choose:")
        print(actualMissionRosterBand)
        return actualMissionRosterBand
    