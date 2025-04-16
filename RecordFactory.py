from Record import Record
from pandas import Series

class RecordFactory:
    _creators = {}

    @classmethod
    def register(cls, eventClassId: int, creator_func):
        cls._creators[eventClassId] = creator_func

    @classmethod
    def create(cls, classId: int, row: Series) -> Record:
        if classId not in cls._creators:
            raise ValueError(f"Unknown record type: {classId}")
        return cls._creators[classId](row)