from email.mime import message
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

from UI.Events.events import CloseScreen, OpenModalRandomRecord, RollRequest, RollRequestV2, RollResponseV2, TablesResponse, TablesRequest

class ScrnTables(Screen):
    def __init__(self, library_id: str, library_name: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.library_id = library_id
        self.library_name = library_name


    BINDINGS = [("s", "toggle_sidebar_random", "Toggle Sidebar"),
                ("c", "close_screen", "Close Screen"),
                ("ctrl+r", "alt_roll", "Alt Roll"),
                ("r", "roll", "Roll")]

    show_sidebar = reactive(False)

    def compose(self) -> ComposeResult:
        self.label_lib = Label(f"Library: {self.library_name}", id="label_library_name")
        yield self.label_lib
        self.label_result = Label("Result:", id="label_result")
        yield self.label_result
        self.sidebar_random = Sidebar(id="sidebar_random")
        self.section_random = SectionRandom(id="section_random")
        with self.sidebar_random:
            yield self.section_random

        with Sidebar(id="sidebar_browser"):
            yield Header()

        yield Header(show_clock=True)
        self.dataTable = DataTable()

        yield self.dataTable
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

    def action_alt_roll(self):
        self.post_message(RollRequestV2(id_table=self.section_random.id_table))

    @on(RollResponseV2)
    def roll_response_v2(self, message: RollResponseV2):
        self.dataTable.clear(columns=False)
        self.dataTable.add_row(*message.values)

    @on(TabbedContent.TabActivated)
    def tab_activated(self, message: TabbedContent.TabActivated):
        self.dataTable.clear()
        pane_title = getattr(message.pane, "title", str(message.pane.id))
        self.log(f"Tab activated: {pane_title}")
        self.section_random.id_table = f"{message.pane.id}"


        pane = self.tabbed_content.get_pane(f"{message.pane.id}")
        dataTable = pane.query_one(DataTable)

        columns = dataTable.columns.values()
        labels_columns = [col.label for col in columns]
        self.log(f"labels_columns: {labels_columns}")
        self.dataTable.add_columns(*labels_columns)

    def action_toggle_sidebar_random(self):
        """Shows / hides Sidebar Random"""
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
