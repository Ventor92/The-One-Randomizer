from MissionRosterBand import MissionRosterBand, DispositionsType
from SheetMissionRoster import SheetMissionRoster
from TheOneRingDetails.DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType, DiceFeatType
from TheOneRingDetails.ResultTOR import ResultTOR, SuccessTORType

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
    def test(missionRosterBand: MissionRosterBand, 
             dispositions: DispositionsType, 
             featType: DiceFeatType, 
             spentHope: int = 0, 
             bonusSuccess: int = 0) -> bool:
        levelDisposition, strDisposition = DispositionsService.getLvlDispo(missionRosterBand, dispositions)
        # Twoja logika ładowania danych
        diceFeat = DiceTheOneRing(DiceTheOneRingType.FEAT)
        diceSuccess = DiceTheOneRing(DiceTheOneRingType.SUCCESS)
        targetNumber:int = missionRosterBand.getTN()
        
        match featType:
            case DiceFeatType.FAVOURED | DiceFeatType.ILL:
                featDiceNum = 2
            case _:
                featDiceNum = 1
        rollsFeat:list[int] = diceFeat.roll(featDiceNum)

        spentHope = DispositionsService.handleHope(missionRosterBand, spentHope)
        isMiserable:bool = MissionRosterBand.isMiserable(missionRosterBand)

        print(f"{strDisposition} {levelDisposition} ")

        rollsSuccess:list[int] = diceSuccess.roll(levelDisposition + spentHope + bonusSuccess)

        result = ResultTOR(rollsFeat, rollsSuccess, featType, targetNumber, isMiserable)
        
        match result.success:
            case SuccessTORType.FAILURE | SuccessTORType.MISERABLE:
                retSuccess = False
            case _:
                retSuccess = True
            
        print(result)
        return retSuccess

    @staticmethod
    def handleHope(missionRosterBand, spentHope):
        MissionRosterBand.getHope(missionRosterBand)
        if (spentHope > missionRosterBand.getHope()):
            spentHope = missionRosterBand.getHope()
        MissionRosterBand.changeHope(missionRosterBand, (-spentHope))
        
        return spentHope

    @staticmethod
    def getLvlDispo(missionRosterBand, dispositions):
        match dispositions:
            case DispositionsType.RALLY:
                levelDisposition:int = missionRosterBand.getRally()
                strDisposition = "Rally (Dzielność)"
            case DispositionsType.MANOEUVRE:
                levelDisposition:int = missionRosterBand.getManoeuvre()
                strDisposition = "Manoeuvre (Mobilność)"
            case DispositionsType.WAR:
                levelDisposition:int = missionRosterBand.getWar()
                strDisposition = "War (Bitność)"
            case DispositionsType.EXPERTISE:
                levelDisposition:int = missionRosterBand.getExpertise()
                strDisposition = "Expertise (Fachowość)"
            case DispositionsType.VIGILANCE:
                levelDisposition:int = missionRosterBand.getVigilance()
                strDisposition = "Vigilance (Ostrożność)"
            case _:
                # raise TypeError(f"{cls.__name__} Zły typ Kompenencji.")
                levelDisposition:int = 0
                strDisposition = "UNKNOWN (Nieznany)"
                pass
        return levelDisposition,strDisposition

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
    