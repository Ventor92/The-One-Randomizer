from dataclasses import dataclass, field
from typing import Optional, List


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

    def get_lib_by_id(self, library_id: str) -> Optional['Library']:
        if self.id == library_id:
            return self
        return None
    
    def get_table_by_id(self, table_id: str) -> Optional[Table]:

        for table in self.tables:
            if table.id == table_id:
                return table
        return None