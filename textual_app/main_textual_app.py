from typing import Optional

from textual import on
from textual.app import App, ComposeResult
from UI.Screens.ScrnHome import ScrnHome
from UI.Screens.ScrnTables import ScrnTables
from UI.Events.events import LibrariesRequest, OpenModalRandomRecord, LibraryChosen, RollRequestV2, RollResponseV2

from UI.Events.events import RollRequest, UpdateModalLabel, TablesRequest, TablesResponse, LibrariesResponse
from UI.Wigets.MScrnRecord import MScrnRecord

from Application.Srvc_Table import Srvc_Table
from Application.TablesLibrariesConfig import TablesLibrariesConfig, Library
from Application.GenericTableLoader import GenericTableLoader
from Application.GenericTable import GenericTable

class TheOneRandomizerApp(App):
    def __init__(self):
        super().__init__()
        self.title = "The One Randomizer"
        self.tablesLibrariesConfig: Optional[TablesLibrariesConfig] = None
        self.genericTables: list[GenericTable] = []

    CSS_PATH = "textual_app.tcss"

    def on_mount(self):
        self.push_screen(ScrnHome())
        self.tablesLibrariesConfig = TablesLibrariesConfig()

    @on(LibraryChosen)
    def on_lib_chosen(self, message: LibraryChosen):
        library: Optional[Library] = self.tablesLibrariesConfig.get_library_by_id(message.library_id) if self.tablesLibrariesConfig else None
        library_id = library.id if library else message.library_id
        name = library.name if library else ""
        self.push_screen(ScrnTables(library_id, name))

    @on(OpenModalRandomRecord)
    def open_modal_random_record(self, message: OpenModalRandomRecord):
        self.push_screen(MScrnRecord(id="record_screen", encounter="Re-Roll!", id_table=message.id_table))


    @on(RollRequestV2)
    def roll_request_v2(self, message: RollRequestV2) -> None:
        id_table = message.id_table
        self.log(f"RollRequestV2 received in TheOneRandomizerApp for table id: {id_table}")

        table = next((t for t in self.genericTables if t.getId() == id_table), None)
        if table is None:
            raise Exception(f"Table with id '{id_table}' not found.")
        
        record = table.rollRecord()

        if record is None:
            raise Exception(f"No record found after rolling on table '{table.getName()}'.")
        
        record = tuple(record.array)

        self.screen.post_message(RollResponseV2(record))

    @on(RollRequest)
    def roll_request(self, message: RollRequest) -> None:
        id_table = message.id_table
        self.log(f"RollRequest received in TheOneRandomizerApp for table id: {id_table}")

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
    
    @on(LibrariesRequest)
    def libraries_request(self, message: LibrariesRequest) -> None:
        self.log("LibrariesRequest received in TheOneRandomizerApp")

        libraries: list[Library] = []
        if self.tablesLibrariesConfig is not None:
            libraries = self.tablesLibrariesConfig.get_libraries()
        else:
            raise RuntimeError("TablesLibrariesConfig is not initialized in TheOneRandomizerApp during LibrariesRequest handling.")

        responseMsg = LibrariesResponse(libraries)

        self.log(f"Available libraries: {[lib.name for lib in libraries]}")

        self.screen.post_message(responseMsg)

        self.log("Libraries request processing completed in TheOneRandomizerApp")

    @on(TablesRequest)
    def tables_request(self, message: TablesRequest) -> None:
        self.log("TablesRequest received in TheOneRandomizerApp")

        if self.tablesLibrariesConfig is not None:
            lib = self.tablesLibrariesConfig.get_library_by_id(message.library_id)
        else:
            raise RuntimeError("TablesLibrariesConfig is not initialized in TheOneRandomizerApp during TablesRequest handling.")

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

        self.log("Tables request processing completed in TheOneRandomizerApp")

if __name__ == "__main__":
    print("Starting The One Randomizer App...")
    TheOneRandomizerApp().run()
