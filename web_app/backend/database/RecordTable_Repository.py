from typing import TypeVar, Generic, Type, List, Optional, Sequence

from TableService.EventService.TableEvent import TableEvent
from TheOneRingDetails.EventTheOneRing import EventTheOneRing
from TheOneRingDetails.ThreadTheOneRing import ThreadTOR
from TableService.TableLoader import TableLoaderV2, TableLoaderExcel, Record
from web_app.backend.models.TableRecord import Table, RandomTable

from web_app.backend.models.RandomTableFactory import TableFactory

tables:Sequence[Table] = TableFactory.build_all_tables()

A = TypeVar("A", bound=Record)
class RecordTable_Repository(Generic[A]):
    recordType: type[A]

    @classmethod
    def getRecordTable(cls):
        for table in tables:
            recordType = table.getRecordType()
            if recordType is cls.recordType:
                return table



