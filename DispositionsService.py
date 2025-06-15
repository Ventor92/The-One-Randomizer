from TheOneRingDetails.DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType, DiceFeatType
from TheOneRingDetails.ResultTOR import ResultTOR, SuccessTORType

from TheOneRingDetails.BandTOR import BandTOR, BandDispositionType
from TheOneRingDetails.EnemyTOR import EnemyTOR

class DispositionsService:
    def __new__(cls, *args, **kwargs):
        raise TypeError(f"{cls.__name__} is a static utility class and cannot be instantiated.")

    @staticmethod
    def handleHope(band: BandTOR, spentHope):
        band.getHope()
        if (spentHope > band.getHope()):
            spentHope = band.getHope()
        band.changeHope((-spentHope))
        
        return spentHope
    
    @staticmethod
    def str2DispositionType(str1) -> BandDispositionType:
        type: BandDispositionType = BandDispositionType.NONE
        match str1:
            case BandDispositionType.RALLY.name:
                type:BandDispositionType = BandDispositionType.RALLY
            case BandDispositionType.MANOEUVRE.name:
                type:BandDispositionType = BandDispositionType.MANOEUVRE
            case BandDispositionType.EXPERTISE.name:
                type:BandDispositionType = BandDispositionType.EXPERTISE
            case BandDispositionType.VIGILANCE.name:
                type:BandDispositionType = BandDispositionType.VIGILANCE
            case BandDispositionType.WAR.name:
                type:BandDispositionType = BandDispositionType.WAR
            case _:
                type:BandDispositionType = BandDispositionType.NONE
        return type

    @staticmethod
    def str2DiceFeatType(str2):
        diceFeat: DiceFeatType = DiceFeatType.NORMAL
        match str2:
            case DiceFeatType.FAVOURED.name:
                diceFeat = DiceFeatType.FAVOURED
            case DiceFeatType.ILL.name:
                diceFeat = DiceFeatType.ILL
            case DiceFeatType.NORMAL.name | _:
                diceFeat = DiceFeatType.NORMAL
        return diceFeat
    
    @staticmethod
    def testBand(band: BandTOR,
            enemy: EnemyTOR,
            dispositions: BandDispositionType, 
            featType: DiceFeatType, 
            spentHope: int = 0, 
            bonusSuccess: int = 0) -> bool:
        levelDisposition = band.getDispositionLevel(dispositions)

        diceFeat = DiceTheOneRing(DiceTheOneRingType.FEAT)
        diceSuccess = DiceTheOneRing(DiceTheOneRingType.SUCCESS)
        targetNumber:int = band.getTargetNumber()
        enemyMighty:int = enemy.getMighty()
        
        match featType:
            case DiceFeatType.FAVOURED | DiceFeatType.ILL:
                featDiceNum = 2
            case _:
                featDiceNum = 1
        rollsFeat:list[int] = diceFeat.roll(featDiceNum)

        spentHope = DispositionsService.handleHope(band, spentHope)
        isMiserable:bool = band.isMiserable()

        # print(f"{strDisposition} {levelDisposition} ")

        rollsSuccess:list[int] = diceSuccess.roll(levelDisposition + spentHope + bonusSuccess)

        result = ResultTOR(rollsFeat, rollsSuccess, featType, targetNumber, isMiserable, enemyMighty)
        
        match result.success:
            case SuccessTORType.FAILURE | SuccessTORType.MISERABLE:
                retSuccess = False
            case _:
                retSuccess = True
            
        print(result)
        return retSuccess
    