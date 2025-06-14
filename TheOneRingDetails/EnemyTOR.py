class EnemyTOR:
    def __init__(self, mighty: int, resistance: int):
        self.mighty = mighty
        self.resistance = resistance

    def __repr__(self):
        return f"Enemy(mighty={self.mighty}, resistance={self.resistance})"
    
    def addResistance(self, value: int) -> None:
        self.resistance += value
        if self.resistance < 0:
            self.resistance = 0

    def getMighty(self) -> int:
        return self.mighty