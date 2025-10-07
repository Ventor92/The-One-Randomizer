import yaml
from pathlib import Path
from typing import Optional, Sequence
from TableService.TableLoader import TableLoaderExcel
from web_app.backend.models.TableRecord import RandomTable
from DiceService.Dice import DiceType

from TheOneRingDetails.EventTheOneRing import EventTheOneRing
from TheOneRingDetails.ThreadTheOneRing import ThreadTOR
from TheOneRingDetails.MissionTOR import MissionTOR

RECORD_TYPES = {
    "event_tor": EventTheOneRing,
    "thread_tor": ThreadTOR,
    "mission_tor": MissionTOR,
}

class TableFactory:
    _config: dict[str, dict] = {}

    @classmethod
    def load_config(cls, config_path: str = "RandomTable_Cfg.yaml"):
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            cls._config = data.get("tables", {})

    @classmethod
    def create(cls, name: str) -> Optional[RandomTable]:
        if not cls._config:
            cls.load_config()

        table_conf = cls._config.get(name)
        if table_conf is None:
            print(f"[TableFactory] Table '{name}' not found in config.")
            return None

        try:
            record_type = RECORD_TYPES[name]
            # record_type = table_conf["record_type"]
            dice_types = [getattr(DiceType, d) for d in table_conf["dice"]]
            loader = TableLoaderExcel(
                recordType=record_type,
                path=table_conf["path"],
                sheet_name=table_conf["sheet_name"]
            )
            return RandomTable(loader, dice_types, table_conf["description"])
        except Exception as e:
            print(f"[TableFactory] Error creating table '{name}': {e}")
            return None

    @classmethod
    def build_all_tables(cls) -> Sequence[RandomTable]:
        if not cls._config:
            cls.load_config()

        tables: list[RandomTable] = []
        for name in cls._config:
            table = cls.create(name)
            if table is not None:
                tables.append(table)
        return tables
