from GameService.Game import Game
from TableService.Table import Table, Record

from TableService.MissionService.TableMission import TableMission
from TableService.EventService.TableEvent import TableEvent
from TableService.ThreadService.TableThread import TableThread

from TheOneRingDetails.EventTheOneRing import EventTheOneRing
from TheOneRingDetails.ThreadTheOneRing import ThreadTOR
from TheOneRingDetails.MissionTOR import MissionTOR
from TheOneRingDetails.DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType

from DiceService.DiceSet import DiceSet, Dice

from TheOneRingDetails.BandTOR import BandTOR, BandDispositionType, BandArmamentType, BandSizeType, BandFacultyType, BandBurdenType
from TheOneRingDetails.BandTORLoader import BandTORLoader

class GameTORService():
    def __new__(cls, *args, **kwargs):
        raise TypeError(f"{cls.__name__} is a static utility class and cannot be instantiated.")
    
    @staticmethod
    def getArmament() -> BandArmamentType:
        armament: BandArmamentType = BandArmamentType.NONE
        strNumber:str = input(f"Band Armament {BandArmamentType.LIGHT.name}({BandArmamentType.LIGHT.value}), {BandArmamentType.READY.name}({BandArmamentType.READY.value}), {BandArmamentType.HEAVY.name}({BandArmamentType.HEAVY.value}) >> ")
        try:
            armament: BandArmamentType = BandArmamentType[strNumber.upper()]
        except KeyError:
            try:
                armament: BandArmamentType = BandArmamentType(int(strNumber))
            except ValueError:
                print("Invalid armament type!")
    
        return armament
    
    @staticmethod
    def getFaculty() -> BandFacultyType:
        faculty: BandFacultyType = BandFacultyType.NONE
        strNumber:str = input(f"Band Faculty {BandFacultyType.WAR.name}({BandFacultyType.WAR.value}), {BandFacultyType.EXPERTISE.name}({BandFacultyType.EXPERTISE.value}), {BandFacultyType.VIGILANCE.name}({BandFacultyType.VIGILANCE.value}) >> ")
        try:
            faculty: BandFacultyType = BandFacultyType[strNumber.upper()]
        except KeyError:
            try:
                faculty: BandFacultyType = BandFacultyType(int(strNumber))
            except ValueError:
                print("Invalid armament type!")
    
        return faculty
    
    @staticmethod
    def getHuntThreshold() -> int:
        huntThreshold: int = 0
        strNumber:str = input("Band Hunt Threshold >>")
        try:
            huntThreshold: int = int(strNumber)
        except KeyError:
            print("Invalid huntThreshold value. Please choose integer.")
        
        return huntThreshold

