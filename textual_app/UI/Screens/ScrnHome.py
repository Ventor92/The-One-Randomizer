from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Tree

from UI.Events.events import LibraryChosen, LibrariesRequest, LibrariesResponse

class ScrnHome(Screen):

    def compose(self) -> ComposeResult:
        self.header = Header(show_clock=True)
        yield self.header
        yield Static("Wybierz grę / bibliotekę tabel:", classes="title")
        self.tree_view = Tree("Libraries and Tables", id="libraries_tables_tree")
        yield self.tree_view
        yield Footer()
        self.app.post_message(LibrariesRequest())

    def on_mount(self):
        pass

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
        self.log(f"Populated tree with {len(message.libraries)} libraries")
        

