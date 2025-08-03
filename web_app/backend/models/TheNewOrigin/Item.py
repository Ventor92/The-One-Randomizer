from enum import Enum, auto
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, field_serializer
from sqlmodel import Field, Relationship

from web_app.backend.models.chatRecord import RecordBase

if TYPE_CHECKING:
    from web_app.backend.models.TheNewOrigin.Character import TNO_Character_ORM

# class StrEnum(str, Enum):
#     @staticmethod
#     def _generate_next_value_(name, start, count, last_values):
#         return name

class ItemSlotType(Enum):
    NONE = auto()
    JEWELRY = auto()
    WEAPON = auto()
    ARMOR = auto()
    MISCELLANEOUS = auto()
    COAT = auto()
    SCABBARD = auto()

class ItemMagicType(Enum):
    NONE = auto()
    NORMAL = auto()
    UNUSUAL = auto()
    WONDERFUL = auto()


class ItemFieldsMixin:
    name: str = "Unnamed Item"
    description: str = "No description"
    slot: ItemSlotType = ItemSlotType.MISCELLANEOUS
    isCursed: bool = False
    type: ItemMagicType = ItemMagicType.NORMAL
    owner_id: Optional[int] = Field(default=None, foreign_key="tno_character_orm.id")

class TNOItem_ORM(RecordBase, ItemFieldsMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner: Optional["TNO_Character_ORM"] = Relationship(back_populates="items")

class TNOItemDTO(BaseModel, ItemFieldsMixin):
    id: Optional[int]

    model_config = {
        "from_attributes": True
    }

    @field_serializer("slot")
    def serialize_slot(self, slot: ItemSlotType, _info):
        return slot.name
    
    @field_serializer("type")
    def serialize_type(self, type: ItemMagicType, _info):
        return type.name

