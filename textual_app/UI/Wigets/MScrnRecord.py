from textual import on
from textual.app import App
from textual.containers import Container, Grid, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Placeholder
from textual.message import Message

from textual_app.UI.Events.events import RollRequest, UpdateModalLabel

class MScrnRecord(ModalScreen):
    def __init__(self, encounter: str, id_table: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.encounter = encounter
        self.id_table = id_table
        print(f"MScrnRecord __init__ with encounter: {encounter}, id_table: {id_table}")

    def compose(self):
        with Container():
            self.encounter_label = Label(id="encounter_label", content=self.encounter)
            yield self.encounter_label
            yield Label("Re-roll?")
            with Horizontal():
                yield Button.success("Yes", id="yes")
                yield Button.error("No", id="no")

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
