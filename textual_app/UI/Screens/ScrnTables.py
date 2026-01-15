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
    def __init__(self, library_id: str, library_name: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.library_id = library_id
        self.library_name = library_name
        GameTOR()



    BINDINGS = [("s", "toggle_sidebar_random", "Toggle Sidebar"),
                ("c", "close_screen", "Close Screen")]

    show_sidebar = reactive(False)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, id="header_tables")
        self.sidebar_random = Sidebar(id="sidebar_random")
        self.section_random = SectionRandom(id="section_random")
        with self.sidebar_random:
            yield self.section_random

        with Sidebar(id="sidebar_browser"):
            yield Header()

        yield Header(show_clock=True)
        self.tabbed_content = TabbedContent(id="table_tabs")
        yield self.tabbed_content
        yield Footer()


    def on_mount(self):
        self.title = self.library_name
        self.post_message(TablesRequest(self.library_id))

    def action_close_screen(self) -> None:
        """Close the screen."""
        self.app.pop_screen()

    @on(TabbedContent.TabActivated)
    def tab_activated(self, message: TabbedContent.TabActivated):
        self.log(f"Tab activated: {message.pane._title._text}")
        self.section_random.id_table = f"{message.pane.id}"

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
        tabs = self.tabbed_content

        for table in message.tables:

            pane_name = table.getName()
            pane_id = table.getId()
            dataFrame: pd.DataFrame = table.getDataFrame()

            dataTable = Srvc_Table.df2DataTable(dataFrame)

            pane = TabPane(pane_name, id=pane_id, name=pane_name)
            tabs.add_pane(pane)
            pane.mount(dataTable)

        tabs.refresh(layout=True)