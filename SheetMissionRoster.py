import pandas as pd
from MissionRosterBand import MissionRosterBand

class SheetMissionRoster:
    def __init__(self, filepath: str="data/MissionRosters.xlsx", sheetName: str ="MissionRoster"):
        self.filepath = filepath
        self.sheet_name = sheetName
        self.__table = pd.read_excel(filepath, sheet_name=sheetName)
        # print(self.__table)
        self.__missionRosters: list[MissionRosterBand] = self.__load()

    def __load(self) -> list[MissionRosterBand]:
        if self.__table.empty:
            raise ValueError("Plik jest pusty lub nie zawiera żadnych danych.")

        missionRosters: list[MissionRosterBand] = []

        for _, row in self.__table.iterrows():
            mr = MissionRosterBand(
                readiness=row.get('readiness', 4),
                rally=row.get('rally', 2),
                war=row.get('war', 2),
                expertise=row.get('expertise', 2),
                manoeuvre=row.get('manoeuvre', 2),
                vigilance=row.get('vigilance', 2),
                hope=row.get('hope', 15)
            )
            missionRosters.append(mr)

        return missionRosters

    def getMissionRosters(self) -> list[MissionRosterBand]:
        if not self.__missionRosters:
            raise RuntimeError("Nie załadowano danych. Użyj metody `load()`.")
        return self.__missionRosters