from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Literal, Union, Annotated, Optional
from enum import Enum, auto
import uuid

from sqlmodel import SQLModel, Field
from DiceService.Dice import Dice, DiceType

class ChatRecordType(str, Enum):
    NONE = "none"
    MESSAGE = "message"
    DICE_ROLL = "dice_roll"

class RecordBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = field(default_factory=lambda: RecordBase.generate_uuid())
    created_at: datetime = Field(default_factory=lambda: RecordBase.get_current_timestamp())

    @staticmethod
    def generate_uuid() -> str:
        return str(uuid.uuid4())
    
    @staticmethod
    def get_current_timestamp() -> datetime:
        return datetime.now()
    
class ChatRecord(RecordBase):
    user_name: str = "Anonymous"
    role: str = "user"

# class Message(ChatRecord):
#     content: str = "Wiadomość od użytkownika"

# class MessageORM(Message, table=True):
#     type: ChatRecordType = ChatRecordType.MESSAGE

# class MessageDTO(Message):
#     type: Literal["message"] = ChatRecordType.MESSAGE.value 

class RollType(Enum):
    NONE = auto()
    STANDARD = auto()
    SKILL = auto()
    COIN = auto()

class Outcome(Enum):
    NONE = 'none'
    SUCCESS = 'success'
    SUCCESS_CONSEQUENCE = 'success-consequence'
    FAILURE = 'failure'
    COIN = 'coin'
    STANDARD = 'standard'

# class DiceRoll(ChatRecord, table=True):
class DiceRollDTO(ChatRecord):
    dice: DiceType = DiceType.D6    # Default to D6
    result: int = 0                # liczna wyrzuconych 6-tek 5-tek lub 1-nek
    breakdown: str = Field(default_factory=lambda: "[]")  # JSON string representation of breakdown
    modifier: int = 0
    character: Optional[str] = None
    purpose: Optional[str] = None
    outcome: Outcome = Outcome.NONE
    rollType: RollType = RollType.NONE
    type: Literal["dice_roll"] = "dice_roll" 