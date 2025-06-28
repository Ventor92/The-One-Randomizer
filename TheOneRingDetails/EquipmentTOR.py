from enum import Enum, auto
from dataclasses import dataclass

from TheOneRingDetails.SkillTOR import SkillTypeTOR
from TheOneRingDetails.ItemTOR import ItemTOR, ItemSlotTypeTOR

  
class EquipmentTOR:
    def __init__(self):
        self.items: list[ItemTOR] = []

    def addItem(self, item: ItemTOR) -> None:
        """Add an item to the equipment."""
        self.items.append(item)

    def removeItem(self, item: ItemTOR) -> None:
        """Remove an item from the equipment."""
        if item in self.items:
            self.items.remove(item)
        else:
            print(f"Item {item.name} not found in equipment.")
    
    def findItemsByBenefit(self, benefit: SkillTypeTOR) -> list[ItemTOR]:
        """Find items that provide a specific benefit."""
        return [item for item in self.items if benefit in item.benefits]
    
    def showItems(self) -> None:
        """Display all items in the equipment."""
        if not self.items:
            print("No items in equipment.")
            return
        for item in self.items:
            print(f"ID: {item.id}, Name: {item.name}, Slot: {item.slot}, Benefits: {item.benefits}, Owner ID: {item.idOwner}")

    def __str__(self):
        return "\n".join(str(item) for item in self.items) if self.items else "No items in equipment."
    
    

