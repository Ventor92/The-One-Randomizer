from textual.message import Message

class TableChosen(Message):
    def __init__(self, table_name: str):
        self.table_name = table_name
        super().__init__()

class OpenModalRandomRecord(Message):
    def __init__(self, id_table: str):
        self.id_table = id_table
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