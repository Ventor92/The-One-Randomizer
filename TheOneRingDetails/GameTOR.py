from GameService.Game import Game
from TableService.Table import Table, Record

from TableService.MissionService.TableMission import TableMission
from TableService.EventService.TableEvent import TableEvent
from TableService.ThreadService.TableThread import TableThread
from TableService.BenefitService.TableBenefit import TableBenefit

from TheOneRingDetails.EventTheOneRing import EventTheOneRing
from TheOneRingDetails.ThreadTheOneRing import ThreadTOR
from TheOneRingDetails.MissionTOR import MissionTOR
from TheOneRingDetails.DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType
from TheOneRingDetails.EnemyTOR import EnemyTOR
from TheOneRingDetails.TreasuryTOR import BenefitTOR, TableBenefit, TreasuryTORFactory

from DiceService.DiceSet import DiceSet, Dice

from TheOneRingDetails.HeroTOR import HeroTOR
from TheOneRingDetails.BandTOR import BandTOR, BandDispositionType, BandArmamentType, BandSizeType, BandFacultyType, BandBurdenType
from TheOneRingDetails.BandTORLoader import BandTORLoader

from TheOneRingDetails.GameTORService import GameTORService
from TheOneRingDetails.HeroTORService import HeroTORService
from TheOneRingDetails.ItemTORService import ItemTORService, ItemTOR

from DispositionsService import DispositionsService, DiceFeatType

from utils.singleton import SingletonMeta

class GameTOR(Game, metaclass=SingletonMeta):
    def __init__(self, title: str = "The One Ring"):
        dices: list[Dice] = [DiceTheOneRing(DiceTheOneRingType.FEAT), DiceTheOneRing(DiceTheOneRingType.SUCCESS)]
        diceSet = DiceSet(dices) 

        tableEvent = TableEvent(EventTheOneRing, diceSet = diceSet, path="data/Table.xlsx", sheetName="Zdarzenia")
        tableThread = TableThread(ThreadTOR, path="data/Table.xlsx", sheetName="Wątki", dices = diceSet.getDiceSet())
        tableMission = TableMission(MissionTOR, path="data/Table.xlsx", sheetName="Missions", dices = diceSet.getDiceSet())

        diceSetBenefit = DiceSet([DiceTheOneRing(DiceTheOneRingType.SUCCESS), DiceTheOneRing(DiceTheOneRingType.SUCCESS)])
        tableBenefit = TableBenefit(BenefitTOR, path="data/Table.xlsx", sheetName="Benefits", diceSet=diceSetBenefit)
        tables: list[Table] = [
            tableEvent,
            tableMission,
            tableThread,
            tableBenefit
        ]
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
        self.chooseBand()
        self.hero = HeroTORService.chooseHero()
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
        DispositionsService.testBand(self.band, enemy, type, diceFeat, spentHope, bonusSuccess)
        pass

    def randomTable(self, arg) -> None:
        """Random table"""
        if len(arg) >= 1:
            sliced = arg.split()
            lenSliced = len(sliced)

            match lenSliced:
                case 1:
                    strType = sliced[0]

                    table = self.recognizeTable(strType)
                    
                    self.rollRecord(table)
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

                    self.getRecord(table, [numFeat, numSuccess])
                case _:
                    raise ValueError("Invalid argument. Expected at least: <tableType>")
                  
        else:
            raise ValueError("No arguments. Expected at least: <tableType>")

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
        strMight:str = input("setup enemy might >> ")
        strResistance:str = input("setup enemy resistance >> ")
        self.enemy = EnemyTOR(int(strMight), int(strResistance))

    def endFight(self) -> None:
        self.enemy = None

    def findTreasury(self) -> None:
        """Find a treasury for the band."""
        table = self._getTable(TableBenefit)
        if not isinstance(table, TableBenefit):
            raise ValueError(f"Expected TableBenefit, got {type(table)}")
        else:
            treasury = TreasuryTORFactory.createTreasuryTOR(table, 0)
            print(treasury)

        for item in treasury.treasure.magicItems:
            strMight:str = input(f"{self.hero.name} should take this item:{item}? (Y/n) >> ")
            if strMight.upper() == "Y":
                self.hero.addItem(item)
            else:
                print(f"Item {item.name} not taken by hero.")

    def grantAward(self, arg) -> None:
        self.findTreasury()