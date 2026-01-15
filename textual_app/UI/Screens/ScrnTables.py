import random
import pandas as pd

from textual import on
from textual.app import App, ComposeResult
from textual.screen import Screen, ModalScreen
from textual.widgets import Header, Footer, Button, Static, ListView, ListItem
from textual.containers import Vertical, Container
from textual.widgets import Label, Tabs, Tab, TabPane, DataTable
from textual import log
from textual.widgets import TabbedContent


# from rich.table import Table as RichTable

from GameService.GameController import GameController, GameTOR
from TableService.Table import Table, Record
from textual_app.Application.Srvc_Table import Srvc_Table
from textual_app.UI.Wigets.MScrnRecord import MScrnRecord

from textual.reactive import reactive
from textual_app.Sidebar import Sidebar
from textual_app.SectionRandom import SectionRandom

from textual_app.UI.Events.events import LibraryChosen, RollRequest, TablesResponse, TablesRequest

class ScrnTables(Screen):
    def __init__(self, library_id: str):
        super().__init__()
        self.library_id = library_id
        GameTOR()



    BINDINGS = [("s", "toggle_sidebar_random", "Toggle Sidebar"),
                ("c", "close_screen", "Close Screen")]

    show_sidebar = reactive(False)

    def compose(self) -> ComposeResult:
        self.sidebar_random = Sidebar(id="sidebar_random")
        with self.sidebar_random:
            yield SectionRandom(id="section_random")

        with Sidebar(id="sidebar_browser"):
            yield Header()

        yield Header(show_clock=True)
        self.tabbed_content = TabbedContent(id="table_tabs")
        yield self.tabbed_content
        yield Footer()


    def on_mount(self):
        self.post_message(TablesRequest(self.library_id))

    def action_close_screen(self) -> None:
        """Close the screen."""
        self.app.pop_screen()

    @on(TabbedContent.TabActivated)
    def tab_activated(self, message: TabbedContent.TabActivated):
        self.log(f"Tab activated: {message.pane._title._text}")
        secRand = self.query_one("#section_random", SectionRandom)
        secRand.id_table = f"{message.pane.id}"

    def action_toggle_sidebar_random(self):
        """Pokazuje / chowa Sidebar Random"""
        if "-visible" in self.sidebar_random.classes:
            self.sidebar_random.remove_class("-visible")
        else:
            self.sidebar_random.add_class("-visible")

        self.sidebar_random.refresh(layout=True)

    @on(TablesResponse)
    def tables_response(self, message: TablesResponse):
        self.log(f"TablesResponse received in ScrnTables: {message.tables}")
        tabs = self.query_one("#table_tabs", TabbedContent)

        for table in message.tables:

            name = table.getName()
            id = table.getId()
            dataFrame: pd.DataFrame = table.getDataFrame()

            dataTable = Srvc_Table.df2DataTable(dataFrame)

            pane = TabPane(name, id=id, name=name)
            tabs.add_pane(pane)
            pane.mount(dataTable)

        tabs.refresh(layout=True)