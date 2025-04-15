from MissionRosterBand import MissionRosterBand, DispositionsType
from SheetMissionRoster import SheetMissionRoster
from DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType, DiceFeatType

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
    def test(missionRosterBand: MissionRosterBand, dispositions: DispositionsType, featType: DiceFeatType):

        match dispositions:
            case DispositionsType.RALLY:
                levelDisposition:int = missionRosterBand.getRally()
                strDisposition = "Rally (Dzielność)"
            case _:
                # raise TypeError(f"{cls.__name__} Zły typ Kompenencji.")
                pass
        # Twoja logika ładowania danych
        print(f"{strDisposition} {levelDisposition}")
        diceFeat = DiceTheOneRing(DiceTheOneRingType.FEAT)
        diceSuccess = DiceTheOneRing(DiceTheOneRingType.SUCCESS)
        targetNumber:int = missionRosterBand.getTN()

        if featType == (DiceFeatType.FAVOURED or DiceFeatType.ILL):
            featDiceNum = 2
        else:
            featDiceNum = 1

        rollsFeat:list[int] = diceFeat.roll(featDiceNum)
        rollsFeatTemp = [0 if x == 11 else x for x in rollsFeat]
        if featType == DiceFeatType.FAVOURED:
            feat:int = max(rollsFeatTemp)
        elif featType == DiceFeatType.ILL:
            feat:int = min(rollsFeatTemp)
        else: 
            feat:int = rollsFeat[0]

        rollsSuccess:list[int] = diceSuccess.roll(levelDisposition)

        successSum:int = sum(rollsSuccess)

        count = rollsSuccess.count(6)
        if ((successSum + feat) >= targetNumber) or (feat == 12):
            strResult = f"SUCCESS in {strDisposition}! Quality: ({count})"
        else:
            strResult = f"FAIL in {strDisposition}!"
            
        print(f"Result: {strResult} || TN:{targetNumber} vs Total:{successSum + feat}")
        print(f"Details: Feat:{rollsFeat}->{feat} Success:{rollsSuccess}->{successSum}")
        pass

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
    