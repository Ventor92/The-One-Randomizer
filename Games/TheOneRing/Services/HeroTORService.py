from GameService.AssetSaver import RecordSaver

from ..Details.HeroTOR import HeroTOR

class HeroTORService:
    def __new__(cls, *args, **kwargs):
        raise TypeError(f"{cls.__name__} is a static utility class and cannot be instantiated.")
    
    @staticmethod
    def __loadHeroes(filepath: str = "data/Band.xlsx", sheetName: str = "Heroes") -> list[HeroTOR]:
        """Load heroes from the specified file."""
        records = RecordSaver.loadRecords(HeroTOR, filepath,sheetName)
        heroes: list[HeroTOR] = []

        for record in records:
            if isinstance(record, HeroTOR):
                heroes.append(record)
            else:
                raise ValueError(f"Record is not of type HeroTOR: {record}")
        
        return heroes
    
    @staticmethod
    def __saveHero(hero: HeroTOR, filepath: str = "data/Band.xlsx", sheetName: str = "Heroes") -> None:
        """Save a hero to the specified file."""
        records: list[HeroTOR] = [hero]
        RecordSaver.saveRecords(records, filepath, sheetName)

    @staticmethod
    def __chooseHero(heroes: list[HeroTOR], uuid:str = "") -> HeroTOR:
        """Choose a hero from list."""
        if not heroes:
            raise ValueError("No heroes available to choose from.")
        
        print("Available Heroes:")
        for hero in heroes:
            print(f"{hero.id}: {hero.name}")
        
        if uuid == "":
            strNumber: str = input("Choose Hero by id >> ")
        else:
            print(f"Using UUID: {uuid}")
            strNumber = uuid
                
        chosenOne = next((h for h in heroes if h.id == strNumber), None)
        if chosenOne is None:
            raise ValueError(f"Hero with id {strNumber} not found.")
        else:
             print(f"You have chosen: {chosenOne.name}")
        return chosenOne

    @staticmethod
    def chooseHero(uuid: str = "") -> HeroTOR:
        """Choose a hero from the available heroes."""
        heroes = HeroTORService.__loadHeroes()
        hero: HeroTOR = HeroTORService.__chooseHero(heroes, uuid)
        return hero
    
    @staticmethod
    def showHero(hero: HeroTOR) -> None:
        """Show the details of a hero."""
        if not isinstance(hero, HeroTOR):
            raise ValueError(f"Expected HeroTOR, got {type(hero)}")
        
        print(f"Hero Details:\n{hero}")

