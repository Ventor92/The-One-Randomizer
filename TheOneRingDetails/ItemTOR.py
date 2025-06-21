from enum import Enum, auto
from dataclasses import dataclass

from TableService.Record import Record, Series

from TheOneRingDetails.SkillTOR import SkillTypeTOR

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from TheOneRingDetails.HeroTOR import HeroTOR  # Import tylko dla adnotacji typów

class ItemSlotTypeTOR(Enum):
    NONE = "None"
    JEWELRY = "Jewelry"
    WEAPON = "Weapon"
    ARMOR = "Armor"
    MISCELLANEOUS = "Miscellaneous"
    COAT = "Coat"
    SCABBARD = "Scabbard"

@dataclass
class Item(Record):
    id: str = ""
    name: str = "Unnamed Item"
    description: str = "No description available."

class MagicItemType(Enum):
    NORMAL = auto()
    UNUSUAL = auto()
    WONDERFUL = auto()

class ItemTOR(Item):
    def __init__(self, id="", name="Unnamed Item", description="No description available.",
                 slot=ItemSlotTypeTOR.NONE, benefits=None, idOwner="", owner=None,
                 isCursed=False, type=MagicItemType.NORMAL):
        self.id = id
        self.name = name
        self.description = description
        self.slot = slot
        self.benefits = benefits if benefits is not None else [SkillTypeTOR.NONE]
        self.idOwner = idOwner
        self.owner = owner
        self.isCursed = isCursed
        self.type = type

    def assignOwner(self, owner: 'HeroTOR') -> None:
        """Assign an owner to the item."""
        self.idOwner = owner.id
        self.owner = owner

    def unassignOwner(self) -> None:
        """Unassign the owner of the item."""
        self.idOwner = ""
        self.owner = None
    
    def checkOwnership(self, owner: 'HeroTOR') -> bool:
        """Check if the item is owned by the given hero."""
        return (self.idOwner == owner.id)

    @classmethod
    def fromRow(cls, row: Series):
        if row['benefit1'] == "" or row['benefit1'] is None:
            row['benefit1'] = SkillTypeTOR.NONE
        
        if row['benefit2'] == "" or row['benefit2'] is None:
            row['benefit2'] = SkillTypeTOR.NONE
        
        ret = cls(
            id=row['id'],
            name=row['name'],
            description = row['description'],
            slot=row['slot'],
            benefits = [row['benefit1'], row['benefit2']],
            idOwner=row['idOwner'],
            isCursed=row.get('isCursed', False),
            type=row['type'] if 'type' in row else MagicItemType.NORMAL
        )
        return ret 
    
    def toRow(self) -> Series:
        row = Series({
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'slot': self.slot if self.slot else ItemSlotTypeTOR.MISCELLANEOUS,
            'benefit1': self.benefits[0] if self.benefits[0] else SkillTypeTOR.NONE,
            'benefit2': self.benefits[1] if self.benefits[1] else SkillTypeTOR.NONE,
            'idOwner': self.idOwner if self.idOwner else "",
            'isCursed': self.isCursed if self.isCursed else False,
            'type': self.type if self.type else MagicItemType.NORMAL
        })
        return row