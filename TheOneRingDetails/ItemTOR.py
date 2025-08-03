from enum import Enum, auto
from dataclasses import dataclass

from TableService.Record import Record, Series

from TheOneRingDetails.SkillTOR import SkillTypeTOR

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from TheOneRingDetails.HeroTOR import HeroTOR  # Import tylko dla adnotacji typów

class ItemSlotTypeTOR(Enum):
    NONE = auto()
    JEWELRY = auto()
    WEAPON = auto()
    ARMOR = auto()
    MISCELLANEOUS = auto()
    COAT = auto()
    SCABBARD = auto()

class Item(Record):
    def __init__(self, id="", name="Unnamed Item", description="No description available."):
        super().__init__(id)
        self.name = name
        self.description = description

class MagicItemType(Enum):
    NONE = 0
    NORMAL = 1
    UNUSUAL = 2
    WONDERFUL = 3

class ItemTOR(Item):
    def __init__(self, id="", name="Unnamed Item", description="No description available.",
                 slot=ItemSlotTypeTOR.NONE, benefits=None, idOwner="", owner=None,
                 isCursed=False, type=MagicItemType.NORMAL):
        super().__init__(id)
        self.name: str = name
        self.description: str = description
        self.slot: ItemSlotTypeTOR = slot
        self.benefits: list[SkillTypeTOR] = [SkillTypeTOR.NONE, SkillTypeTOR.NONE]
        if benefits is None:
            self.benefits: list[SkillTypeTOR] = [SkillTypeTOR.NONE, SkillTypeTOR.NONE]
        else:
            for i, benefit in enumerate(benefits):
                if i < len(self.benefits):
                    self.benefits[i] = benefit             
            
        self.idOwner: str = idOwner
        self.owner = owner
        self.isCursed:bool = isCursed
        self.type: MagicItemType = type

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
            id=str(row['id']),
            name=row['name'],
            description=row['description'],
            slot=ItemSlotTypeTOR[row['slot']] if row['slot'] else ItemSlotTypeTOR.NONE,
            benefits=[
            SkillTypeTOR[row['benefit1']] if row['benefit1'] else SkillTypeTOR.NONE,
            SkillTypeTOR[row['benefit2']] if row['benefit2'] else SkillTypeTOR.NONE
            ],
            idOwner=row['idOwner'],
            isCursed=row.get('isCursed', False),
            type=MagicItemType[row['type']] if 'type' in row and row['type'] else MagicItemType.NORMAL
        )
        return ret
    
    @staticmethod
    def getAmountOfBenefitsByItemType(typeItem: MagicItemType) -> int:
        # print(f"Getting amount of benefits for item type: {typeItem.name}")
        match typeItem:
            case MagicItemType.NORMAL | MagicItemType.UNUSUAL:
                amountOfBenefits = 1
            case MagicItemType.WONDERFUL:
                amountOfBenefits = 2
            case _:
                amountOfBenefits = 0

        return amountOfBenefits
    
    def toRow(self) -> Series:
        row = Series({
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'slot': str(self.slot.name) if self.slot else str(ItemSlotTypeTOR.MISCELLANEOUS.name),
            'benefit1': str(self.benefits[0].name) if self.benefits[0] else str(SkillTypeTOR.NONE.name),
            'benefit2': str(self.benefits[1].name) if self.benefits[1] else str(SkillTypeTOR.NONE.name),
            'idOwner': self.idOwner if self.idOwner else "",
            'isCursed': self.isCursed if self.isCursed else False,
            'type': str(self.type.name) if self.type else str(MagicItemType.NORMAL.name)
        })
        return row
    
    def __str__(self):
        # return (f"Item: {self.name} - {self.description}\r\n")
        return (f"[{self.id}]:{self.name} - {self.description}\r\n"
                f"\t{self.slot.name}, {self.type.name}{' - CURSED' if self.isCursed else ''},\r\n"
                f"\tBenefits: \r\n\t\t{', '.join(benefit.name for benefit in self.benefits)}\r\n"
                f"\t[{self.id}]\r\n"
            )