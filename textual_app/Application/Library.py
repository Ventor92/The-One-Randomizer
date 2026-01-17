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