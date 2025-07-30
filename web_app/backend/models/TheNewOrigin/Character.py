from typing import Literal, List, Optional
from enum import Enum, auto
from dataclasses import dataclass

from pydantic import BaseModel
from sqlmodel import Relationship, Field

from web_app.backend.models.chatRecord import RecordBase
from web_app.backend.models.TheNewOrigin.Item import TNOItem_ORM, ItemSlotType, ItemMagicType, TNOItemDTO
from web_app.backend.models.TheNewOrigin.Sheet import TNO_AttributesSheet_DTO, TNO_AttributesSheet_ORM, TNO_SkillsSheet_ORM, TNO_SkillsSheet_DTO


    
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

    skillsSheet: TNO_SkillsSheet_ORM = Relationship(
        back_populates="character")
    attributesSheet: TNO_AttributesSheet_ORM = Relationship(
        back_populates="character")

    def getAttributes(self) -> TNO_AttributesSheet_ORM:
        return self.attributesSheet
    
    def getSkills(self) -> TNO_SkillsSheet_ORM:
        return self.skillsSheet
    
    def updateAttrByDTO(self, dto: TNO_AttributesSheet_DTO):
        self.attributesSheet.updateByDTO(dto)

    def updateSkillsByDTO(self, dto: TNO_SkillsSheet_DTO):
        self.skillsSheet.updateByDTO(dto)

class TNO_Character_DTO(BaseModel):
    id: Optional[int]
    user_id: str
    name: str

    model_config = {
        "from_attributes": True
    }
