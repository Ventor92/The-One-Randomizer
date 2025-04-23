from dataclasses import dataclass


class Character:
    def __init__(self, name: str):
        self.name = name

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

@dataclass
class AllieTOR():
    id: int = 0
    idBand: int = 0

    active: bool = True
    name: str = "Ally of the Ring"
    injuries: InjuryTORType = InjuryTORType.NONE
    fatigue: FatigueTORType = FatigueTORType.NONE

    hardened: bool = False

    gift: str = "None"
    giftWasted: bool = False

    kinglyGift: str = "None"
    kinglyGiftWasted: bool = False

    quirksOrNotes: str = "None"

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


class BandArmamentType(Enum):
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

class BandDispositionType(Enum):
    NONE = auto()
    WAR = auto()
    EXPERTISE = auto()
    VIGILANCE = auto()
    RALLY = auto()
    MANOEUVRE = auto()

class BandBurdenType(Enum):
    LIGHT = auto()
    MEDIUM = auto()
    HEAVY = auto()
    OVERBURDENED = auto()

@dataclass
class BandTOR(CharacterTOR):
    def __init__(self, id:int, 
                 name: str = "Band of the Ring", 
                 armament: BandArmamentType = BandArmamentType.READY,
                 size: BandSizeType = BandSizeType.MEDIUM,
                 faculty: BandFacultyType = BandFacultyType.NONE,
                 eyeAwareness: int = 0,
                 huntThreshold: int = 14,
                 hopePts: int = 10,
                 shadowPts: int = 0,
                 shadowScars: int = 0):
        super().__init__(name)
        self.id: int = id
        self.allies: list[AllieTOR] = []

        self.armament: BandArmamentType = armament
        self.size: BandSizeType = size
        self.faculty: BandFacultyType = faculty

        self.eyeAwareness: int = eyeAwareness
        self.huntThreshold: int = huntThreshold


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

    def __calculateReadiness(self) -> int:
        """Calculate readiness based on the number of hardened active allies."""
        hardenedAlliesCount = sum(1 for ally in self.allies if ally.active and ally.hardened)
        return hardenedAlliesCount + 4 
    
    def getTargetNumber(self) -> int:
        targetNumber = 20 - self.__calculateReadiness()
        return targetNumber

    def setArmament(self, armament: BandArmamentType):
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

    def isCaring(self) -> bool:
        """Check if the band is caring."""
        if self.treasureWorth > 0:
            return True
        else:
            return False

    def getBurden(self) -> BandBurdenType:
        """Calculate burden based on Armament."""
        burden: BandBurdenType = BandBurdenType.LIGHT
        match self.armament:
            case BandArmamentType.READY:
                burden = BandBurdenType.MEDIUM
            case BandArmamentType.HEAVY:
                burden = BandBurdenType.HEAVY
            case BandArmamentType.NONE | BandArmamentType.LIGHT | _:
                burden = BandBurdenType.LIGHT
        
        if self.isCaring():
            match burden:
                case BandBurdenType.LIGHT:
                    burden = BandBurdenType.MEDIUM
                case BandBurdenType.MEDIUM:
                    burden = BandBurdenType.HEAVY
                case BandBurdenType.HEAVY:
                    burden = BandBurdenType.OVERBURDENED
        
        return burden

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
            case BandArmamentType.NONE:
                manoeuvre += 2
            case BandArmamentType.LIGHT:
                manoeuvre += 1
            case BandArmamentType.READY:
                manoeuvre += 0
            case BandArmamentType.HEAVY:
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
            case BandArmamentType.NONE:
                war += -2
            case BandArmamentType.LIGHT:
                war += -1
            case BandArmamentType.READY:
                war += 0
            case BandArmamentType.HEAVY:
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
    
    def getDispositionLevel(self, disposition: BandDispositionType) -> int:
        levelDisposition:int = 0
        match disposition:
            case BandDispositionType.WAR:
                levelDisposition = self.getWar()
            case BandDispositionType.EXPERTISE:
                levelDisposition = self.getExpertise()
            case BandDispositionType.VIGILANCE:
                levelDisposition = self.getVigilance()
            case BandDispositionType.MANOEUVRE:
                levelDisposition = self.getManoeuvre()
            case BandDispositionType.RALLY:
                levelDisposition = self.getRally()
            case _:
                levelDisposition = 0
        return levelDisposition
    
    def isMiserable(self) -> bool:
        if self.hopePts <= self.shadowPts:
            return True
        else:
            return False 
        
    def __str__(self) -> str:
        """Return a string representation of the band."""
        allies_info = "\n".join(
            f"  - {ally.name} (Active: {ally.active}, Hardened: {ally.hardened})"
            for ally in self.allies
        )
        return (
            f"Name: {self.name} (Band ID {self.id})\n"
            f"Armament: {self.armament.name} Size: {self.size.name} Faculty: {self.faculty.name}\n"
            f"Eye Awareness: {self.eyeAwareness} Hunt Threshold: {self.huntThreshold}\n"
            f"Hope Points: {self.hopePts} Shadow Points: {self.shadowPts} Shadow Scars: {self.shadowScars}\n"
            f"Conditions: Weary: TODO Miserable: {self.isMiserable()}\n"
            f"Disposition Levels:\n"
            f"  - W: {self.getWar()} R: {self.getRally()} E: {self.getExpertise()} M: {self.getManoeuvre()} V: {self.getVigilance()}\n"
            f"Allies ({len(self.allies)}):\n{allies_info}"
        )

