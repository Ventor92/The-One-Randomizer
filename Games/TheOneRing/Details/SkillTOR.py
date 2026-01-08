from enum import Enum, auto
from dataclasses import dataclass

class AttributesTypeTOR(Enum):
    NONE = auto()
    STRENGTH = auto()
    HEART = auto()
    WITS = auto()

class SkillTypeTOR(Enum):
    NONE = auto()
    AWE = auto()
    ATHLETICS = auto()
    AWARENESS = auto()
    HUNTING = auto()
    SONG = auto()
    CRAFT = auto()
    ENHEARTEN = auto()
    TRAVEL = auto()
    INSIGHT = auto()
    HEALING = auto()
    COURTESY = auto()
    BATTLE = auto()
    PERSUADE = auto()
    STEALTH = auto()
    SCAN = auto()
    EXPLORE = auto()
    RIDDLE = auto()
    LORE = auto()

class SkillGroupTypeTOR(Enum):
    NONE = auto()
    OBSERVATION = auto()
    MANNERS = auto()
    SURVIVAL = auto()
    PERSONALITY = auto()
    PROFESSION = auto()
    MOBILITY = auto()

@dataclass
class SkillTOR:
    skill: SkillTypeTOR = SkillTypeTOR.NONE
    relatedAttribute: AttributesTypeTOR = AttributesTypeTOR.NONE
    relatedGroup: SkillGroupTypeTOR = SkillGroupTypeTOR.NONE

    def __str__(self):
        return f"Skill: {self.skill.name}, Attribute: {self.relatedAttribute.name}, Group: {self.relatedGroup.name}"


