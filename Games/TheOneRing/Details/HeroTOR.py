from pandas import Series

from .CharacterTOR import CharacterTOR
from .EquipmentTOR import EquipmentTOR, ItemTOR
from TableService.Record import Record

class HeroTOR(Record, CharacterTOR):
    def __init__(self, id: str = "", name: str = "Hero of the Ring"):
        super().__init__(id)
        CharacterTOR.__init__(self, name)
        self.equipment = EquipmentTOR()

    def addItem(self, item: ItemTOR) -> None:
        """Add an item to the hero's inventory."""
        item.assignOwner(self)
        self.equipment.addItem(item)
    
    def removeItem(self, item: ItemTOR) -> None:
        """Remove an item from the hero's inventory."""
        item.unassignOwner()
        self.equipment.removeItem(item)

    @classmethod
    def fromRow(cls, row: Series):
        return cls(
            id = row['id'],
            name = row['name'],
        )
    
    def __str__(self):
        return (f"HeroTOR(id={self.id}, name={self.name}, "
                f"equipment=\r\n\t{self.equipment})")



