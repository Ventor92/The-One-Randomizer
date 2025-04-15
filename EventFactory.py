from Event import Event
from pandas import Series

class EventFactory:
    _creators = {}

    @classmethod
    def register(cls, eventClassId: int, creator_func):
        cls._creators[eventClassId] = creator_func

    @classmethod
    def create(cls, eventClassId: int, row: Series) -> Event:
        if eventClassId not in cls._creators:
            raise ValueError(f"Unknown event type: {eventClassId}")
        return cls._creators[eventClassId](row)