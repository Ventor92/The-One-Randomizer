from typing import TypeVar, Generic, Type, List, Optional

from TableService.EventService.TableEvent import TableEvent
from TheOneRingDetails.EventTheOneRing import EventTheOneRing
from TableService.TableLoader import TableLoaderV2, TableLoaderExcel, Record
from web_app.backend.models.TableRecord import TOR_TableEvent, Table

loaderEventTOR = TableLoaderExcel(recordType=EventTheOneRing, path="data/Table.xlsx", sheet_name="Zdarzenia")

tables:list[Table] = [TOR_TableEvent(loaderEventTOR)]

A = TypeVar("A", bound=Record)
class RecordTable_Repository(Generic[A]):
    recordType: type[A]

    @classmethod
    def getRecordTable(cls):
        for table in tables:
            recordType = table.getRecordType()
            if recordType is cls.recordType:
                return table



