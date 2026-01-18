from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Tree

from UI.Events.events import LibraryChosen, LibrariesRequest, LibrariesResponse
from Application.Library import Library

from Sidebar import Sidebar


class ScrnHome(Screen):

    BINDINGS = [("s", "toggle_sidebar_parameters", "Toggle Sidebar"),
                ("c", "close_screen", "Close Screen")]
        
    def compose(self) -> ComposeResult:
        self.libraries: list[Library] = []
        self.header = Header(show_clock=True)
        yield self.header
        self.sidebar_parameters = Sidebar(id="sidebar_parameters")
        self.label_table_description = Label("Description goes here", id="label_table_description")
        
        with self.sidebar_parameters:
            yield self.label_table_description

        yield Static("Wybierz grę / bibliotekę tabel:", classes="title")
        self.tree_view = Tree("Libraries and Tables", id="libraries_tables_tree")
        yield self.tree_view
        yield Footer()
        self.app.post_message(LibrariesRequest())

    def on_mount(self):
        pass

    @on(Tree.NodeHighlighted)       
    def on_tree_node_highlighted(self, message: Tree.NodeHighlighted):
        node_data = message.node.data
        if node_data is None:
            return
        description = "No description available."
        if "library_id" in node_data:
            library_id = node_data["library_id"]
            self.log(f"Highlighted library node with ID: {library_id}")
        elif "table_id" in node_data:
            table_id = node_data["table_id"]
            self.log(f"Highlighted table node with ID: {table_id}")
            for lib in self.libraries:
                print(f"Searching in library: {lib.name} (ID: {lib.id})")
                table = lib.get_table_by_id(table_id)
                if table is not None:
                    description = table.description if table.description else "No description available."
                    break

        self.label_table_description.update(f"Table Description:\n{description}")
        self.label_table_description.refresh(layout=True)

    def action_toggle_sidebar_parameters(self):
        """Pokazuje / chowa Sidebar Parameters"""
        if "-visible" in self.sidebar_parameters.classes:
            self.sidebar_parameters.remove_class("-visible")
        else:
            self.sidebar_parameters.add_class("-visible")

        self.sidebar_parameters.refresh(layout=True)
    
    @on(Tree.NodeSelected)
    def on_tree_node_selected(self, message: Tree.NodeSelected):
        node_data = message.node.data
        if node_data is None:
            return

        if "library_id" in node_data:
            library_id = node_data["library_id"]
            if library_id is not None:
                self.post_message(LibraryChosen(library_id))
            else:
                raise ValueError("Library ID is None in selected tree node.")
            self.log("Selected tree node is not a library.")
        
    @on(LibrariesResponse)
    def on_libraries_response(self, message: LibrariesResponse):
        self.log(f"Received libraries: {[lib.name for lib in message.libraries]}")
        tree_view = self.query_one("#libraries_tables_tree", Tree)

        # Clear existing nodes and populate with libraries -> tables
        tree_view.clear()
        root = tree_view.root

        for lib in message.libraries:
            lib_label = lib.name or lib.id
            lib_node = root.add(lib_label, data={"library_id": lib.id})
            # Add tables as children
            for table in getattr(lib, "tables", []):
                table_label = table.sheet_name or table.id
                lib_node.add_leaf(table_label, data={"table_id": table.id})

        tree_view.refresh(layout=True)
        self.libraries = message.libraries
        self.log(f"Populated tree with {len(message.libraries)} libraries")
        

