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
from web_app.backend.models.TheOneRing.Thread import TOR_Thread_DTO
from web_app.backend.models.TheOneRing.Mission import TOR_Mission_DTO
from web_app.backend.services.Table_Service import Table_Service

from google import genai
from google.genai import types

import logging
logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/api/table/enhanced",
    tags=["table enhanced"]
)

client = genai.Client()

base_model: str = "gemini-2.5-flash"
base_system_instruction="You are the creative assistance of Game Master - Lore Master, " \
    "in ttRPG The One Ring 2e based on Lord of the Ring universe." \
    "The Response provide in polish language"

client.models.generate_content(
  model=base_model,
  contents="What is AI?",
  config=types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(
      thinking_budget=0
    )
  )
)


class RecordEnhanced(BaseModel):
    event_name: str
    event_description: str
    creative_extension: str

class RecordEnhanced_DTO(BaseModel):
    enhances: list[RecordEnhanced]
    event: TOR_Event_DTO

class AdditionalContext_DTO(BaseModel):
    variationsNumber: int = 1
    locations: Optional[list[str]]
    circumstances: Optional[list[str]]
    characters: Optional[list[str]]

@router.get("/tor_event", response_model=RecordEnhanced_DTO, summary="Pobierz The One Ring Event")
@router.post("/tor_event", response_model=RecordEnhanced_DTO, summary="Pobierz The One Ring Event")
def get_event(input: AdditionalContext_DTO):

    dto: Optional[TOR_Event_DTO] = Table_Service.rollEventTOR()

    if not dto:
        raise HTTPException(status_code=404, detail="No event found")
    # else:
    #     return dto
    
    # Request the model to populate the schema
    eventInJSON: str = dto.model_dump_json()
    additionalContextInJSON: str = input.model_dump_json()

    response = client.models.generate_content(
        model=base_model,
        contents=[eventInJSON, additionalContextInJSON, 
                  f"Based on provided random event and additional context in json form, you action to do is create {input.variationsNumber} creative extensions of event"],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[RecordEnhanced],
            system_instruction=base_system_instruction
        ),
    )
    
    enhances: list[RecordEnhanced] = []
    if isinstance(response.parsed, list):
      for parsed in response.parsed:
          enhances.append(RecordEnhanced.model_validate(parsed))
      else:
          pass
          # raise: "ERROR!"

    # time.sleep(0.75)
    # enhances = [
    #     RecordEnhanced(event_name="Event Name Develop", event_description="Event Description Develop", creative_extension= "Creative Extension Develop")
    #     ]
    ret: RecordEnhanced_DTO = RecordEnhanced_DTO(enhances=enhances, event = dto)
    return ret

    