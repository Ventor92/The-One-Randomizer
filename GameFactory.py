from TableService.Record import Record

class GameFactory:
    _creators = {}

    @classmethod
    def register(cls, gameClassId: int, creator_func):
        cls._creators[gameClassId] = creator_func

    @classmethod
    def create(cls, classId: int) -> Record:
        if classId not in cls._creators:
            raise ValueError(f"Unknown record type: {classId}")
        return cls._creators[classId]()