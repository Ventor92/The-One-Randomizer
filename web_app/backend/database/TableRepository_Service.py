from typing import TypeVar, Generic, Type, List, Optional

from DiceService.Dice import DiceType, DiceResults

from web_app.backend.models.TableRecord import Table

T = TypeVar("T")  # Typ modelu

class TableRepository_Service(Generic[T]):
    model: Type[T]

    @classmethod
    # def getRecord(self, results: DiceResults):
    def get(cls, table: Table, results: DiceResults) -> Optional[T]:
        return table.getRecord(results)