


class Character:
    def __init__(self, name: str):
        self.name = name

class CharacterTOR(Character):
    def __init__(self, name: str = "Lord of the Rings"):
        super().__init__(name)
        self.hopePts: int = 0
        self.shadowPts: int = 0
        self.shadowScars: int = 0

class HeroTOR(CharacterTOR):
    def __init__(self, name: str = "Hero of the Ring"):
        super().__init__(name)

from enum import Enum, auto

class InjuryTORType(Enum):
    NONE = auto()
    FLEETING = auto()
    MODERATE = auto()
    SEVERE = auto()
    GRIEVOUS = auto()
    LINGERING = auto()

class FatigueTORType(Enum):
    NONE = auto()
    FATIGUED = auto()
    FALTERING = auto()
    SPENT = auto()
    COLLAPSED = auto()


class AllieTOR():
    def __init__(self, name: str = "Allie form Band"):

        self.active: bool = True
        self.name: str = name
        self.injuries: InjuryTORType = InjuryTORType.NONE
        self.fatigue: FatigueTORType = FatigueTORType.NONE

        self.hardened: bool = False

        self.gift: str = "None"
        self.giftWasted: bool = False

        self.kinglyGift: str = "None"
        self.kinglyGiftWasted: bool = False

        self.quirksOrNotes: str = "None"

    def setInjury(self, injury: InjuryTORType):
        self.injuries = injury

    def setFatigue(self, fatigue: FatigueTORType):
        self.fatigue = fatigue
    
    def setGiftWasted(self, wasted: bool):
        self.giftWasted = wasted
    
    def setKinglyGiftWasted(self, wasted: bool):
        self.kinglyGiftWasted = wasted

    def setHardened(self, hardened: bool):
        self.hardened = hardened

    def setActive(self, active: bool):
        self.active = active


class Armament(Enum):
    NONE = auto()
    LIGHT = auto()
    READY = auto()
    HEAVY = auto()

class BandSizeType(Enum):
    NONE = auto()
    SMALL = 1
    MEDIUM = 4
    LARGE = 9 

class BandFacultyType(Enum):
    NONE = auto()
    WAR = auto()
    EXPERTISE = auto()
    VIGILANCE = auto()

class BandTOR(CharacterTOR):
    def __init__(self, name: str = "Band of the Ring"):
        super().__init__(name)
        self.allies: list[AllieTOR] = []

        self.armament: Armament = Armament.LIGHT
        self.size: BandSizeType = BandSizeType.NONE
        self.faculty: BandFacultyType = BandFacultyType.NONE

        self.eyeAwareness: int = 0
        self.huntThreshold: int = 14

    def addAlly(self, ally: AllieTOR):
        self.allies.append(ally)

    def activateAlly(self, name: str):
        """Activate ally by name."""
        ally = next((ally for ally in self.allies if ally.name == name), None)
        if ally:
            ally.setActive(True)
        else:
            print(f"Ally {name} not found in the band.")
    
    def removeAllyByName(self, name: str):
        """Remove ally by name from the band."""
        ally = next((ally for ally in self.allies if ally.name == name), None)
        if ally:
            self.allies.remove(ally)
        else:
            print(f"Ally {name} not found in the band.")


    def setArmament(self, armament: Armament):
        self.armament = armament

    def setSize(self, size: BandSizeType):
        self.size = size
    
    def setFaculty(self, faculty: BandFacultyType):
        self.faculty = faculty

    def setEyeAwareness(self, eyeAwareness: int):
        self.eyeAwareness = eyeAwareness

    def setHuntThreshold(self, huntThreshold: int):
        self.huntThreshold = huntThreshold

    def updateSize(self):
        """Update size of the band based on the number of active allies."""
        active_allies_count = sum(1 for ally in self.allies if ally.active)
        if active_allies_count <= 4:
            self.size = BandSizeType.SMALL
        elif active_allies_count <= 9:
            self.size = BandSizeType.MEDIUM
        else:
            self.size = BandSizeType.LARGE

    def getVigilance(self) -> int:
        vigilance:int = 2

        match self.faculty:
            case BandFacultyType.VIGILANCE:
                vigilance += 1
            case _:
                vigilance += 0
        return vigilance

    def getExpertise(self) -> int:
        expertise:int = 2

        match self.faculty:
            case BandFacultyType.EXPERTISE:
                expertise += 1
            case _:
                expertise += 0
        return expertise
    
    def getManoeuvre(self) -> int:
        manoeuvre:int = 2

        match self.armament:
            case Armament.NONE:
                manoeuvre += 2
            case Armament.LIGHT:
                manoeuvre += 1
            case Armament.READY:
                manoeuvre += 0
            case Armament.HEAVY:
                manoeuvre += -1

        match self.size:
            case BandSizeType.NONE:
                manoeuvre += 2
            case BandSizeType.SMALL:
                manoeuvre += 1
            case BandSizeType.MEDIUM:
                manoeuvre += 0
            case BandSizeType.LARGE:
                manoeuvre += -1

        return manoeuvre


    def getRally(self) -> int:
        return 2

    def getWar(self) -> int:
        war:int = 2
        
        match self.armament:
            case Armament.NONE:
                war += -2
            case Armament.LIGHT:
                war += -1
            case Armament.READY:
                war += 0
            case Armament.HEAVY:
                war += 1

        match self.size:
            case BandSizeType.NONE:
                war += -2
            case BandSizeType.SMALL:
                war += -1
            case BandSizeType.MEDIUM:
                war += 0
            case BandSizeType.LARGE:
                war += 1

        match self.faculty:
            case BandFacultyType.WAR:
                war += 1
            case BandFacultyType.NONE | BandFacultyType.EXPERTISE | BandFacultyType.VIGILANCE | _:
                war += 0

        return war

