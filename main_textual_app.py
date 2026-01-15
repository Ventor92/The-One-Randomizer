from typing import Optional

from textual import on
from textual.app import App, ComposeResult
from textual_app.UI.Screens.ScrnHome import ScrnHome
from textual_app.UI.Screens.ScrnTables import ScrnTables
from textual_app.UI.Events.events import OpenModalRandomRecord, LibraryChosen

from textual_app.UI.Events.events import RollRequest, UpdateModalLabel, TableIdsRequest, TableIdsResponse, TablesRequest, TablesResponse
from textual_app.UI.Wigets.MScrnRecord import MScrnRecord

from GameService.GameController import GameController, GameTOR
from textual_app.Application.Srvc_Table import Srvc_Table, GenericTable
from textual_app.Application.TablesLibrariesConfig import TablesLibrariesConfig, Library
from TableService.GenericTableLoader import GenericTableLoader

class MGApp(App):
    def __init__(self):
        self.tablesLibrariesConfig = TablesLibrariesConfig()
        self.genericTables: list[GenericTable] = []
        super().__init__()

    CSS_PATH = "textual_app/textual_app.tcss"

    def on_mount(self):
        self.push_screen(ScrnHome())

    @on(LibraryChosen)
    def on_lib_chosen(self, message: LibraryChosen):
        library: Optional[Library] = self.tablesLibrariesConfig.get_library_by_id(message.library_id)
        id = library.id if library else message.library_id
        name = library.name if library else ""
        self.push_screen(ScrnTables(id, name))

    @on(OpenModalRandomRecord)
    def open_modal_random_record(self, message: OpenModalRandomRecord):
        self.push_screen(MScrnRecord(id="record_screen", encounter="Re-Roll!", id_table=message.id_table))

    @on(RollRequest)
    def roll_request(self, message: RollRequest) -> None:
        id_table = message.id_table
        self.log(f"RollRequest received in MGApp for table id: {id_table}")

        table = next((t for t in self.genericTables if t.getId() == id_table), None)
        if table is None:
            raise Exception(f"Table with id '{id_table}' not found.")
        
        print(table.getDataFrame())

        record = table.rollRecord()
        if record is None:
            raise Exception(f"No record found after rolling on table '{table.getName()}'.")
        
        string = self.generate_roll_summary(table, record)

        self.screen.post_message(UpdateModalLabel(string))

    def generate_roll_summary(self, table, record):
        string: str = ""
        for k, v in table._diceMap.items():
            string += f"{k} ({v.getType().name}):".ljust(20) + f"{record[k]}\n"
            print(f"{k}: {v.getType().name} -> {record[k]}")
        
        dice_columns = list(table._diceMap.keys())
        record = record.drop(dice_columns)

        for col, val in record.items():
            string += f"{col}:".ljust(20) + f"{val}\n"
            print(f"{col}: {val}")
        return string



    @on(TableIdsRequest)
    def table_name_list_request(self, message: TableIdsRequest) -> None:
        self.log("TableIdsRequest received in MGApp")

        libs: dict[str, Library] = self.tablesLibrariesConfig.get_libraries_name_map()
        responseParam: dict[str, str] = {}
        for k, v in libs.items():
            responseParam[v.id] = v.name
            print(f"Library id: {v.id}, name: {v.name}")

        # libs is expected to be a dict[str, str] (id_name_map)
        responseMsg = TableIdsResponse(responseParam)

        self.log(f"Available table ids: {list(libs.keys())}")

        self.screen.post_message(responseMsg)

        self.log("Table names request processing completed in MGApp")


    @on(TablesRequest)
    def tables_request(self, message: TablesRequest) -> None:
        self.log("TablesRequest received in MGApp")

        message.library_id
        lib = self.tablesLibrariesConfig.get_library_by_id(message.library_id)

        self.genericTables.clear()

        print(f"Loading tables for library id: {message.library_id}")
        print(f"Found library: {lib}")

        tables = []
        if lib is not None:
            tables = lib.tables
        else:
            raise Exception(f"Library with id '{message.library_id}' not found.")
        
        for table in tables:
            df = GenericTableLoader.loadRecords(table.path, table.sheet_name)

            if table.column_dice_map is not None:
                genericTable = GenericTable(path=table.path, 
                                            sheetName=table.sheet_name, 
                                            id=table.id, 
                                            dataFrame=df, 
                                            diceMap=table.column_dice_map)
            else:
                raise Exception(f"Table '{table.sheet_name}' in library '{lib.name}' is missing 'column_dice_map' configuration.")
            
            self.genericTables.append(genericTable)

        print(f"Generic tables loaded: {[t.getName() for t in self.genericTables]}")
        responseMsg = TablesResponse(self.genericTables)

        self.screen.post_message(responseMsg)

        self.log("Tables request processing completed in MGApp")

if __name__ == "__main__":
    MGApp().run()
