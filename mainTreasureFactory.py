from TheOneRingDetails.BenefitTOR import BenefitTOR
from TheOneRingDetails.DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType
from DiceService.DiceSet import DiceSet, Dice

from TheOneRingDetails.TreasuryTOR import TreasuryTORFactory

from TableService.BenefitService.TableBenefit import TableBenefit

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