import yaml
from dataclasses import dataclass, field
from typing import List, Optional


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
    def __init__(self, config_path: str = "textual_app/Table_CfgV2.yaml"):
        self._config: dict = self._load_config(config_path)
        print(f"[TableFactory] Loaded config for libraries: {list(self._config.keys())}")

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            # Cała sekcja 'libraries' z pliku YAML
            libraries = data.get("libraries", {})
            return libraries


    def get_table_config(self, name: str) -> dict | None:
        # Szuka tabeli o podanej nazwie w każdej bibliotece
        for lib_key, lib_val in self._config.items():
            tables = lib_val.get("tables", {})
            if name in tables:
                return tables[name]
        print(f"[TablesConfig] Table '{name}' not found in any library.")
        return None

    def get_all_table_configs(self) -> list[dict]:
        # Zwraca listę wszystkich tabel ze wszystkich bibliotek
        all_tables = []
        for lib_val in self._config.values():
            tables = lib_val.get("tables", {})
            all_tables.extend(tables.values())
        return all_tables

    def _find_library(self, identifier: str) -> dict | None:
        # Szuka biblioteki po kluczu (np. 'tables_tor') lub po polu 'name'
        if identifier in self._config:
            return self._config[identifier]
        for lib in self._config.values():
            if lib.get("name") == identifier:
                return lib
        return None

    def get_library_names(self) -> list[str]:
        # Zwraca listę wyświetlanych nazw bibliotek (pole 'name'),
        # jeśli brak pola 'name' zwraca klucz biblioteki
        names: list[str] = []
        for key, lib in self._config.items():
            names.append(lib.get("name", key))
        return names

    def get_sheet_names(self, library_identifier: str) -> list[str]:
        """Zwraca listę wartości `sheet_name` dla wszystkich tabel w podanej bibliotece.

        `library_identifier` może być kluczem biblioteki (np. 'tables_tor') lub jej polem 'name'.
        """
        lib = self._find_library(library_identifier)
        if lib is None:
            print(f"[TablesConfig] Library '{library_identifier}' not found.")
            return []
        tables = lib.get("tables", {})
        sheet_names: list[str] = []
        for tconf in tables.values():
            sheet = tconf.get("sheet_name")
            if sheet:
                sheet_names.append(sheet)
        return sheet_names

    def get_libraries(self) -> List[Library]:
        """Convert internal config into a list of `Library` objects.

        Each `Library` contains `Table` objects built from the library's `tables` section.
        """
        libs: List[Library] = []
        for lib_key, lib_val in self._config.items():
            lib_obj = Library(id=lib_key, name=lib_val.get("name", lib_key), description=lib_val.get("description"))
            tables_cfg = lib_val.get("tables", {})
            for table_key, table_val in tables_cfg.items():
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
    
    def get_libraries_name_map(self) -> dict[str, Library]:
        """Zwraca słownik mapujący nazwy bibliotek na obiekty `Library`."""
        libs = self.get_libraries()
        return {lib.name: lib for lib in libs}
    
    def get_library_by_id(self, library_id: str) -> Library | None:
        libs = self.get_libraries()
        for lib in libs:
            if lib.id == library_id:
                return lib
        return None