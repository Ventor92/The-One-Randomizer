from textual.message import Message

class TableChosen(Message):
    def __init__(self, table_name: str):
        self.table_name = table_name
        super().__init__()

class RollRequest(Message):
    pass

class GoToMainMenu(Message):
    pass