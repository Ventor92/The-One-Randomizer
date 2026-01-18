from textual import on
from textual.app import App
from textual.containers import Container, Grid, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Placeholder, Footer
from textual.message import Message

from UI.Events.events import RollRequest, UpdateModalLabel

class MScrnRecord(ModalScreen):
    def __init__(self, encounter: str, id_table: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.encounter = encounter
        self.id_table = id_table
        print(f"MScrnRecord __init__ with encounter: {encounter}, id_table: {id_table}")

    BINDINGS = [("c", "close_screen", "Close Screen"),
                ("r", "roll", "Roll")]

    def compose(self):
        with Container():
            self.encounter_label = Label(id="encounter_label", content=self.encounter)
            yield self.encounter_label
            self.question_label = Label(id="question_label", content="Re-roll?")
            yield self.question_label
            with Horizontal():
                yield Button.success("Yes", id="yes")
                yield Button.error("No", id="no")
            yield Footer()

    def action_roll(self):
        self.post_message(RollRequest(id_table=self.id_table))

    def action_close_screen(self):
        self.app.pop_screen()

    @on(Button.Pressed)
    def button_pressed(self, event):
        button_id = event.button.id
        idRecordTable = self.id_table
        if button_id in ("yes"):
            self.post_message(RollRequest(id_table=idRecordTable))
        elif button_id in ("no"):
            self.app.pop_screen()
    
    @on(UpdateModalLabel)
    def update_label(self, message: UpdateModalLabel):
        self.encounter_label.update(message.text)
        self.encounter_label.refresh(layout=True)
