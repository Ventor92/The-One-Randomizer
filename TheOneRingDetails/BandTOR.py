from dataclasses import dataclass
from enum import Enum, auto

from TheOneRingDetails.CharacterTOR import CharacterTOR
from TheOneRingDetails.AllieTOR import AllieTOR

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

class BandCallingType(Enum):
    NONE = 0
    VANGUARDS = auto()          # WAR
    RECLAIMERS = auto()         # EXPERTISE
    GUARDIANS = auto()          # VIGILANCE
    STANDARD_BEARERS = auto()   # RALLY
    PATHFINDERS = auto()        # MANOEUVRE

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
                 size: BandSizeType = BandSizeType.NONE,
                 faculty: BandFacultyType = BandFacultyType.NONE,
                 calling: BandCallingType = BandCallingType.NONE,
                 eyeAwareness: int = 0,
                 huntThreshold: int = 14,
                 hopePts: int = 10,
                 shadowPts: int = 0,
                 shadowScars: int = 0):
        super().__init__(name, hopePts, shadowPts, shadowScars)
        self.id: int = id
        self.allies: list[AllieTOR] = []

        self.armament: BandArmamentType = armament
        self.size: BandSizeType = size
        self.faculty: BandFacultyType = faculty
        self.calling: BandCallingType = calling

        self.eyeAwareness: int = eyeAwareness
        self.huntThreshold: int = huntThreshold

    def getAllyByName(self, name: str) -> AllieTOR | None:
        """Get ally by name."""
        for ally in self.allies:
            if ally.name == name:
                return ally
        return None

    def injureAlly(self, name: str):
        """Injure ally by name."""
        ally = next((ally for ally in self.allies if ally.name == name), None)
        if ally:
            ally.incrementInjury()
            print(f"Ally {name} has been injured. New injury level: {ally.injuries.name}")
        else:
            print(f"Ally {name} not found in the band.")

    def addAlly(self, ally: AllieTOR):
        self.allies.append(ally)
        ally.band = self  # Set the band reference in the ally

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
    
    def isWeary(self) -> bool:
        """Check if the band is weary."""
        wearyCount = sum(1 for ally in self.allies if (ally.active and (ally.isSeriouslyOffended() or ally.isSeriousTired())))
        activeAlliesCount = sum(1 for ally in self.allies if ally.active)
        if wearyCount >= (activeAlliesCount / 2):
            return True
        else:
            return False
    
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
        elif active_allies_count <= 8:
            self.size = BandSizeType.MEDIUM
        else:
            self.size = BandSizeType.LARGE

        print(f"Band size updated to: {self.size.name} based on {active_allies_count} active allies.")

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
        
    def isInspired(self, disposition: BandDispositionType) -> bool:
        """Check if the band is inspired based on the disposition and calling."""
        if disposition is BandDispositionType.NONE or self.calling is BandCallingType.NONE:
            return False
        
        match disposition:
            case BandDispositionType.WAR:
                return self.calling is BandCallingType.VANGUARDS
            case BandDispositionType.EXPERTISE:
                return self.calling is BandCallingType.RECLAIMERS
            case BandDispositionType.VIGILANCE:
                return self.calling is BandCallingType.GUARDIANS
            case BandDispositionType.RALLY:
                return self.calling is BandCallingType.STANDARD_BEARERS
            case BandDispositionType.MANOEUVRE:
                return self.calling is BandCallingType.PATHFINDERS
            case _:
                return False
        
    def printAlliesActive(self):
        """Print the list of active allies in the band."""
        active_allies = [ally for ally in self.allies if ally.active]
        if not active_allies:
            print("No active allies in the band.")
            return
        
        print(f"Active Allies in {self.name}:")
        for ally in active_allies:
            print(ally.__str__())
        
    def printAllies(self):
        """Print the list of allies in the band."""
        if not self.allies:
            print("No allies in the band.")
            return
        
        print(f"Allies in {self.name}:")
        for ally in self.allies:
            print(ally.__str__())
        
    def __str__(self) -> str:
        """Return a string representation of the band."""
        allies_info = "\n".join(
            # f"  - {ally.name} (Active: {ally.active}, Hardened: {ally.hardened})"
            # for ally in self.allies
            ally.__str__()
            for ally in self.allies
        )
        return (
            f"Name: {self.name} (Band ID {self.id})\n"
            f"Size: {self.size.name} Burden: {self.getBurden().name}\n"
            f"Armament: {self.armament.name} Faculty: {self.faculty.name}\n"
            f"Eye Awareness: {self.eyeAwareness} Hunt Threshold: {self.huntThreshold}\n"
            f"Hope Points: {self.hopePts} Shadow Points: {self.shadowPts} Shadow Scars: {self.shadowScars}\n"
            f"Conditions: Weary: {self.isWeary()} Miserable: {self.isMiserable()}\n"
            f"Disposition Levels:\n"
            f"  - W: {self.getWar()} R: {self.getRally()} E: {self.getExpertise()} M: {self.getManoeuvre()} V: {self.getVigilance()}\n"
            f"Allies ({len(self.allies)}):\n{allies_info}"
        )
    
    def __repr__(self):
        return self.__str__()