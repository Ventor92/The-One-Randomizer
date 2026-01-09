import random
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, ListView, ListItem
from textual.containers import Vertical
from textual.widgets import Label, Tabs, Tab, TabPane, DataTable
from textual import log
from textual.widgets import TabbedContent

from rich.table import Table as RichTable


LIBRARIES = {
    "The_One_Ring": [
        "Znajdujesz starożytny artefakt.",
        "Widzisz cień w oddali.",
        "Wiatr wzbudza dawne przekleństwa.",
        "Zbliża się nieprzyjazny obcy.",
    ],
}


class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("Wybierz grę / bibliotekę tabel:", classes="title")
        yield ListView(id="library_list")
        yield Footer()

    def on_mount(self):
        list_view = self.query_one("#library_list", ListView)

        for name in LIBRARIES.keys():
            list_view.append(ListItem(Static(name), id=name))

    def on_list_view_selected(self, event: ListView.Selected):

        selected_id = event.item.id

        if selected_id is not None:
            self.app.push_screen(RollScreen(selected_id))
        else:
            self.app.push_screen(RollScreen("Pulp_Cthulhu"))

from GameService.GameController import GameController, GameTOR
from TableService.Record import Record

class RollScreen(Screen):
    def __init__(self, library_name: str):
        super().__init__()
        self.library_name = library_name
        GameTOR()
        self.events = LIBRARIES[library_name]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        # TabbedContent automatycznie tworzy Tabs + TabPane
        yield TabbedContent(id="table_tabs")
        # self.tabs = TabbedContent()
        # yield self.tabs
        yield Footer()


    def on_mount(self):

        # self.title = "Header Application"
        self.sub_title = self.library_name

        tables = GameTOR().tables

        tabs = self.query_one("#table_tabs", TabbedContent)

        for table in tables:

            name = table.getName()
            typeRecord = table.getRecordType()

            listRecords: list[Record] = table.getAllRecords()

            dataTable = DataTable()
            columns = list(listRecords[0].toRawDict().keys())
            dataTable.add_columns(*columns)

            for event in listRecords:
                row = list(event.toRawDict().values())
                dataTable.add_row(*row)
            
            pane = TabPane(name, id=f"tab-{name}")
            tabs.add_pane(pane)
            pane.mount(dataTable)


        # yield Header(show_clock=True)
        # yield Static(f"Biblioteka: {self.library_name}", classes="title")
        # yield Static("Kliknij aby wylosować zdarzenie:")
        # self.result = Static("", id="result")
        # yield self.result
        # yield Button("Losuj", id="roll")
        # yield Button("Powrót", id="back")
        # yield Footer()

    # def on_button_pressed(self, event: Button.Pressed):
    #     if event.button.id == "roll":
    #         self.result.update(random.choice(self.events))
    #     elif event.button.id == "back":
    #         self.app.pop_screen()


class MGApp(App):
    CSS = """
    .title {
        text-style: bold;
        color: yellow;
        padding: 1;
    }

    #result {
        height: 5;
        border: solid green;
        padding: 1;
        text-style: bold;
    }
    """

    def on_mount(self):
        self.push_screen(HomeScreen())


if __name__ == "__main__":
    MGApp().run()
