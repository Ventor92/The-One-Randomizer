from fastapi import APIRouter
from pydantic import BaseModel
import random

router = APIRouter(
    prefix="/api/dice",
    tags=["dice"]
)

class DiceRollRequest(BaseModel):
    sides: int

class DiceRollResponse(BaseModel):
    result: int

@router.post("/roll", response_model=DiceRollResponse)
def roll_dice(payload: DiceRollRequest):
    result = random.randint(1, payload.sides)
    return {"result": result}