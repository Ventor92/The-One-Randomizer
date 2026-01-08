from .ItemTORService import ItemTORService

from ..Details.TreasuryTOR import TreasuryTOR, TreasuryTORFactory
from ..Details.HeroTOR import HeroTOR


class TreasuryTORService:
    """Service class for managing the Treasury of the Rings (TOR) data."""
    def __new__(cls, *args, **kwargs):
        raise TypeError(f"{cls.__name__} is a static utility class and cannot be instantiated.")
    
    @staticmethod
    def takeTreasure(treasury: TreasuryTOR, hero: HeroTOR):
        """Allow a character to take treasure from the treasury."""
        print(f"{hero.name} is taking treasure from {treasury.name}.")
        # Logic for taking treasure would go here

        hero.addTreasureWorth(treasury.treasure.value)
        treasury.treasure.value = 0


    @staticmethod
    def showTresure (treasury: TreasuryTOR):
        """Show the treasury."""
        # treasury = TreasuryTORFactory.createTreasuryTOR(TableBenefit())
        print(treasury)

    @staticmethod
    def takeMagicItems(treasury: TreasuryTOR, hero: HeroTOR):
        """Find a treasury for the band."""
        for item in treasury.treasure.magicItems:
            print(f"{item}")
            strMight:str = input(f"{hero.name} Should take this item? (Y/n) >> ")
            if strMight.upper() == "Y":
                hero.addItem(item)
                ItemTORService.saveItem(item)
            else:
                print(f"Item {item.name} not taken by hero.")


