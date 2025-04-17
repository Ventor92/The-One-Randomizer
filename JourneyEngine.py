class State:
    """Base class for all states in the state machine."""
    def __init__(self, name):
        self.name = name

    def on_enter(self):
        """Called when entering the state."""
        pass

    def on_exit(self):
        """Called when exiting the state."""
        pass

    def update(self):
        """Called to update the state logic."""
        pass


class StateMachine:
    """A simple state machine implementation."""
    def __init__(self):
        self.current_state = None

    def change_state(self, new_state):
        """Change the current state to a new state."""
        if self.current_state:
            self.current_state.on_exit()
        self.current_state = new_state
        if self.current_state:
            self.current_state.on_enter()

    def update(self):
        """Update the current state."""
        if self.current_state:
            self.current_state.update()