from dataclasses import dataclass

@dataclass
class EventCallOfCthulhu:
    featDieMin: int                  # KOŚĆ DZIAŁANIA
    featDieMax: int                  # KOŚĆ DZIAŁANIA
    event: str                      # ZDARZENIE
    testConsequences: str          # KONSEKWENCJE TESTU
    fatigueGained: int             # OTRZYMANE ZNUŻENIE
    successDie: int                # KOŚĆ SUKCESU
    detailedEvent: str             # ZDARZENIE SZCZEGÓŁOWE
    outcome: str                   # SKUTEK

    def __str__(self):
        return (
            f"CoC Event: {self.event} || Detailed: {self.detailedEvent}\n"
            f"  Test Consequences: {self.testConsequences}\n"
            f"  Outcome: {self.outcome} || Fatigue Gained: {self.fatigueGained}\n"
            f"  Feat Die: ({self.featDieMin}-{self.featDieMax}) Success Die: {self.successDie}\n"
        )

    