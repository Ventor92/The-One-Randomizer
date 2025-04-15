import pandas as pd
from Event import Event
from utils.singleton import singleton

@singleton
class TableEvent:
    def __init__(self, path="data/TableEvent.xlsx", sheet_name="Zdarzenia"):
        table = pd.read_excel(path, sheet_name=sheet_name)
        self.__events = self.__load_events(table)

    def __load_events(self, table) -> list[Event]:
        # Konwersja wierszy na obiekty Event
        events = []
        for _, row in table.iterrows():
            e = Event(
                featDieMin=int(row['featDieMin']),
                featDieMax=int(row['featDieMax']),
                event=row['event'],
                testConsequences=row['testConsequences'],
                fatigueGained=int(row['fatigueGained']),
                successDie=int(row['successDie']),
                detailedEvent=row['detailedEvent'],
                outcome=row['outcome']
            )
            events.append(e)
        return events

    def _findEventsByFeatDie(self, dieFeatValue: int) -> list[Event]:
        """
        Zwraca listę zdarzeń, których zakres featDieMin–featDieMax obejmuje wartość 'value'.
        """
        print(dieFeatValue)
        try:
            if not (1 <= dieFeatValue <= 12):
                raise ValueError("dieFeatValue not in rage <1:12>")
        except ValueError:
            print("Error, default dieFeatValue 1!")
            dieFeatValue = 1

        matching = [event for event in self.__events if event.featDieMin <= dieFeatValue <= event.featDieMax]
        return matching
    
    def _findEventBySuccessDie(self, events: list[Event], successDie: int) -> Event | None:
        """
        Zwraca pierwszy Event z listy, który ma successDie równy podanej wartości.
        """
        for event in events:
            if event.successDie == successDie:
                return event
        return None  # Jeśli nie znaleziono pasującego eventu
    
    def getEvent(self, dieFeatValue: int, dieSuccess: int) -> Event | None:
        print(f"dupa {dieFeatValue}, {dieSuccess}")
        eventsFeat = self._findEventsByFeatDie(dieFeatValue)
        event = self._findEventBySuccessDie(eventsFeat, dieSuccess)
        return event

