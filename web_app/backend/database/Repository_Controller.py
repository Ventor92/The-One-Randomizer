from .database import get_engine

class RepositoryController():
    @staticmethod
    def getEngine():
        return get_engine()