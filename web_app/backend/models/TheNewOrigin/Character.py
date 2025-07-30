from typing import Literal, List, Optional
from enum import Enum, auto
from dataclasses import dataclass

from pydantic import BaseModel
from sqlmodel import Relationship, Field

from web_app.backend.models.chatRecord import RecordBase
from web_app.backend.models.TheNewOrigin.Item import TNOItem_ORM, ItemSlotType, ItemMagicType, TNOItemDTO


class TNOAttributeType(Enum):
    BODY = auto()
    AGILE = auto()
    HEART  = auto()
    FLAIR  = auto()
    FORCE = auto()

class TNOSkillType(Enum):
    POWER_COMBAT = auto()
    PRECISION_COMBAT = auto()
    INSPIRATION = auto()
    TACTICS = auto()
    IMPULSE_MAGIC = auto() 

@dataclass
class TNOAttributes:
    body: int = 0
    agile: int = 0
    heart: int = 0
    flair: int = 0
    force: int = 0

    def to_dict(self):
        return {
            TNOAttributeType.BODY: self.body,
            TNOAttributeType.AGILE: self.agile,
            TNOAttributeType.HEART: self.heart,
            TNOAttributeType.FLAIR: self.flair,
            TNOAttributeType.FORCE: self.force,
        }

@dataclass
class TNOSkills:
    power_combat: int = 0
    precision_combat: int = 0
    inspiration: int = 0
    tactics: int = 0
    impulse_magic: int = 0

    def to_dict(self):
        return {
            TNOSkillType.POWER_COMBAT: self.power_combat,
            TNOSkillType.PRECISION_COMBAT: self.precision_combat,
            TNOSkillType.INSPIRATION: self.inspiration,
            TNOSkillType.TACTICS: self.tactics,
            TNOSkillType.IMPULSE_MAGIC: self.impulse_magic,
        }
    
class TNO_AttributeSheet():
    body: int = 0
    agile: int = 0
    heart: int = 0
    flair: int = 0
    force: int = 0

    character_id: Optional[int] = None
    
    
class TNO_AttributesSheet_DTO(BaseModel, TNO_AttributeSheet):
    id: Optional[int] = None
    model_config = {
        "from_attributes": True
    }

# class TNO_SkillsSheet_ORM(RecordBase, table=True):
#     power_combat: int = 0
#     precision_combat: int = 0
#     inspiration: int = 0
#     tactics: int = 0
#     impulse_magic: int = 0

#     character_id: Optional[int] = Field(default=None, foreign_key="tno_character_orm.id", unique=True)
    # character: Optional["TNO_Character_ORM"] = Relationship(back_populates="skillSheet")
    
class TNO_AttributesSheet_ORM(RecordBase, TNO_AttributeSheet, table=True):
    character_id: Optional[int] = Field(default=None, foreign_key="tno_character_orm.id", unique=True)
    character: Optional["TNO_Character_ORM"] = Relationship(
        back_populates="attributesSheet"
    )

    def updateByDTO(self, dto: TNO_AttributesSheet_DTO):
        self.body = dto.body
        self.agile = dto.agile
        self.heart = dto.heart
        self.flair = dto.flair
        self.force = dto.force
    
class TNO_Character_ORM(RecordBase, table=True):
    """
    Represents a character in The New Origin (TNO) game.
    Inherits from RecordBase to provide basic record functionality.
    """
    name: str = "default_name"
    user_id: str = ""
    # skills: TNOSkills = TNOSkills()
    # attribute: TNOAttributes = TNOAttributes()

    items: List["TNOItem_ORM"] = Relationship(back_populates="owner")
    # skillSheet: TNO_SkillsSheet_ORM = Relationship(back_populates="character")
    # attributesSheet: TNO_AttributesSheet_ORM = Relationship(back_populates="character", passive_deletes=True)

    attributesSheet: TNO_AttributesSheet_ORM = Relationship(
        back_populates="character"
    )

    def getAttributesSheet(self) -> TNO_AttributesSheet_ORM:
        return self.attributesSheet
    
    def updateAttrByDTO(self, dto: TNO_AttributesSheet_DTO):
        self.attributesSheet.updateByDTO(dto)

class TNO_Character_DTO(BaseModel):
    id: Optional[int]
    user_id: str
    name: str

    model_config = {
        "from_attributes": True
    }
