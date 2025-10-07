from enum import Enum, auto
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel
from sqlmodel import Field, Relationship

from web_app.backend.models.chatRecord import RecordBase

from TheOneRingDetails.ThreadTheOneRing import ThreadTOR



class TOR_Thread_DTO(BaseModel, ThreadTOR):
    # id: Optional[int]

    model_config = {
        "from_attributes": True
    }

