from typing import Optional

from TableService.EventService.TableEvent import TableEvent
from TheOneRingDetails.EventTheOneRing import EventTheOneRing
from TableService.TableLoader import TableLoaderV2, TableLoaderExcel, Record
from web_app.backend.models.TableRecord import TOR_TableEvent, Table
from web_app.backend.models.TheOneRing.Event import TOR_Event_DTO
from web_app.backend.database.RecordTable_Repository import RecordTable_Repository

class RecordTable_EventTOR_Repository(RecordTable_Repository[EventTheOneRing]):
    recordType = EventTheOneRing

class Table_Service:
    def __new__(cls, *args, **kwargs):
        raise NotImplementedError("This class cannot be instantiated. Use static methods only.")
    
    @staticmethod
    def rollEventTOR() -> Optional[TOR_Event_DTO]:

        table = RecordTable_EventTOR_Repository.getRecordTable()
        if table is not None:
            event = table.rollRecord()
            dto = TOR_Event_DTO.model_validate(event) 
        else: 
            dto = None

        return dto