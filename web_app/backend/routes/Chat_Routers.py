from fastapi import APIRouter, Body, WebSocket, WebSocketDisconnect, Query
from pydantic import BaseModel, Field
import time
from typing import List, Literal, Union, Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database.database import create_db_and_tables, get_session
from ..models.Message import Message

from web_app.backend.models.chatRecord import RecordBase
from web_app.backend.models.Message import MessageDTO, MessageORM
from web_app.backend.models.DiceRoll import DiceRollDTO, DiceRollORM 

from ..services.Chat_Service import Chat_Service


import logging
logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/api/chat",
    tags=["chat"]
)

active_connections: List[WebSocket] = []

RecordUnion = Annotated[Union[MessageDTO, DiceRollDTO], Field(discriminator="type")]


@router.websocket("/roll")
async def websocket_roll(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            dto = DiceRollDTO.model_validate_json(data)
            diceRollORM = DiceRollORM.fromDiceRoll(dto, dto.breakdown)
            dto = Chat_Service.add_roll(diceRollORM)
            json = dto.model_dump_json()
            await broadcast(json)
    except WebSocketDisconnect:
        active_connections.remove(websocket)

@router.websocket("/message")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    # logger.info("To jest informacja w stylu uvicorn")
    try:
        while True:
            data = await websocket.receive_text()
            dto = MessageDTO.model_validate_json(data)
            dto = Chat_Service.add_message(dto)
            json = dto.model_dump_json()
            await broadcast(json)
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def broadcast(data: str):
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_text(data)
        except Exception:
            disconnected.append(connection)
    for connection in disconnected:
        active_connections.remove(connection)

@router.post("/message", response_model=MessageDTO, status_code=status.HTTP_201_CREATED, summary="Dodaj wiadomość")
def create_message(dto: MessageDTO):
    """
    Tworzy nową wiadomość i zapisuje ją w bazie danych.
    """
    messageORM = MessageORM.fromMessage(dto)
    dto = Chat_Service.add_message(messageORM)
    return dto

@router.post("/roll", response_model=DiceRollDTO, status_code=status.HTTP_201_CREATED, summary="Dodaj rzut kością")
def create_roll(dto: DiceRollDTO):
    """
    Tworzy nowy rzut kością i zapisuje go w bazie danych.
    """
    diceRollORM = DiceRollORM.fromDiceRoll(dto, dto.breakdown)
    dto = Chat_Service.add_roll(diceRollORM)
    return dto

@router.get("/records", response_model=List[RecordUnion], summary="Pobierz historię wiadomości i rzutów kośćmi")
def get_records():
    """
    Pobiera historię wiadomości i rzutów kośćmi z bazy danych.
    """
    list = Chat_Service.get_history()
    return list