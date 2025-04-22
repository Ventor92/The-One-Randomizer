import pandas as pd
# from Event import Event
from TableService.RecordFactory import RecordFactory, Record
   
class TableLoader:

    @staticmethod
    def loadRecords(classId: int, path: str, sheet_name:str) -> list[Record]:
        table = pd.read_excel(path, sheet_name)
        events = []
        for _, row in table.iterrows():
            e = RecordFactory.create(classId, row)
            events.append(e)
        return events