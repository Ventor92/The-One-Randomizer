from textual import on
from textual.app import App, ComposeResult
from textual_app.UI.Screens.ScrnHome import ScrnHome
from textual_app.UI.Screens.ScrnTables import ScrnTables
from textual_app.UI.Events.events import OpenModalRandomRecord, TableChosen

from textual_app.UI.Events.events import RollRequest, UpdateModalLabel
from textual_app.UI.Wigets.MScrnRecord import MScrnRecord

from GameService.GameController import GameController, GameTOR


class MGApp(App):

    CSS_PATH = "textual_app/textual_app.tcss"

    def on_mount(self):
        self.push_screen(ScrnHome())

    def on_table_chosen(self, message: TableChosen):
        self.push_screen(ScrnTables(message.table_name))

    @on(OpenModalRandomRecord)
    def open_modal_random_record(self, message: OpenModalRandomRecord):
        self.push_screen(MScrnRecord(id="record_screen", encounter="Re-Roll!", id_table=message.id_table))

    @on(RollRequest)
    def roll_request(self, message: RollRequest) -> None:
        self.log("RollRequest received in MGApp")

        game = GameTOR()

        idTableRecord = message.id_table[:-1]
        text = str(game.randomTableV2(idTableRecord))
        self.log(self.app.screen)

        self.screen.post_message(UpdateModalLabel(text))
        
        self.log("RollRequest processing completed in ScrnTables")


if __name__ == "__main__":
    MGApp().run()
