from GameService.Game import Game
from TableService.Table import Table, Record

from TableService.MissionService.TableMission import TableMission
from TableService.EventService.TableEvent import TableEvent
from TableService.ThreadService.TableThread import TableThread
from TableService.BenefitService.TableBenefit import TableBenefit
from DiceService.DiceSet import DiceSet, Dice

from ..Details.EventTheOneRing import EventTheOneRing
from ..Details.ThreadTheOneRing import ThreadTOR
from ..Details.MissionTOR import MissionTOR
from ..Details.DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType
from ..Details.EnemyTOR import EnemyTOR
from ..Details.TreasuryTOR import TableBenefit, TreasuryTORFactory
from ..Details.HeroTOR import HeroTOR
from ..Details.BandTOR import BandTOR, BandDispositionType, BandArmamentType, BandSizeType, BandFacultyType, BandBurdenType
from ..Details.BandTORLoader import BandTORLoader

from .ClashTORService import ClashTORService, StancesTOR
from .FightTORCtrl import FightTORCtrl
from .GameTORService import GameTORService
from .HeroTORService import HeroTORService
from .ItemTORService import ItemTORService, ItemTOR
from .TreasuryTORController import TreasuryTORController

from DispositionsService import DispositionsService, DiceFeatType

from utils.singleton import SingletonMeta

