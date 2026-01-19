from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Vertical, Container
from textual.widgets import Label, Static, Button

from UI.Events.events import CloseScreen, OpenModalRandomRecord

class SectionRandom(Widget):

    def compose(self) -> ComposeResult:
        with Container(classes="section"):
            # yield Label("Random Section")
            # yield Static("Kliknij aby wylosować zdarzenie:")
            self.id_table = "random_encounter_table"
            self.result = Static("", id="result")
            
            yield self.result
            self.btn_roll = Button("Roll", id="roll")
            self.btn_back = Button("Back", id="back")
            with Container():
                yield self.btn_roll
                yield self.btn_back

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "roll":
            self.post_message(OpenModalRandomRecord(id_table=self.id_table))

        if event.button.id == "back":
            self.screen.post_message(CloseScreen())