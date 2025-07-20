from typing import Literal

from web_app.backend.models.chatRecord import ChatRecord, ChatRecordType

class Message(ChatRecord):
    content: str = "Wiadomość od użytkownika"

class MessageORM(Message, table=True):
    type: ChatRecordType = ChatRecordType.MESSAGE

    @classmethod
    def fromMessage(cls, message: Message):
        obj = cls.model_validate(message)
        obj.type = ChatRecordType.MESSAGE

        return obj
    
class MessageDTO(Message):
    type: Literal["message"] = ChatRecordType.MESSAGE.value
    # type: ChatRecordType = ChatRecordType.MESSAGE

    @classmethod
    def fromMessage(cls, message: Message):
        obj = cls.model_validate(message)
        obj.type = "message"

        return obj