class GameTOR(Game, metaclass=SingletonMeta):
    def __init__(self, title: str = "The One Ring"):
        dices: list[Dice] = [DiceTheOneRing(DiceTheOneRingType.FEAT), DiceTheOneRing(DiceTheOneRingType.SUCCESS)]
        diceSet = DiceSet(dices) 

        tableEvent = TableEvent(EventTheOneRing, diceSet = diceSet, path="data/Table.xlsx", sheetName="Events")
        tableThread = TableThread(ThreadTOR, path="data/Table.xlsx", sheetName="Threads", dices = diceSet.getDiceSet())
        tableMission = TableMission(MissionTOR, path="data/Table.xlsx", sheetName="Missions", dices = diceSet.getDiceSet())

        tableBenefit = TableBenefit(path="data/Table.xlsx", sheetName="Benefits")
        tables: list[Table] = [
            tableEvent,
            tableMission,
            tableThread,
            tableBenefit
        ]

        for table in tables:
            table.loadRecords()

        print("GameTOR __init__")
        self.band: BandTOR
        self.loadBand()

        self.hero: HeroTOR

        self.enemy: EnemyTOR | None = None

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
        
    def chooseBand(self, id: int = 0) -> None:
        """Choose a band from the available bands."""
        bands: list[BandTOR] = BandTORLoader().getBands()
        print(bands)
        if id == 0:
            while True:
                strNumber: str = input("Choose Band by id >> ")
                try:
                    id = int(strNumber)
                    band = next((b for b in bands if b.id == id), None)
                    if band is None:
                        print("Band with the given id not found.")
                        continue
                    print("Your choose:")
                    print(band)
                    self.band = band
                    return
                except ValueError:
                    print("Invalid input. Please enter a valid integer id.")
        else:
            band = next((b for b in bands if b.id == id), None)
            if band is None:
                raise ValueError(f"Band with id {id} not found.")
            else:
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
        print(self.band)

        armament: BandArmamentType = GameTORService.getArmament()
        faculty: BandFacultyType = GameTORService.getFaculty()
        huntThreshold: int = GameTORService.getHuntThreshold()
        
        # self.setupAllies()

        self.band.setArmament(armament)
        self.band.setFaculty(faculty)
        self.band.setHuntThreshold(huntThreshold)

        print(self.band)

    @staticmethod
    def linkItemsToOwners(items: list[ItemTOR], heroes: list[HeroTOR]) -> None:
        """Assign an item to the hero."""
        for hero in heroes:
            for item in items:
                if item.checkOwnership(hero):
                    hero.addItem(item)


    def chooseAssets(self) -> None:
        self.chooseBand(1)
        self.hero = HeroTORService.chooseHero("qqqq1111")
        items: list[ItemTOR] = ItemTORService.loadItems()
        GameTOR.linkItemsToOwners(items, [self.hero])

    def modifyAssets(self) -> None:
        """Modify assets for the game."""

        if self.enemy is None:
            strNumber:str = input("Enter to fight? (Y/N) >> ")
            if strNumber.upper() == "Y":
                self.startFight()
            else: 
                pass
        else:
            strNumber:str = input("End fight? (Y/N) >> ")
            if strNumber.upper() == "Y":
                self.endFight()
            else: 
                pass

        strNumber:str = input("Modify Band? (Y/N) >> ")
        if strNumber.upper() == "Y":
            self.modifyBand()
        else:
            pass

    def test(self, arg) -> None:
        """Test method for the game."""

        try:
            str1, str2, str3, str4 = arg.split()
            type = DispositionsService.str2DispositionType(str1)
            diceFeat = DispositionsService.str2DiceFeatType(str2)
            spentHope = int(str3)
            bonusSuccess = int(str4)
        except ValueError:
            type = BandDispositionType.NONE
            diceFeat = DiceFeatType.NORMAL
            spentHope = 0
            bonusSuccess = 0

        print(f"{type.name} {diceFeat.name}")

        enemy = self.enemy or EnemyTOR(0, 0)
        if self.enemy is None:
            DispositionsService.testBand(self.band, enemy, type, diceFeat, spentHope, bonusSuccess)
        else:
            ClashTORService.makeClash(self.band, enemy, StancesTOR.NONE, spentHope, bonusSuccess)

    def _getTableByRecordType(self, recordType: type[Record]) -> Table:
        for table in self.tables:
            if table.isRecordType(recordType):
                return table
        raise ValueError(f"No table found for record type: {recordType}")

    def randomRecord(self, recordType: type[Record]) -> Record:
        """Random record from table by record type."""
        table = self._getTableByRecordType(recordType)
        table.roll
        record = self.rollRecord(table)
        return record
    

    def randomTable(self, arg) -> None:
        """Random table"""
        self.randomTableV2(arg)

    def randomTableV2(self, arg) -> Record:
        """Random table"""
        if len(arg) >= 1:
            sliced = arg.split()
            lenSliced = len(sliced)

            match lenSliced:
                case 1:
                    strType = sliced[0]

                    table = self.recognizeTable(strType)
                    
                    record = self.rollRecord(table)
                case 3:
                    strType = sliced[0]
                    strNumFeat = sliced[1]
                    strNumSuccess = sliced[2]

                    table = self.recognizeTable(strType)
                    
                    try:
                        numFeat = int(strNumFeat)
                        numSuccess = int(strNumSuccess)
                    except ValueError:
                        raise ValueError(f"Invalid argument. Expected: Int as <numFeat> & <numSuccess>")

                    record = self.getRecord(table, [numFeat, numSuccess])
                case _:
                    raise ValueError("Invalid argument. Expected at least: <tableType>")
                    record = None
                  
        else:
            raise ValueError("No arguments. Expected at least: <tableType>")
            record = None

        return record 

    def recognizeTable(self, strType):
        table_mapping = {
            "EVENT": TableEvent,
            "MISSION": TableMission,
            "THREAD": TableThread
        }
        try:
            return table_mapping[strType.upper()]
        except KeyError:
            raise ValueError(f"Invalid argument. Type: {strType}")
        
    def startFight(self) -> None:
        strMight:str = input("Setup enemy might >> ")
        strResistance:str = input("Setup enemy resistance >> ")
        self.enemy = EnemyTOR(int(strMight), int(strResistance))

    def endFight(self) -> None:
        self.enemy = None

    def findTreasury(self) -> None:
        """Find a treasury for the band."""
        table = TableBenefit()
        treasury = TreasuryTORFactory.createTreasuryTOR(table, 0)
        TreasuryTORController.enterToTreasury(treasury, self.hero)

    def grantAward(self, arg) -> None:
        self.findTreasury()

    def showCharacter(self, arg) -> None:
        """Show character details."""
        if self.hero is None:
            raise ValueError("Hero is not set.")
        else:
            HeroTORService.showHero(self.hero)
            print(f"Band: {self.band}")
            print(f"Enemy: {self.enemy}") if self.enemy else print("No enemy in the game.")

    def takeClash(self) -> None:
        """Take a clash in the game."""
        if self.enemy is None:
            raise ValueError("No enemy to clash with.")
        else:
            ClashTORService.makeClash(self.band, self.enemy, StancesTOR.NONE)

    def enterTheFight(self) -> None:
        """Enter the fight with the enemy."""
        FightTORCtrl.enterFight(self.band)
    
    def takeDecisiveAction(self) -> None:
        """Take a decisive action in the game."""
