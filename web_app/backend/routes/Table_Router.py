from typing import List, Literal, Union, Annotated, Optional
import time

from fastapi import APIRouter, Body, WebSocket, WebSocketDisconnect, Query
from pydantic import BaseModel, Field
from sqlmodel import Session

from fastapi import FastAPI, Depends, HTTPException, status

from ..database.database import create_db_and_tables, get_session

from web_app.backend.services.Character_Service import Character_Service
from web_app.backend.models.TheNewOrigin.Character import TNO_Character_ORM, TNO_Character_DTO, TNO_AttributesSheet_DTO, TNO_SkillsSheet_DTO
from web_app.backend.models.TheNewOrigin.Item import TNOItem_ORM, TNOItemDTO

from web_app.backend.models.TheOneRing.Event import TOR_Event_DTO
from web_app.backend.services.Table_Service import Table_Service

import logging
logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/api/table",
    tags=["table"]
)

@router.get("/tor_event", response_model=TOR_Event_DTO, summary="Pobierz The One Ring Event")
def get_event():

    dto: Optional[TOR_Event_DTO] = Table_Service.rollEventTOR()

    if not dto:
        raise HTTPException(status_code=404, detail="No event found")
    else:
        return dto