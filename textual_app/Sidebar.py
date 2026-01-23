
from textual.widget import Widget

class Sidebar(Widget):

    DEFAULT_CSS = """
    Sidebar {
        /* Start hidden by using zero width so it participates in layout */
        width: 0;
        min-width: 0;
        height: 100%;
        /* Do not use a separate layer so the sidebar pushes content */
        /* Dock the sidebar to the left side so it affects layout */
        dock: left;
        overflow: hidden;

        /* Animate width so the main content is pushed */
        transition: width 200ms;
        
        &.-visible {
            /* Expand to visible width */
            width: 22;
        }

        & > Horizontal {
            margin: 1 2;
        }
    }
    """