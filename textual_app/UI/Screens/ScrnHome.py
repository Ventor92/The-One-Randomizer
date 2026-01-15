import random
from textual import on
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, ListView, ListItem
from textual.containers import Vertical
from textual.widgets import Label, Tabs, Tab, TabPane, DataTable
from textual import log
from textual.widgets import TabbedContent

from UI.Events.events import Message, LibraryChosen, TableIdsRequest, TableIdsResponse

from rich.table import Table as RichTable




class ScrnHome(Screen):

    __list_library_ids: list[str] = []


    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("Wybierz grę / bibliotekę tabel:", classes="title")
        yield ListView(id="library_list")
        yield Footer()
        self.app.post_message(TableIdsRequest())

    def on_mount(self):
        pass


    def on_list_view_selected(self, event: ListView.Selected):

        selected_id = event.item.id

        if selected_id is not None:
            message: Message = LibraryChosen(selected_id)
        else:
            message: Message = LibraryChosen("The_One_Ring")

        self.post_message(message)
        
    @on(TableIdsResponse)
    def on_table_ids_response(self, message: TableIdsResponse):
        list_view = self.query_one("#library_list", ListView)

        for id, name in message.id_name_map.items():
            list_view.append(ListItem(Static(name), id=id))

        list_view.refresh(layout=True)
        self.log(f"Received table IDs: {message.id_name_map}")