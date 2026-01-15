
from textual.widget import Widget

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