from dataclasses import dataclass

@dataclass
class Thread:
    dieFeat: int       # wynik z kości działania
    dieSuccess: int    # wynik z kości sukcesu
    action: str        # działanie, które wykonuje postać
    aspect: str        # aspekt sytuacji lub sceny
    subject: str       # podmiot zdarzenia
    motive: str        # motyw lub cel działania

    def __str__(self):
        return (
            f"Thread:\n"
            f"  Feat Die: {self.dieFeat} Success Die: {self.dieSuccess}\n"
            f"  Action: {self.action} Aspect: {self.aspect} Subject: {self.subject} Motive: {self.motive}"
        )