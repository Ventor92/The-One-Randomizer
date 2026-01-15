from textual.message import Message

from TableService.GenericTable import GenericTable

class LibraryChosen(Message):
    def __init__(self, library_id: str):
        self.library_id = library_id
        super().__init__()

class OpenModalRandomRecord(Message):
    def __init__(self, id_table: str):
        self.id_table = id_table
        super().__init__()

class TableIdsRequest(Message):
    pass

class TableIdsResponse(Message):
    def __init__(self, id_name_map: dict[str, str]):
        self.id_name_map = id_name_map
        super().__init__()

class RollRequest(Message):
    def __init__(self, id_table: str):
        self.id_table = id_table
        super().__init__()

class GoToMainMenu(Message):
    pass

class UpdateModalLabel(Message):
    def __init__(self, text: str):
        self.text = text
        super().__init__()

class TablesRequest(Message):
    def __init__(self, library_id: str):
        self.library_id = library_id
        super().__init__()

class TablesResponse(Message):
    def __init__(self, tables: list[GenericTable]):
        self.tables = tables
        super().__init__()