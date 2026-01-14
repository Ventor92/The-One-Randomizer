from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Vertical, Horizontal
from textual.widgets import Label, Static, Button, TabbedContent, TabPane

from textual.reactive import reactive

from GameService.GameController import GameController, GameTOR
from textual_app.UI.Events.events import RollRequest, OpenModalRandomRecord

class SectionRandom(Widget):

    def compose(self) -> ComposeResult:
        with Vertical(classes="section"):
            yield Label("Random Section")
            yield Static("Kliknij aby wylosować zdarzenie:")
            self.id_table = "random_encounter_table"
            self.result = Static("", id="result")
            
            yield self.result

            yield Button("Losuj", id="roll")
            yield Button("Powrót", id="back")
    

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "roll":
            self.post_message(OpenModalRandomRecord(id_table=self.id_table))

        if event.button.id == "back":
            pass


    