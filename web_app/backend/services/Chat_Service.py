from ..models.chatRecord import RecordBase
from ..models.Message import MessageORM, MessageDTO
from ..models.DiceRoll import DiceRollORM, DiceRollDTO
from ..database.Repository_Controller import RepositoryController
from ..database.Repository_Service import RepositoryService
from sqlmodel import Session
from collections.abc import Sequence

class MessageRepository(RepositoryService[MessageORM]):
    model = MessageORM

class DiceRollRepository(RepositoryService[DiceRollORM]):
    model = DiceRollORM

class Chat_Service:
    def __new__(cls, *args, **kwargs):
        raise NotImplementedError("This class cannot be instantiated. Use static methods only.")
    
    @staticmethod
    def add_message(message: MessageDTO) -> MessageDTO:
        
        messageORM = MessageORM.fromMessage(dto)
        dto = Chat_Service.__add_message(messageORM)

        return dto
        

    @staticmethod
    def __add_message(message: MessageORM) -> MessageDTO:
        """
        Adds a message to the chat history.
        :param message: Message object to be added.
        :return: The added Message object.
        """
        engine = RepositoryController.getEngine()
        with Session(engine) as session:
            RepositoryService.add(session, message)
        dto = MessageDTO.fromMessage(message)
        return dto
    
    @staticmethod
    def add_roll(roll: DiceRollORM) -> DiceRollDTO:
        """
        Adds a dice roll to the chat history.
        :param roll: DiceRollDTO object to be added.
        :return: The added DiceRollDTO object.
        """
        engine = RepositoryController.getEngine()
        with Session(engine) as session:
            RepositoryService.add(session, roll)
        dto = DiceRollDTO.fromDiceRoll(roll)
        return dto

    @staticmethod
    def get_history() -> Sequence[RecordBase]:
        """
        Retrieves the chat history from both tables.
        :return: A combined list of MessageORM and DiceRollORM objects.
        """
        engine = RepositoryController.getEngine()
        with Session(engine) as session:
            messages = MessageRepository.get_all(session)
            rolls = DiceRollRepository.get_all(session)
            records = messages + rolls
            records.sort(key=lambda r: r.created_at)
        return records

