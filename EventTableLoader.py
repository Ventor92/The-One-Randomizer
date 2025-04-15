import pandas as pd
from Event import Event
from EventFactory import EventFactory

class EventTableLoader:

    @staticmethod
    def loadEvents(eventClassId: int, path="data/TableEvent.xlsx", sheet_name="Zdarzenia") -> list[Event]:
        table = pd.read_excel(path, sheet_name=sheet_name)
        events = []
        for _, row in table.iterrows():
            e = EventFactory.create(eventClassId, row)
            events.append(e)
        return events