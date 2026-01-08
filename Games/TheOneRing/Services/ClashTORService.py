from enum import Enum
from dataclasses import dataclass

from DispositionsService import DispositionsService
from ..Details.EnemyTOR import EnemyTOR
from ..Details.BandTOR import BandTOR
from ..Details.BandTOR import BandDispositionType
from ..Details.DiceTheOneRing import DiceFeatType
from ..Details.ResultTOR import ResultTOR, SuccessTORType

class StancesTOR(Enum):
    NONE = "None"
    FORWARD = "Forward"
    OPEN = "Open"
    DEFENSIVE = "Defensive"
    REARWARD = "Rearward" 

@dataclass
class ClashResultDTO():

    pass   

    
class ClashTORService:
    def __new__(cls, *args, **kwargs):
        raise TypeError(f"{cls.__name__} is a static utility class and cannot be instantiated.")
    
    @staticmethod
    def mapUsableSuccess(bandStance: StancesTOR, result: ResultTOR) -> int:
        usableSuccess: int = 1
        match bandStance:
            case StancesTOR.FORWARD | StancesTOR.OPEN:
                usableSuccess = result.specSuccNum + 1
            case StancesTOR.DEFENSIVE:
                print("Defensive stance: Ignore Special Success!")
                usableSuccess = 1
        return usableSuccess
    
    
    @staticmethod
    def onClashSucceeded(band: BandTOR, enemy: EnemyTOR, bandStance: StancesTOR, result: ResultTOR, hit: int = 0):
        usableSuccess: int = ClashTORService.mapUsableSuccess(bandStance, result)
        
        print(f"Clash {result.success.name} succeeded: Success Number {usableSuccess}")
        print(f"Enemy mighty: {enemy.getMighty()}, Resistance: {enemy.resistance}")

        if hit > usableSuccess:
            print(f"Hit {hit} exceeds usable success {usableSuccess}. Using max possible value: hit = {usableSuccess}")
            hit = usableSuccess

        enemy.addResistance(-hit)
        print(f"Enemy resistance decreased by {hit}. New resistance: {enemy.resistance}")
        print(f"Left {usableSuccess - hit} success to spend.")

    @staticmethod
    def makeRally(band: BandTOR, enemy: EnemyTOR, spentHope: int = 0, bonusSuccess: int = 0) -> ResultTOR:
        dispositionType: BandDispositionType = BandDispositionType.RALLY
        diceFeat: DiceFeatType = DiceFeatType.NORMAL

        resultRally: ResultTOR = DispositionsService.testBandV2(band, enemy, dispositionType, diceFeat, spentHope, bonusSuccess)
        return resultRally

    @staticmethod
    def onClashFailed(band: BandTOR, enemy: EnemyTOR, bandStance: StancesTOR, result: ResultTOR, spentHope: int = 0, bonusSuccess: int = 0):
        print(f"Clash {result.success.name} failed:")
        dispositionType: BandDispositionType = BandDispositionType.RALLY
        diceFeat: DiceFeatType = DiceFeatType.NORMAL

        resultRally: ResultTOR = DispositionsService.testBandV2(band, enemy, dispositionType, diceFeat, spentHope, bonusSuccess)

        match resultRally.success:
            case SuccessTORType.FAILURE | SuccessTORType.MISERABLE:
                print(f"Rally failed with result: {resultRally.success.name}")
                print(f"Band is injured more, enemy resistance is still {enemy.resistance}.")
                band.printAllies()
                allyName:str = input("Choose Ally to injure >> ")
                band.injureAlly(allyName)
            case SuccessTORType.EXTRAORDINARY | SuccessTORType.GREAT | SuccessTORType.CRITICAL | SuccessTORType.NORMAL:
                print(f"Rally succeeded with result: {resultRally.success.name}")
                print(f"Band is not injured more, but enemy resistance is still {enemy.resistance}.")

    @staticmethod
    def __getDisposition(bandStance: StancesTOR) -> BandDispositionType:

        dispositionType: BandDispositionType = BandDispositionType.NONE
        match bandStance:
            case StancesTOR.FORWARD | StancesTOR.OPEN | StancesTOR.DEFENSIVE:
                dispositionType = BandDispositionType.WAR
            case StancesTOR.REARWARD:
                dispositionType = BandDispositionType.MANOEUVRE
            case StancesTOR.NONE | _:
                raise ValueError(f"Invalid band stance: {bandStance}. Expected one of: {StancesTOR.FORWARD}, {StancesTOR.OPEN}, {StancesTOR.DEFENSIVE}, {StancesTOR.REARWARD}.")    
        return dispositionType
    
    @staticmethod
    def __getDiceFeatType(bandStance: StancesTOR) -> DiceFeatType:
        diceFeat: DiceFeatType = DiceFeatType.NORMAL
        match bandStance:
            case StancesTOR.DEFENSIVE:
                diceFeat = DiceFeatType.FAVOURED
            case StancesTOR.FORWARD:
                diceFeat = DiceFeatType.ILL
            case StancesTOR.REARWARD | StancesTOR.OPEN:
                diceFeat = DiceFeatType.NORMAL
            case StancesTOR.NONE | _:
                raise ValueError(f"Invalid band stance: {bandStance}. Expected one of: {StancesTOR.FORWARD}, {StancesTOR.OPEN}, {StancesTOR.DEFENSIVE}, {StancesTOR.REARWARD}.")
        return diceFeat
    
    @staticmethod
    def __chooseStance() -> StancesTOR:
        print("Choose band stance:")
        for stance in StancesTOR:
            print(f"{stance.name} - {stance.value}")
        
        while True:
            strStance = input("Enter band stance >> ").strip().upper()
            try:
                return StancesTOR[strStance]
            except KeyError:
                print(f"Invalid stance: {strStance}. Please choose a valid stance.")
    
    @staticmethod
    def makeClash(band: BandTOR, enemy: EnemyTOR, bandStance: StancesTOR, spentHope: int = 0, bonusSuccess: int = 0) -> ResultTOR:
        if bandStance is StancesTOR.NONE or bandStance is None:
            bandStance = ClashTORService.__chooseStance()
        else:
            pass

        dispositionType: BandDispositionType = ClashTORService.__getDisposition(bandStance)
        diceFeat: DiceFeatType = ClashTORService.__getDiceFeatType(bandStance)

        result: ResultTOR = DispositionsService.testBandV2(band, enemy, dispositionType, diceFeat, spentHope, bonusSuccess)

        return result
    
    @staticmethod
    def resolveClash(band: BandTOR, enemy: EnemyTOR, bandStance, result: ResultTOR) -> None:

        if bandStance is StancesTOR.FORWARD:
            print(f"Band is in Forward stance, enemy resistance decreased by 1.")
            enemy.addResistance(-1)

        match result.success:
            case SuccessTORType.FAILURE | SuccessTORType.MISERABLE:
                ClashTORService.onClashFailed(band, enemy, bandStance, result)
            case SuccessTORType.EXTRAORDINARY | SuccessTORType.GREAT | SuccessTORType.CRITICAL | SuccessTORType.NORMAL:
                ClashTORService.onClashSucceeded(band, enemy, bandStance, result)
        

    @staticmethod
    def makeSequence(band: BandTOR, enemy: EnemyTOR, bandStance: StancesTOR, spentHope: int = 0, bonusSuccess: int = 0) -> None:

        # ClashTORService.makeCommanderActivity()
        if bandStance is StancesTOR.NONE or bandStance is None:
            bandStance = ClashTORService.__chooseStance()
        else:
            pass
        resultClash = ClashTORService.makeClash(band, enemy, bandStance, spentHope, bonusSuccess)
        ClashTORService.resolveClash(band, enemy, bandStance, resultClash)


