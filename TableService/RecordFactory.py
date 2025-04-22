from TableService.Record import Record
from pandas import Series

class RecordFactory:
    _creators = {}

    @classmethod
    def register(cls, typeRecord: type[Record], creator_func):
        cls._creators[typeRecord] = creator_func

    @classmethod
    def create(cls, typeRecord: type[Record], row: Series) -> Record:
        if typeRecord not in cls._creators:
            raise ValueError(f"Unknown record type: {typeRecord}")
        return cls._creators[typeRecord](row)