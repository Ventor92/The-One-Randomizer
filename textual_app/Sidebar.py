from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Vertical, Horizontal, Container
from textual.widgets import Label, Static, Button, TabbedContent, TabPane

from textual.reactive import reactive

from GameService.GameController import GameController, GameTOR
from textual_app.UI.Events.events import RollRequest

class Sidebar(Widget):

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