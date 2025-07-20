from fastapi import APIRouter
from enum import Enum, auto

class GameType(str, Enum):
    TOR = "TOR"
    DND = "DND"
    OTHER = "OTHER"

class SkillRollDTO():
    game: GameType = GameType.TOR
    featDice: int = 1
    skillDice: int = 1
    skillType: str = "Standard"

class EventRollDTO():
    pass

router = APIRouter(
    prefix="/api/roll",
    tags=["chat"]
)

@router.get("/", response_model=List[RecordUnion], summary="Pobierz historię wiadomości i rzutów kośćmi")
def create_roll(dto: DiceRollDTO):