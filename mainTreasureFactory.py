from DiceService.DiceSet import DiceSet, Dice
from TableService.BenefitService.TableBenefit import TableBenefit

from Games.TheOneRing.Details.BenefitTOR import BenefitTOR
from Games.TheOneRing.Details.DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType
from Games.TheOneRing.Details.TreasuryTOR import TreasuryTORFactory



if __name__ == "__main__":
    # Example usage of the TreasuryTORFactory
    diceSetBenefit = DiceSet([DiceTheOneRing(DiceTheOneRingType.SUCCESS), DiceTheOneRing(DiceTheOneRingType.SUCCESS)])
    tableBenefit = TableBenefit(BenefitTOR, path="data/Table.xlsx", sheetName="Benefits", diceSet=diceSetBenefit)
  
    treasury = TreasuryTORFactory.createTreasuryTOR(tableBenefit, bonus=0)
    print(f"Treasury Size: {treasury.size.name}")
    print(f"Treasury Value: {treasury.treasure.value}")
    print("Magic Items:")
    for item in treasury.treasure.magicItems:
        print(f"  - Name: {item.name}")
        print(f"    Description: {item.description}")
        print(f"    Cursed: {'Yes' if item.isCursed else 'No'}")
        print(f"    Type: {item.type.name}")
        print(f"    Benefits: {[benefit.name for benefit in item.benefits]}")