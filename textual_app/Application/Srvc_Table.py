from textual.widgets import Label, Tabs, Tab, TabPane, DataTable

from TableService.Table import Table, Record
from GameService.Game import Game

class Srvc_Table:
    def __new__(cls, *args, **kwargs):
        raise TypeError(f"{cls.__name__} is a static utility class and cannot be instantiated.")
    
    @staticmethod
    def _getAllRecords(table: Table) -> list[Record]:
        return table.getAllRecords()

    @staticmethod
    def _createColumnNames(table: Table) -> list[str]:
        listRecords: list[Record] = table.getAllRecords()
        columns = list(listRecords[0].toRawDict().keys())
        return columns
    
    @staticmethod
    def createDataTable(table: Table) -> DataTable:
        dataTable = DataTable()

        columns = Srvc_Table._createColumnNames(table)
        dataTable.add_columns(*columns)

        listRecords: list[Record] = Srvc_Table._getAllRecords(table)
        
        rows = [list(record.toRawDict().values()) for record in listRecords]
        dataTable.add_rows(rows)

        return dataTable