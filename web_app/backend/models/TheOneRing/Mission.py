from enum import Enum, auto
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel
from sqlmodel import Field, Relationship

from web_app.backend.models.chatRecord import RecordBase

from TheOneRingDetails.MissionTOR import MissionTOR



class TOR_Mission_DTO(BaseModel, MissionTOR):
    # id: Optional[int]

    model_config = {
        "from_attributes": True
    }

