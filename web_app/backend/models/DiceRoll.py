from typing import Literal, Optional, List
from enum import Enum, auto

from sqlmodel import SQLModel, Field, Column

from DiceService.Dice import Dice, DiceType
from web_app.backend.models.chatRecord import ChatRecord, ChatRecordType

from sqlalchemy.dialects.mysql import JSON as MySQLJSON

class RollType(str, Enum):
    NONE = "NONE"
    STANDARD = "STANDARD"
    SKILL = "SKILL"
    COIN = "COIN"

class Outcome(str, Enum):
    NONE = "NONE"
    SUCCESS = "SUCCESS"
    SUCCESS_CONSEQUENCE = "SUCCESS-CONSEQUENCE"
    FAILURE = "FAILURE"
    COIN = "COIN"
    STANDARD = "STANDARD"

# from sqlalchemy import JSON
# class DiceRollORM(DiceRoll, table=True):
#     type: ChatRecordType = ChatRecordType.DICE_ROLL
#     # breakdown: str = Field(default_factory=lambda: "[]")  # JSON string representation of breakdown
    
#     breakdown: list[int] = Field(sa_column=Field(sa_column=JSON))

#     @classmethod
#     def fromDiceRoll(cls, base: DiceRollDTO):
#         obj = cls(
#             dice=base.dice,
#             result=base.result,
#             modifier=base.modifier,
#             character=base.character,
#             purpose=base.purpose,
#             outcome=base.outcome,
#             rollType=base.rollType,
#             user_name=base.user_name,
#             role=base.role,
#             breakdown=json.dumps(getattr(base, "breakdown", [])),
#         )

#         return obj
  
from typing import Literal

from web_app.backend.models.chatRecord import ChatRecord, ChatRecordType

class DiceRoll(ChatRecord):
    dice: DiceType = DiceType.D6    # Default to D6
    result: int = 0                # liczna wyrzuconych 6-tek 5-tek lub 1-nek
    modifier: int = 0
    character: Optional[str] = None
    purpose: Optional[str] = None
    outcome: Outcome = Outcome.NONE
    rollType: RollType = RollType.NONE

class DiceRollORM(DiceRoll, table=True):
    type: ChatRecordType = ChatRecordType.DICE_ROLL
    # breakdown: List[int] = Field(default_factory=list, sa_column_kwargs={"type_": MySQLJSON})
    breakdown: List[int] = Field(sa_column=Column(MySQLJSON))

    # Needed for Column(JSON)
    # class Config:
    #     arbitrary_types_allowed = True

    @classmethod
    def fromDiceRoll(cls, diceRoll: DiceRoll, breakdown: List[int] = []):
        obj = cls.model_validate(diceRoll)
        obj.type = ChatRecordType.DICE_ROLL
        obj.breakdown = breakdown

        return obj
    
class DiceRollDTO(DiceRoll):
    breakdown: list[int] = []
    type: Literal["dice_roll"] = ChatRecordType.DICE_ROLL.value 

    @classmethod
    def fromDiceRoll(cls, diceRoll: DiceRoll):
        obj = cls.model_validate(diceRoll)
        obj.type = "dice_roll"

        return obj