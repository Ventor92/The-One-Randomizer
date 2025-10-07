from typing import Optional, Type

from TableService.EventService.TableEvent import TableEvent
from TheOneRingDetails.EventTheOneRing import EventTheOneRing
from TheOneRingDetails.ThreadTheOneRing import ThreadTOR
from TheOneRingDetails.MissionTOR import MissionTOR
from TableService.TableLoader import TableLoaderV2, TableLoaderExcel, Record
from web_app.backend.models.TheOneRing.Event import TOR_Event_DTO
from web_app.backend.models.TheOneRing.Thread import TOR_Thread_DTO
from web_app.backend.models.TheOneRing.Mission import TOR_Mission_DTO
from web_app.backend.models.TableRecord import Table
from web_app.backend.database.RecordTable_Repository import RecordTable_Repository

class RecordTable_EventTOR_Repository(RecordTable_Repository[EventTheOneRing]):
    recordType = EventTheOneRing

class RecordTable_ThreadTOR_Repository(RecordTable_Repository[ThreadTOR]):
    recordType = ThreadTOR

class RecordTable_MissionTOR_Repository(RecordTable_Repository[MissionTOR]):
    recordType = MissionTOR

class Table_Service:
    def __new__(cls, *args, **kwargs):
        raise NotImplementedError("This class cannot be instantiated. Use static methods only.")
    
    @staticmethod
    def rollEventTOR() -> Optional[TOR_Event_DTO]:
           
        table: Optional[Table] = RecordTable_EventTOR_Repository.getRecordTable()
        record = Table_Service._rollRecord(table)

        dto: TOR_Event_DTO = TOR_Event_DTO.model_validate(record)
        return dto
    
    @staticmethod
    def rollThreadTOR() -> Optional[TOR_Thread_DTO]:

        table: Optional[Table] = RecordTable_ThreadTOR_Repository.getRecordTable()
        record = Table_Service._rollRecord(table)

        dto: TOR_Thread_DTO = TOR_Thread_DTO.model_validate(record)
        return dto
    
    @staticmethod
    def rollMissionTOR() -> Optional[TOR_Mission_DTO]:

        table: Optional[Table] = RecordTable_MissionTOR_Repository.getRecordTable()
        record = Table_Service._rollRecord(table)
        dto: TOR_Mission_DTO = TOR_Mission_DTO.model_validate(record)
        return dto
    
    @staticmethod
    def _rollRecord(table: Optional[Table]) -> Optional[Record]:
        if table is not None:
            record = table.rollRecord()
        else:
            record = None

        return record
