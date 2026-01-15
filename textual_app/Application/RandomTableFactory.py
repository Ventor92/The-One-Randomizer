import pandas as pd
import yaml
from pathlib import Path
from typing import Optional, Sequence
from TableService.GenericTableLoader import GenericTableLoader
from TableService.GenericTable import GenericTable
from web_app.backend.models.TableRecord import RandomTable
from DiceService.Dice import DiceType

class TableFactory:
    _config: dict[str, dict] = {}

    @classmethod
    def load_config(cls, config_path: str = "Table_Cfg.yaml"):
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            cls._config = data.get("tables", {})
            print(f"[TableFactory] Loaded config for tables: {cls._config.keys()}")

    @classmethod
    def create(cls, name: str) -> Optional[GenericTable]:
        if not cls._config:
            cls.load_config()

        table_conf = cls._config.get(name)
        if table_conf is None:
            print(f"[TableFactory] Table '{name}' not found in config.")
            return None

        try:
            column_dice_map = table_conf.get("column_dice_map", {})
            dataFrame = GenericTableLoader.loadRecords(
                path=table_conf["path"],
                sheet_name=table_conf["sheet_name"]
            )

            table = GenericTable(
                path=table_conf["path"],
                sheetName=table_conf["sheet_name"],
                dataFrame=dataFrame,
                diceMap=column_dice_map
            )

            
            return table
        except Exception as e:
            print(f"[TableFactory] Error creating table '{name}': {e}")
            return None

    # @classmethod
    # def build_all_tables(cls) -> Sequence[RandomTable]:
    #     if not cls._config:
    #         cls.load_config()

    #     tables: list[RandomTable] = []
    #     for name in cls._config:
    #         table = cls.create(name)
    #         if table is not None:
    #             tables.append(table)
    #     return tables
