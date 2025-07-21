
from web_app.backend.models.chatRecord import ChatRecord
from web_app.backend.models.DiceRoll import DiceRoll, DiceRollORM, DiceRollDTO
from web_app.backend.models.chatRecord import ChatRecordType
from sqlalchemy.dialects.mysql import JSON as MySQLJSON
from enum import Enum, auto
from typing import List
from sqlmodel import Field

class GameType(str, Enum):
    NONE = "none"
    THE_ONE_RING = "the_one_ring"
    DUNGEONS_AND_DRAGONS = "dungeons_and_dragons"
    PATHFINDER = "pathfinder"

class Roll(ChatRecord):
    game: GameType = GameType.NONE
    # type: ChatRecordType = ChatRecordType.DICE_ROLL

class TORRollORM(DiceRoll, table=True):
    # breakdown: List[int] = Field(default_factory=list, sa_column_kwargs={"type_": MySQLJSON})
    type: ChatRecordType = Field(default=ChatRecordType.DICE_ROLL)

    @classmethod
    def fromDiceRoll(cls, dice_roll: DiceRoll):
        obj = cls.model_validate(dice_roll)
        obj.type = ChatRecordType.DICE_ROLL
        return obj
        
    def rollFeatDices(self, num_dices: int) -> List[int]:
        """
        Rolls the specified number of feat dice.
        :param num_dices: Number of feat dice to roll.
        :return: List of results from the rolled feat dice.
        """
        # self.resultFeatDices = [DiceRollORM.roll_dice(DiceType.FEAT) for _ in range(num_dices)]
        self.resultFeatDices = [1, 11, 6, 3, 12]  # Example results
        return self.resultFeatDices
    
    def rollSuccessDices(self, num_dices: int) -> List[int]:
        """
        Rolls the specified number of success dice.
        :param num_dices: Number of success dice to roll.
        :return: List of results from the rolled success dice.
        """
        # self.resultSuccessDices = [DiceRollORM.roll_dice(DiceType.SUCCESS) for _ in range(num_dices)]
        self.resultSuccessDices = [1, 2, 3, 4, 5, 6]  # Example results
        return self.resultSuccessDices

