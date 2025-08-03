from enum import Enum, auto
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel
from sqlmodel import Field, Relationship

from web_app.backend.models.chatRecord import RecordBase

from TheOneRingDetails.EventTheOneRing import EventTheOneRing

if TYPE_CHECKING:
    from web_app.backend.models.TheNewOrigin.Character import TNO_Character_ORM


class TOR_Event_DTO(BaseModel, EventTheOneRing):
    # id: Optional[int]

    model_config = {
        "from_attributes": True
    }

