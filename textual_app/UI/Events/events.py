from textual.message import Message

from Application.GenericTable import GenericTable

from Application.Library import Library

class LibraryChosen(Message):
    def __init__(self, library_id: str):
        self.library_id = library_id
        super().__init__()

class OpenModalRandomRecord(Message):
    def __init__(self, id_table: str):
        self.id_table = id_table
        super().__init__()

class LibrariesRequest(Message):
    pass

class LibrariesResponse(Message):
    def __init__(self, libraries: list[Library]):
        self.libraries = libraries
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

class CloseScreen(Message):
    pass