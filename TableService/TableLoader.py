import pandas as pd
# from Event import Event
from TableService.Record import Record
   
class TableLoader:

    @staticmethod
    def loadRecords(recordType: type[Record], path: str, sheet_name:str) -> list[Record]:
        table = pd.read_excel(path, sheet_name)
        events = []
        for _, row in table.iterrows():
            e = recordType.fromRow(row)
            events.append(e)
        return events