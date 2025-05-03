from Character import Character

class CharacterTOR(Character):
    def __init__(self, name: str = "Lord of the Rings", 
                 hopePts: int = 0,
                 shadowPts: int = 0,
                 shadowScars: int = 0):
        """ Initialize a character with the given name, hope points, shadow points, and shadow scars. """
        super().__init__(name)
        self.hopePts: int = hopePts
        self.shadowPts: int = shadowPts
        self.shadowScars: int = shadowScars

        self.treasureWorth: int = 0

    def getHope(self) -> int:
        return self.hopePts
    
    def setHope(self, hope:int) -> None:
        self.hopePts = hope

    def changeHope(self, hope:int) -> int:
        self.hopePts += hope
        if self.hopePts < 0:
            self.hopePts = 0
        return self.hopePts
    
    def isCaring(self) -> bool:
        """Check if the character is caring."""
        if self.treasureWorth > 0:
            return True
        else:
            return False