from dataclasses import dataclass
from enum import Enum, auto

from TheOneRingDetails.SkillTOR import SkillTypeTOR
from TheOneRingDetails.ItemTOR import ItemTOR, ItemSlotTypeTOR, MagicItemType

class TreasurySizeTOR(Enum):
    NONE = 0
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class TreasureTOR:
    def __init__(self, value=0, magicItems=None):
        self.value = value
        self.magicItems = magicItems if magicItems is not None else []

class TreasuryTOR:
    def __init__(self, size=TreasurySizeTOR.NONE, treasure=None, name="Treasury Name", description="Treasury Description"):
        self.size = size
        self.treasure = treasure if treasure is not None else TreasureTOR()
        self.name = name
        self.description = description

    def __str__(self):
        return (f"Treasury Size: {self.size.name},\n" 
                f"Value: {self.treasure.value},\n" 
                f"Magic Items: {[item.name for item in self.treasure.magicItems]}\n"
                f"Description: {self.description}\n"
                f"Name: {self.name}"
                )
    

from DiceService.DiceSet import DiceSet, Dice
from TheOneRingDetails.DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType
from TableService.BenefitService.TableBenefit import TableBenefit
from TheOneRingDetails.BenefitTOR import BenefitTOR
from TheOneRingDetails.EquipmentTOR import EquipmentTOR

class TreasuryTORFactory:
    # def __init__(self, tableBenefit: TableBenefit):
    #     self.tableBenefit = tableBenefit

    @staticmethod
    def __specifyTreasurySize(bonus: int = 0) -> TreasurySizeTOR:
        print(f"Calculating treasury size with bonus: {bonus}")
        dice = DiceTheOneRing(DiceTheOneRingType.SUCCESS)
        results = dice.roll(1 + bonus)
        result = max(results)

        match result:
            case 1 | 2:
                return TreasurySizeTOR.SMALL
            case 3 | 4:
                return TreasurySizeTOR.MEDIUM
            case 5 | 6:
                return TreasurySizeTOR.LARGE
            case _:
                return TreasurySizeTOR.NONE

    @staticmethod  
    def __specifyDiceSets(TreasurySizeTOR) -> tuple[DiceSet, DiceSet]: 
        numDiceFeat: int = 2
        numDiceSuccess: int = 1
        multiplier: int = 0
        match TreasurySizeTOR:
            case TreasurySizeTOR.SMALL:
                multiplier = 1
            case TreasurySizeTOR.MEDIUM:
                multiplier = 2
            case TreasurySizeTOR.LARGE:
                multiplier = 3
            case _:
                multiplier = 0

        dicesMagicItems: list[Dice] = []
        dicesSuccess: list[Dice] = []


        for _ in range(numDiceFeat * multiplier):
            dicesMagicItems.append(DiceTheOneRing(DiceTheOneRingType.FEAT))

        for _ in range(numDiceSuccess * multiplier):
            dicesSuccess.append(DiceTheOneRing(DiceTheOneRingType.SUCCESS))


        diceSetMagicItems = DiceSet(dicesMagicItems)
        diceSetSuccess = DiceSet(dicesSuccess)
        return diceSetMagicItems, diceSetSuccess
    
    @staticmethod
    def __specifyTreasureValue(diceSetSuccess: DiceSet) -> int:
        print("Calculating treasure value...")
        results = diceSetSuccess.roll()
        totalValue = sum(results)
        return totalValue
    
    @staticmethod
    def __specifyMagicItemType() -> MagicItemType:
        print("Specifying magic item type...")
        results = DiceTheOneRing(DiceTheOneRingType.SUCCESS).roll(1)
        match results[0]:  # Assuming results is a list with one element
            case 1 | 2 | 3:
                return MagicItemType.UNUSUAL
            case 4 | 5:
                return MagicItemType.WONDERFUL
            case 6:
                return MagicItemType.WONDERFUL
                # return MagicItemType.WEAPON
            case _:
                return MagicItemType.NORMAL
    
    @staticmethod
    def __rollMagicItems(diceSetFeat: DiceSet, tableBenefit: TableBenefit) -> list[ItemTOR]:
        results = diceSetFeat.roll()
        items: list[ItemTOR] = []
        for result in results:
            match result:
                case 12:
                    typeItem = TreasuryTORFactory.__specifyMagicItemType()
                    isCursed = False
                    magicItem = ItemTOR(name=typeItem.name, description="Magic item.", isCursed=isCursed, type=typeItem)
                    items.append(magicItem)
                case 11:
                    typeItem = TreasuryTORFactory.__specifyMagicItemType()
                    isCursed = True
                    magicItem = ItemTOR(name=typeItem.name, description="Cursed magic item.", isCursed=isCursed, type=typeItem)
                    items.append(magicItem)
                case _:
                    pass

        for item in items:
            match item.type:
                case MagicItemType.UNUSUAL:
                    benefitNum = 1
                case MagicItemType.WONDERFUL:
                    benefitNum = 2
                case MagicItemType.NORMAL:
                    benefitNum = 1
                case _:
                    benefitNum = 0
            
            for _ in range(benefitNum):  # Assuming 2 benefits for unusual items
                resultsRollBenefit = tableBenefit.roll()
                print(f"Rolling for benefit: {resultsRollBenefit}")
                benefit = tableBenefit.getRecord(resultsRollBenefit)
                print(f"Benefit rolled: {benefit}")
                if isinstance(benefit, BenefitTOR):
                    item.benefits.append(benefit.benefit)
                else:
                    raise ValueError(f"Expected BenefitTOR, got {type(benefit)}")
        
        return items

    @staticmethod
    def createTreasuryTOR(tableBenefit: TableBenefit, bonus: int = 0) -> TreasuryTOR:
        size: TreasurySizeTOR = TreasuryTORFactory.__specifyTreasurySize(bonus=bonus)
        diceSetMagicItems, diceSetSuccess = TreasuryTORFactory.__specifyDiceSets(size)
        value: int = TreasuryTORFactory.__specifyTreasureValue(diceSetSuccess)
        magicItems: list[ItemTOR] = TreasuryTORFactory.__rollMagicItems(diceSetFeat=diceSetMagicItems, tableBenefit=tableBenefit)
        treasureTOR = TreasureTOR(value=value, magicItems=magicItems)
        treasury = TreasuryTOR(size=size, treasure=treasureTOR, name="Treasury Name", description="Treasury Description") 
        return treasury

         
        




