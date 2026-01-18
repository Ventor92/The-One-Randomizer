import yaml
from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class Table:
    id: str
    sheet_name: str
    path: str
    description: Optional[str] = None
    schema: Optional[dict] = None
    column_dice_map: Optional[dict] = None


@dataclass
class Library:
    id: str
    name: str
    description: Optional[str] = None
    tables: List[Table] = field(default_factory=list)


class TablesLibrariesConfig:
    """Loader/adapter for Tables_Cfg.yaml with separate 'libraries' and 'tables' sections.

    The YAML structure expected:
    - top-level 'libraries': mapping of library_id -> {name, description, tables: {table_id: ...} }
    - top-level 'tables': mapping of table_id -> table definition (path, sheet_name, ...)
    """

    def __init__(self, config_path: str = "Tables_Cfg.yaml"):
        raw = self._load_raw(config_path)
        self._libraries: Dict[str, dict] = raw.get("libraries", {})
        self._tables: Dict[str, dict] = raw.get("tables", {})
        print(f"[TableFactory] Loaded libraries: {list(self._libraries.keys())}; tables: {list(self._tables.keys())}")

    def _load_raw(self, config_path: str) -> dict:
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                return data
        except FileNotFoundError:
            print(f"[TablesLibrariesConfig] Configuration file '{config_path}' not found.")
            return {}
        except yaml.YAMLError as e:
            print(f"[TablesLibrariesConfig] Error parsing YAML file '{config_path}': {e}")
            return {}

    def get_table_config(self, name: str) -> dict | None:
        """Return the table definition from the top-level 'tables' section by id."""
        t = self._tables.get(name)
        if t is None:
            print(f"[TablesConfig] Table '{name}' not found in 'tables' section.")
        return t

    def get_all_table_configs(self) -> list[dict]:
        """Return all table definitions from the top-level 'tables' section."""
        return list(self._tables.values())

    def _find_library(self, identifier: str) -> dict | None:
        # search by key
        if identifier in self._libraries:
            return self._libraries[identifier]
        # search by displayed name
        for lib in self._libraries.values():
            if lib.get("name") == identifier:
                return lib
        return None

    def get_library_names(self) -> list[str]:
        names: list[str] = []
        for key, lib in self._libraries.items():
            names.append(lib.get("name", key))
        return names

    def get_sheet_names(self, library_identifier: str) -> list[str]:
        """Return list of `sheet_name` values for all tables referenced by the library.

        The library's `tables` value may be a mapping (keys are table ids) or a list of table ids.
        """
        lib = self._find_library(library_identifier)
        if lib is None:
            print(f"[TablesConfig] Library '{library_identifier}' not found.")
            return []

        tables_section = lib.get("tables", {})
        # Normalize to a list of table ids
        if isinstance(tables_section, dict):
            table_ids = list(tables_section.keys())
        elif isinstance(tables_section, list):
            table_ids = tables_section
        else:
            table_ids = []

        sheet_names: list[str] = []
        for tid in table_ids:
            tconf = self._tables.get(tid, {}) or {}
            sheet = tconf.get("sheet_name")
            if sheet:
                sheet_names.append(sheet)
        return sheet_names

    def get_libraries(self) -> List[Library]:
        """Convert config into list of `Library` objects with populated `Table` objects.

        Each library's `tables` list may reference table ids defined in the top-level 'tables' section.
        """
        libs: List[Library] = []
        for lib_key, lib_val in self._libraries.items():
            lib_obj = Library(id=lib_key, name=lib_val.get("name", lib_key), description=lib_val.get("description"))

            tables_section = lib_val.get("tables", {})
            if isinstance(tables_section, dict):
                table_ids = list(tables_section.keys())
            elif isinstance(tables_section, list):
                table_ids = tables_section
            else:
                table_ids = []

            for table_key in table_ids:
                table_val = self._tables.get(table_key, {}) or {}
                table_obj = Table(
                    id=table_key,
                    sheet_name=table_val.get("sheet_name", ""),
                    path=table_val.get("path", ""),
                    description=table_val.get("description"),
                    schema=table_val.get("schema"),
                    column_dice_map=table_val.get("column_dice_map"),
                )
                lib_obj.tables.append(table_obj)

            libs.append(lib_obj)
        return libs

    def get_libraries_name_map(self) -> Dict[str, Library]:
        libs = self.get_libraries()
        return {lib.name: lib for lib in libs}

    def get_library_by_id(self, library_id: str) -> Library | None:
        libs = self.get_libraries()
        for lib in libs:
            if lib.id == library_id:
                return lib
        return None