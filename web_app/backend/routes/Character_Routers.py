from fastapi import APIRouter, Body, WebSocket, WebSocketDisconnect, Query
from pydantic import BaseModel, Field
from sqlmodel import Session
import time
from typing import List, Literal, Union, Annotated

from fastapi import FastAPI, Depends, HTTPException, status

from ..database.database import create_db_and_tables, get_session

from web_app.backend.services.Character_Service import Character_Service
from web_app.backend.models.TheNewOrigin.Character import TNO_Character_ORM, TNO_Character_DTO, TNO_AttributesSheet_DTO
from web_app.backend.models.TheNewOrigin.Item import TNOItem_ORM, TNOItemDTO

# from ..services.Chat_Service import Chat_Service


import logging
logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/api/character",
    tags=["character"]
)

@router.get("/item", response_model=List[TNOItemDTO], summary="Pobierz przedmioty postaci")
def get_items(char_id: int = Query(None, description="Character Id"), session: Session = Depends(get_session)):
    """
    Pobiera przedmioty postaci z bazy danych.
    """
    character = session.get(TNO_Character_ORM, char_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    items = Character_Service.get_items(char_id)
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this character")
    else:
        return items




@router.post("/item", response_model=TNOItemDTO, status_code=status.HTTP_201_CREATED, summary="Dodaj przedmiot postaci")
def give_item(dto: TNOItemDTO, char_id: int = Query(None, description="Character Id"), session: Session = Depends(get_session)):
    """
    Tworzy nową wiadomość i zapisuje ją w bazie danych.
    """
    character = session.get(TNO_Character_DTO, char_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    else:
        dto.owner_id = char_id
        dtoResponse = Character_Service.add_item(dto)
        
    return dtoResponse

@router.post("/create", response_model=TNO_Character_DTO, status_code=status.HTTP_201_CREATED, summary="Stwórz postać")
def createCharacter(dto: TNO_Character_DTO):
    dtoResponse = Character_Service.createCharacter(dto)
        
    return dtoResponse

@router.patch("/att", response_model=TNO_AttributesSheet_DTO, summary="Update atrybutów postaci")
def assignAttribute(dto: TNO_AttributesSheet_DTO, char_id: int = Query(None, description="Character Id")):
    dtoResponse = Character_Service.updateCharacterAttribute(dto, char_id)
    if (dtoResponse.id == None) or (dtoResponse.character_id == None):
        raise HTTPException(status_code=404, detail=f"No character found: {char_id}")
    else:
        return dtoResponse

@router.get("/att", response_model=TNO_AttributesSheet_DTO, summary="Update atrybutów postaci")
def getAttribute(dto: TNO_AttributesSheet_DTO, char_id: int = Query(None, description="Character Id")):
    dtoResponse = Character_Service.getCharacterAttribute(char_id)
    if (dtoResponse.id == None) or (dtoResponse.character_id == None):
        raise HTTPException(status_code=404, detail=f"No character found: {char_id}")
    else:
        return dtoResponse


# @router.post("/roll", response_model=DiceRollDTO, status_code=status.HTTP_201_CREATED, summary="Dodaj rzut kością")
# def create_roll(dto: DiceRollDTO):
#     """
#     Tworzy nowy rzut kością i zapisuje go w bazie danych.
#     """
#     diceRollORM = DiceRollORM.fromDiceRoll(dto, dto.breakdown)
#     dto = Chat_Service.add_roll(diceRollORM)
#     return dto

# @router.get("/records", response_model=List[RecordUnion], summary="Pobierz historię wiadomości i rzutów kośćmi")
# def get_records():
#     """
#     Pobiera historię wiadomości i rzutów kośćmi z bazy danych.
#     """
#     list = Chat_Service.get_history()
#     return list