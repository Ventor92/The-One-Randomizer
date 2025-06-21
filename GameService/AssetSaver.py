from TableService.Record import Record
from TableService.RecordFactory import RecordFactory
import pandas as pd
from collections.abc import Sequence

class RecordSaver:
    
    @staticmethod
    def loadRecords(recordType: type[Record], path: str, sheet_name:str) -> list[Record]:
        table = pd.read_excel(path, sheet_name)
        record = []
        for _, row in table.iterrows():
            e = RecordFactory.create(recordType, row)
            record.append(e)
        return record

    @staticmethod
    def saveRecords(records: Sequence[Record], path: str, sheet_name:str) -> None:
        """Save records to a specified path and sheet name."""

        df = pd.read_excel(path, sheet_name, index_col=0)
        print(df)

        rows = list(map(lambda record: record.toRow(), records))

        dfAdditional = pd.DataFrame(rows)
        dfMerged = pd.concat([df, dfAdditional], ignore_index=True)
        dfUnique = dfMerged.drop_duplicates(subset=['id']) 
        print(dfUnique)

        dfUnique.to_excel(path, sheet_name=sheet_name, index=True)
        # Implement saving logic here
        pass
