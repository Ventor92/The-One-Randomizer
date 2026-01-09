from textual.app import App, ComposeResult
from textual_app.UI.Screens.ScrnHome import ScrnHome
from textual_app.UI.Screens.ScrnTables import ScrnTables
from textual_app.UI.Events.events import TableChosen


class MGApp(App):
    CSS = """
    .title {
        text-style: bold;
        color: yellow;
        padding: 1;
    }
    """

    def on_mount(self):
        self.push_screen(ScrnHome())

    def on_table_chosen(self, message: TableChosen):
        self.push_screen(ScrnTables(message.table_name))

if __name__ == "__main__":
    MGApp().run()
