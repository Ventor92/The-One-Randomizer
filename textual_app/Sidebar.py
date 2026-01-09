from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Vertical, Horizontal
from textual.widgets import Label, Static, Button, TabbedContent, TabPane

from textual.reactive import reactive

from GameService.GameController import GameController, GameTOR
from textual_app.UI.Events.events import RollRequest

class Sidebar(Widget):
    """
    Our sidebar widget.

    Add desired content to compose()

    """

    DEFAULT_CSS = """
    Sidebar {
        /* width: 30; */
        height: 30%;
        /* Needs to go in its own layer to sit above content */
        layer: sidebar; 
        /* Dock the sidebar to the appropriate side */
        dock: top;
        /* Offset x to be -100% to move it out of view by default */
        # offset-x: -100%;
        offset-y: -100%;

        background: $primary;
        border-right: vkey $background;    

        /* Enable animation */
        transition: offset 200ms;
        
        &.-visible {
            /* Set offset.x to 0 to make it visible when class is applied */
            # offset-x: 0;
            offset-y: 0;
        }

        & > Horizontal {
            margin: 1 2;
        }
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("Your sidebar here!")
            # yield Header(show_clock=True)
            # yield Static(f"Biblioteka: {self.library_name}", classes="title")
            yield Static("Kliknij aby wylosować zdarzenie:")
            self.result = Static("", id="dupa")
            # self.result.styles.text_wrap = "wrap"
            self.result.styles.text_overflow = "ellipsis"
            yield self.result
            yield Button("Losuj", id="roll")
            # yield Button("Powrót", id="back")
            # yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "roll":
            self.post_message(RollRequest())