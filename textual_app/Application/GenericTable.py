import ast
import pandas as pd

from Application.DiceService.DiceSet import Dice
from Application.GenericTableLoader import GenericTableLoader

class GenericTable:
    def __init__(self, path, sheetName, id: str, dataFrame: pd.DataFrame, diceMap: dict[str, str]):
        self._id = id
        self._name = sheetName
        self._path = path
        self._dataFrame: pd.DataFrame = dataFrame
        
        self._diceMap: dict[str, Dice] = {}

        for key, dieStr in diceMap.items():
            die = self.__strToDie(dieStr)
            if die is not None:
                self._diceMap[key] = die

        print(f"GenericTable __init__")

    def __strToDie(self, dieStr: str) -> Dice | None:
        try:
            die = Dice.fromString(dieStr)
            return die
        except Exception as e:
            print(f"[GenericTable] Error converting string to Die: {e}")
            return None

    def loadRecords(self) -> None:
        self._dataFrame = GenericTableLoader.loadRecords(self._path, self._name)

    @staticmethod
    def parse_cell(x):
        try:
            if x is None or str(x).strip() == "":
                return []

            x = str(x).strip()

            try:
                return list(map(int, ast.literal_eval(x)))
            except:
                x = x.replace(";", ",")
                return [int(v) for v in x.split(",") if v]
        except Exception as e:
            print(f"Błąd w komórce: {x} -> {e}")
            return []

    @staticmethod
    def filter_rows_by_column_values(df, column_values):
        mask = pd.Series(True, index=df.index)  # zaczynamy od wszystkiego True

        for col, value in column_values.items():
            # upewniamy się, że kolumna istnieje
            if col not in df.columns:
                raise ValueError(f"Kolumna {col} nie istnieje w DataFrame")
            mask &= df[col].apply(lambda lst: value in lst)

        return df[mask]


    def rollRecord(self) -> pd.Series | None:
        if self._dataFrame.empty:
            print(f"[GenericTable] DataFrame is empty, cannot roll record.")
            return None

        roll_results: dict[str, int] = {}
        for column, die in self._diceMap.items():
            roll_results[column] = die.roll(1)[0]

        tmp_df = self._dataFrame.copy()
        for col, val in roll_results.items():
            tmp_df[col] = tmp_df[col].apply(self.parse_cell)
            tmp_df = self.filter_rows_by_column_values(tmp_df, {col: val})
            print(f"[GenericTable] Parsed column '{col}' and val: {val}:")
            print(tmp_df[col])

        matched_rows = tmp_df
        print(matched_rows)

        if not matched_rows.empty:
            return matched_rows.iloc[0]
        else:
            print(f"[GenericTable] No matching record found for rolls: {roll_results}")
            return None
        
    def getName(self) -> str:
        return self._name

    def getDataFrame(self) -> pd.DataFrame:
        return self._dataFrame
    
    def getId(self) -> str:
        return self._id