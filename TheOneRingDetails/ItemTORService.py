from GameService.AssetSaver import RecordSaver

from TheOneRingDetails.HeroTOR import HeroTOR, ItemTOR


class ItemTORService:
    def __new__(cls, *args, **kwargs):
        raise TypeError(f"{cls.__name__} is a static utility class and cannot be instantiated.")
    
    @staticmethod
    def loadItems(filepath: str = "data/Band.xlsx", sheetName: str = "Items") -> list[ItemTOR]:
        """Load items from the specified file."""
        records = RecordSaver.loadRecords(ItemTOR, filepath,sheetName)
        items: list[ItemTOR] = []

        for record in records:
            if isinstance(record, ItemTOR):
                items.append(record)
            else:
                raise ValueError(f"Record is not of type HeroTOR: {record}")
        
        return items
    
    @staticmethod
    def __saveItem(item: ItemTOR, filepath: str = "data/Band.xlsx", sheetName: str = "Heroes") -> None:
        """Save a item to the specified file."""
        records: list[ItemTOR] = [item]
        RecordSaver.saveRecords(records, filepath, sheetName)
