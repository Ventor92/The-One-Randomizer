from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Body
from typing import List, Literal, Union, Annotated
from pydantic import BaseModel, Field

from fastapi.responses import HTMLResponse

from web_app.backend.models.chatRecord import DiceRollDTO, RecordBase
from web_app.backend.models.Message import MessageDTO

from ..services.Chat_Service import Chat_Service

router = APIRouter(
    prefix="/api/ws",
    tags=["websocket"]
)

import logging
logger = logging.getLogger("uvicorn")

active_connections: List[WebSocket] = []

RecordUnion = Annotated[Union[MessageDTO, DiceRollDTO], Field(discriminator="type")]

# class ChatRecordDTO(BaseModel):
#     type: Literal["none", "dice_roll", "message"] = "none"

# class MessageDTO(ChatRecordDTO, Message):
#     # type = "message"
#     pass

# class DiceRollDTO(ChatRecordDTO, DiceRoll):
#     self.type = "dice_roll"
#     pass

# ChatEvent = Union[MessageDTO, DiceRollDTO]

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <textarea id="chat_log" rows="20" cols="100"></textarea><br>
        <input type="text" id="messageInput" autocomplete="off"/><button onclick="sendMessage()">Send</button>
        <script>
            const ws = new WebSocket("ws://localhost:8000/api/ws/chat");
            ws.onmessage = function(event) {
                const chatLog = document.getElementById('chat_log');
                chatLog.value += event.data + '\\n';
            };
            function sendMessage() {
                const input = document.getElementById("messageInput");
                ws.send(input.value);
                input.value = '';
            }
        </script>
    </body>
</html>
"""

@router.get("/")
async def get():
    return HTMLResponse(html)

@router.post("/chat/send/message", response_model=MessageDTO)
def add_history_roll(dto: MessageDTO = Body(...)):
    dto.content = "DUPA"
    return dto

@router.get("/chat/history", response_model=List[RecordUnion])
def get_chat_history():
    return Chat_Service.get_history()

@router.websocket("/roll")
async def websocket_roll(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            dto = DiceRoll.model_validate_json(data)
            await broadcast(dto.model_dump_json())
    except WebSocketDisconnect:
        active_connections.remove(websocket)



@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    logger.info("To jest informacja w stylu uvicorn")
    try:
        while True:
            data = await websocket.receive_text()
            # await websocket.send_text(f"Message text was: {data}")
            # dto = MessageDTO.model_validate_json(data)
            await broadcast(data)
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def broadcast(data: str):
    for connection in active_connections:
        await connection.send_text(data)