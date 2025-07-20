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
