import random
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, ListView, ListItem
from textual.containers import Vertical
from textual.widgets import Label, Tabs, Tab, TabPane, DataTable
from textual import log
from textual.widgets import TabbedContent

# from rich.table import Table as RichTable

from GameService.GameController import GameController, GameTOR
from TableService.Table import Table, Record
from textual_app.Application.Srvc_Table import Srvc_Table

from textual.reactive import reactive
from textual_app.Sidebar import Sidebar

from textual_app.UI.Events.events import TableChosen, RollRequest

class ScrnTables(Screen):
    def __init__(self, library_name: str):
        super().__init__()
        self.library_name = library_name
        GameTOR()

    """
    Test app to show our sidebar.
    """

    DEFAULT_CSS = """
    Screen {    
        layers: sidebar;
    }

    """

    BINDINGS = [("s", "toggle_sidebar", "Toggle Sidebar"),
                ("c", "close_screen", "Close Screen")]

    show_sidebar = reactive(False)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield TabbedContent(id="table_tabs")
        yield Sidebar()

        yield Footer()


    def on_mount(self):

        # self.title = "Header Application"
        self.sub_title = self.library_name

        tables = GameTOR().tables

        tabs = self.query_one("#table_tabs", TabbedContent)

        for table in tables:

            name = table.getName()
            recordType = table.getRecordType()
            self.log(name)

            dataTable = Srvc_Table.createDataTable(table)
            
            pane = TabPane(name, id=f"tab-{recordType.__name__}", name=recordType.__name__)
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

    def action_toggle_sidebar(self) -> None:
        """Toggle the sidebar visibility."""
        self.show_sidebar = not self.show_sidebar

    def watch_show_sidebar(self, show_sidebar: bool) -> None:
        """Set or unset visible class when reactive changes."""
        self.query_one(Sidebar).set_class(show_sidebar, "-visible")

    def action_close_screen(self) -> None:
        """Close the screen."""
        self.app.pop_screen()

    def on_roll_request(self, message: RollRequest) -> None:
        tabbed = self.query_one("#table_tabs", TabbedContent)
        active_id = tabbed.active

        if not active_id:
            return

        game = GameTOR()

        active_pane = self.query_one(f"#{active_id}", TabPane)
        self.log(active_pane._title)

        name = active_pane._title._text
        name = name[:-1]

        text = str(game.randomTableV2(name))

        self.query_one("#result", Static).update(text)