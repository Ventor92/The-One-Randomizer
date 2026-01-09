import random
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, ListView, ListItem
from textual.containers import Vertical
from textual.widgets import Label, Tabs, Tab, TabPane, DataTable
from textual import log
from textual.widgets import TabbedContent

from textual_app.UI.Events.events import Message, TableChosen

from rich.table import Table as RichTable


LIBRARIES = {
    "The_One_Ring": [
        "Znajdujesz starożytny artefakt.",
        "Widzisz cień w oddali.",
        "Wiatr wzbudza dawne przekleństwa.",
        "Zbliża się nieprzyjazny obcy.",
    ],
}


class ScrnHome(Screen):
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
            message: Message = TableChosen(selected_id)
        else:
            message: Message = TableChosen("The_One_Ring")

        self.post_message(message)