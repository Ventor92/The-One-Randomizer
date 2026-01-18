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
from textual.reactive import reactive


# from rich.table import Table as RichTable

from Application.Srvc_Table import Srvc_Table
from UI.Wigets.MScrnRecord import MScrnRecord

from Sidebar import Sidebar
from SectionRandom import SectionRandom

from UI.Events.events import CloseScreen, LibraryChosen, OpenModalRandomRecord, RollRequest, TablesResponse, TablesRequest, ToggleSidebar

class ScrnTables(Screen):
    def __init__(self, library_id: str, library_name: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.library_id = library_id
        self.library_name = library_name


    BINDINGS = [("s", "toggle_sidebar_random", "Toggle Sidebar"),
                ("c", "close_screen", "Close Screen"),
                ("r", "roll", "Roll")]

    show_sidebar = reactive(False)

    def compose(self) -> ComposeResult:
        self.label = Label(f"Biblioteka: {self.library_name}", id="label_library_name")
        yield self.label
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
        self.__toggle_loading(True)
        self.post_message(TablesRequest(self.library_id))

    def __toggle_loading(self, loading: bool):
        self.tabbed_content.loading = loading

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

    def action_roll(self):
        table_id = self.section_random.id_table
        self.post_message(OpenModalRandomRecord(id_table=table_id))
        self.post_message(RollRequest(id_table=table_id))

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

        self.__toggle_loading(False)
        tabs.refresh(layout=True)
    
    @on(CloseScreen)
    def close_screen(self, message: CloseScreen):
        self.action_close_screen()
