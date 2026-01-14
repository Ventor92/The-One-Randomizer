import pandas as pd

from DiceService.DiceSet import Dice
from TableService.GenericTableLoader import GenericTableLoader

class GenericTable:
    def __init__(self, path, sheetName, dataFrame: pd.DataFrame, diceMap: dict[str, str]):
        self._name = sheetName
        self._path = path
        self._dataFrame: pd.DataFrame = dataFrame
        
        self._diceMap: dict[str, Dice] = {}

        for key, dieStr in diceMap.items():
            die = self.__strToDie(dieStr)
            if die is not None:
                self._diceMap[key] = die

        print(f"GenericTable __init__")

    def getDataFrame(self) -> pd.DataFrame:
        return self._dataFrame

    def __strToDie(self, dieStr: str) -> Dice | None:
        try:
            die = Dice.fromString(dieStr)
            return die
        except Exception as e:
            print(f"[GenericTable] Error converting string to Die: {e}")
            return None

    def loadRecords(self) -> None:
        self._dataFrame = GenericTableLoader.loadRecords(self._path, self._name)

    def rollRecord(self) -> pd.Series | None:
        if self._dataFrame.empty:
            print(f"[GenericTable] DataFrame is empty, cannot roll record.")
            return None

        roll_results: dict[str, int] = {}
        for column, die in self._diceMap.items():
            roll_results[column] = die.roll(1)[0]
            
        mask = True
        print(f"[GenericTable] Roll results: {roll_results}")
        for col, val in roll_results.items():
            mask &= self._dataFrame[col] == val

        matched_rows = self._dataFrame[mask]
        print(matched_rows)

        if not matched_rows.empty:
            return matched_rows.iloc[0]
        else:
            print(f"[GenericTable] No matching record found for rolls: {roll_results}")
            return None

    