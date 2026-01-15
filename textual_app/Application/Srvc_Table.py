import pandas as pd

from textual.widgets import Label, Tabs, Tab, TabPane, DataTable

from Application.GenericTableLoader import GenericTableLoader

from Application.GenericTable import GenericTable
from Application.TablesLibrariesConfig import TablesLibrariesConfig

class Srvc_Table:
    def __new__(cls, *args, **kwargs):
        raise TypeError(f"{cls.__name__} is a static utility class and cannot be instantiated.")
    
    # @staticmethod
    # def _getAllRecords(table: Table) -> list[Record]:
    #     return table.getAllRecords()

    # @staticmethod
    # def _createColumnNames(table: Table) -> list[str]:
    #     listRecords: list[Record] = table.getAllRecords()
    #     columns = list(listRecords[0].toRawDict().keys())
    #     return columns
    
    # @staticmethod
    # def createDataTable(table: Table) -> DataTable:
    #     dataTable = DataTable()

    #     columns = Srvc_Table._createColumnNames(table)
    #     dataTable.add_columns(*columns)

    #     listRecords: list[Record] = Srvc_Table._getAllRecords(table)
        
    #     rows = [list(record.toRawDict().values()) for record in listRecords]
    #     dataTable.add_rows(rows)

    #     return dataTable

    # @staticmethod
    # def loadTables() -> list[GenericTable]:
    #     cfg: TablesLibrariesConfig = TablesLibrariesConfig()
    #     tables = cfg.get_all_table_configs()
    #     genericTables: list[GenericTable] = []
    #     for table_conf in tables:
    #         table = GenericTableLoader.loadRecords(
    #             path=table_conf["path"],
    #             sheet_name=table_conf["sheet_name"]
    #         )
    #         genTable = GenericTable(
    #             path=table_conf["path"],
    #             sheetName=table_conf["sheet_name"],
    #             dataFrame=table,
    #             diceMap=table_conf.get("column_dice_map", {})
    #         )
    #         genericTables.append(genTable)

    #     return genericTables
    
    @staticmethod
    def df2DataTable(df: pd.DataFrame) -> DataTable:
        table = DataTable()

        # Kolumny
        table.add_columns(*df.columns.astype(str))

        # Wiersze
        for row in df.itertuples(index=False):
            table.add_row(*map(str, row))

        return table
    