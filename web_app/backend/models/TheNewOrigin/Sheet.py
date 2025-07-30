from typing import Literal, List, Optional, TYPE_CHECKING
from enum import Enum, auto
from dataclasses import dataclass

from pydantic import BaseModel
from sqlmodel import Relationship, Field

from web_app.backend.models.chatRecord import RecordBase

if TYPE_CHECKING:
    from web_app.backend.models.TheNewOrigin.Character import TNO_Character_ORM

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

class TNO_SkillsSheet():
    power_combat: int = 0
    precision_combat: int = 0
    inspiration: int = 0
    tactics: int = 0
    impulse_magic: int = 0

    character_id: Optional[int] = None

class TNO_SkillsSheet_DTO(BaseModel, TNO_SkillsSheet):
    id: Optional[int] = None
    model_config = {
        "from_attributes": True
    }

class TNO_SkillsSheet_ORM(RecordBase, TNO_SkillsSheet, table=True):

    character_id: Optional[int] = Field(default=None, foreign_key="tno_character_orm.id", unique=True)
    character: Optional["TNO_Character_ORM"] = Relationship(back_populates="skillsSheet")

    def updateByDTO(self, dto: TNO_SkillsSheet_DTO):
        self.power_combat = dto.power_combat
        self.precision_combat = dto.precision_combat
        self.inspiration = dto.inspiration
        self.tactics = dto.tactics
        self.impulse_magic = dto.impulse_magic
