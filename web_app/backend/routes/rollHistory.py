from fastapi import APIRouter, Body, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Optional, Literal
import time

router = APIRouter(
    prefix="/api/history",
    tags=["history"]
)

class DiceRoll(BaseModel):
    id: str
    timestamp: int
    dice: str
    result: int
    breakdown: List[int]
    modifier: int
    character: Optional[str] = None
    purpose: Optional[str] = None
    outcome: Optional[Literal['success', 'success-consequence', 'failure', 'coin', 'standard']] = None
    rollType: Literal['skill', 'coin', 'standard']

historyRoll: list[DiceRoll] = []

class RollRecordRequest(BaseModel):
    sides: int

class DiceRollResponse(BaseModel):
    records: list[DiceRoll]

@router.post("/rolls", response_model=DiceRoll)
def add_history_roll(roll: DiceRoll = Body(...)):
    historyRoll.append(roll)
    return roll

@router.get("/rolls", response_model=DiceRollResponse)
def get_history_rolls():
    breakdown: list[int] = [1, 2, 3, 4, 5, 6]

    if breakdown.count(6) > 0:
        result = breakdown.count(6)
    elif breakdown.count(5) > 0:
        result = breakdown.count(5)
    elif breakdown.count(1) > 0:
        result = breakdown.count(1)
    else:
        result = 0

    diceRoll = DiceRoll(
        id="unique-id",
        timestamp=int(time.time()),
        dice=f"d6",
        result=result,
        breakdown=breakdown,
        modifier=0,
        character="Sample Character",
        purpose="Sample Purpose",
        outcome="success",
        rollType="skill"
    )

    records = historyRoll if historyRoll else [diceRoll]
    return DiceRollResponse(records=records)

@router.websocket("/ws/rolls")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Here you can process the incoming message and send a response
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")