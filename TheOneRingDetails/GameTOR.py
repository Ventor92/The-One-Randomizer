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

from TheOneRingDetails.GameTORService import GameTORService

from utils.singleton import singleton

@singleton
class GameTOR(Game):
    def __init__(self, title: str = "The One Ring"):
        dices: list[Dice] = [DiceTheOneRing(DiceTheOneRingType.FEAT), DiceTheOneRing(DiceTheOneRingType.SUCCESS)]
        diceSet = DiceSet(dices) 

        tableEvent = TableEvent(EventTheOneRing, diceSet = diceSet, path="data/Table.xlsx", sheetName="Zdarzenia")
        tableThread = TableThread(ThreadTOR, path="data/Table.xlsx", sheetName="Wątki", dices = diceSet.getDiceSet())
        tableMission = TableMission(MissionTOR, path="data/Table.xlsx", sheetName="Missions", dices = diceSet.getDiceSet())

        tables: list[Table] = [
            tableEvent,
            tableMission,
            tableThread
        ]
        print("GameTOR __init__")
        self.band: BandTOR
        self.loadBand()

        super().__init__(title, tables)

    def loadBand(self) -> None:
        """Load band data into the game."""
        self.band = BandTORLoader().getBands()[0]
  
    def getEvent(self, results: list[int]) -> EventTheOneRing:
        table = self._getTable(TableEvent)
        record = table.getRecord(results)
        if isinstance(record, EventTheOneRing):
            return record
        else:
            raise ValueError(f"Record is not of type EventTheOneRing: {record}")
        
    def chooseBand(self) -> None:
        """Choose a band from the available bands."""
        bands: list[BandTOR] = BandTORLoader().getBands()
        print(bands)
        strNumber:str = input("Choose Band by id >> ")
        id:int = int(strNumber)
        band = next((b for b in bands if b.id == id), None)
        if band is None:
            print("Band with the given id not found.")
            return
        print("Your choose:")
        print(band)
        self.band = band
        return
    
    def setupAllies(self) -> bool:
        """Setup allies for the band."""
        if not self.band.allies:
            print("No allies available for this band.")
            return False
        
        print("Available Allies:")
        for ally in self.band.allies:
            print(ally)
        
        strNumber:str = input("Choose Ally by id >> ")
        id:int = int(strNumber)
        ally = next((a for a in self.band.allies if a.id == id), None)
        if ally is None:
            print("Ally with the given id not found.")
            return False
        
        strNumber:str = input("Active or Camped Ally? (A/C) >> ")
        if strNumber.upper() == "C":
            ally.setActive(False)
        elif strNumber.upper() == "A":
            ally.setActive(True)
        else:
            print("Invalid choice. Defaulting to active.")
        
        print(f"Ally {ally.name} activated.")

        strNumber:str = input("Do you want modify another? (Y/N)>> ")
        if strNumber.upper() == "Y":
            return self.setupAllies()
        elif strNumber.upper() == "N":
            return False
        else:
            print("Invalid choice. Defaulting to no more allies.")
        return True
    
    
    def modifyBand(self) -> None:
        # strNumber:str = input("Band Armament LIGHT, READY or HEAVY >>")
        # try:
        #     armament: BandArmamentType = BandArmamentType[strNumber.upper()]
        # except KeyError:
        #     print("Invalid armament type. Please choose LIGHT, READY, or HEAVY.")
        #     return
        
        # strNumber:str = input("Band Faculty WAR, EXPERTISE or VIGILANCE >>")
        # try:
        #     faculty: BandFacultyType = BandFacultyType[strNumber.upper()]
        # except KeyError:
        #     print("Invalid Faculty type. Please choose WAR, EXPERTISE or VIGILANCE.")
        #     return
        
        # strNumber:str = input("Band Hunt Threshold >>")
        # try:
        #     huntThreshold: int = int(strNumber)
        # except KeyError:
        #     print("Invalid huntThreshold value. Please choose integer.")
        #     return

        print(self.band)

        armament: BandArmamentType = GameTORService.getArmament()
        faculty: BandFacultyType = GameTORService.getFaculty()
        huntThreshold: int = GameTORService.getHuntThreshold()
        
        # self.setupAllies()

        self.band.setArmament(armament)
        self.band.setFaculty(faculty)
        self.band.setHuntThreshold(huntThreshold)

        print(self.band)

    def chooseAssets(self) -> None:
        self.chooseBand()

    def modifyAssets(self) -> None:
        self.modifyBand()

