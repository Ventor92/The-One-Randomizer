from typing import List
import pandas as pd
from Thread import Thread  # zakładam, że masz klasę Thread w osobnym pliku

class TableThread:
    def __init__(self, path="data/TableEvent.xlsx", sheet_name="Wątki"):
        self.__table = pd.read_excel(path, sheet_name=sheet_name)
        self.__threads = self.__load_threads()

    def __load_threads(self) -> List[Thread]:
        threads = []
        for _, row in self.__table.iterrows():
            thread = Thread(
                dieFeat=int(row["dieFeat"]),
                dieSuccess=int(row["dieSuccess"]),
                action=str(row["action"]),
                aspect=str(row["aspect"]),
                subject=str(row["subject"]),
                motive=str(row["motive"])
            )
            threads.append(thread)

        return threads

    def getAllThreads(self) -> List[Thread]:
        return self.__threads

    def getThreadsByFeat(self, dieFeatValue: int) -> List[Thread]:
        return [t for t in self.__threads if t.dieFeat == dieFeatValue]

    def getThread(self, dieFeatValue: int, dieSuccessValue: int) -> Thread | None:
        for t in self.__threads:
            if t.dieFeat == dieFeatValue and t.dieSuccess == dieSuccessValue:
                return t
        return None