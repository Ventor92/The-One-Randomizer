from dataclasses import dataclass
from enum import Enum

class DispositionsType(Enum):
    NONE = 0
    RALLY = 1
    WAR = 2
    EXPERTISE = 3
    MANOEUVRE = 4
    VIGILANCE = 5

class BandSizeType(Enum):
    SMALL = 1
    MEDIUM = 4
    LARGE = 9 

class BurdenType(Enum):
    LIGHT = 1
    MEDIUM = 2
    HEAVY = 3
    OVERBURDENED = 4

class ConditionsType(Enum):
    Weary = 1
    Miserable = 2

@dataclass
class MissionRosterBand:
    def __init__(self, readiness=4, rally=2, war=2, expertise=2, manoeuvre=2, vigilance=2, hope=10, shadowPts=0):
        self.readiness = readiness          #sprawność
        self.rally = rally                  #dzielność
        self.war = war                      #bitność
        self.expertise = expertise          #fachowość
        self.manoeuvre = manoeuvre          #mobilność
        self.vigilance = vigilance          #ostrożność
        self.hope = hope                    #nadzieja
        self.shadowPts = shadowPts            #Punkty Cienia
        # self.bandSize = BandSizeType        #wielkość kompanii
        # self.burden = burden                #brzemię
        # self.eyeAwareness = eyeAwareness    #Uwaga Oka
        # self.huntThreshold = huntThreshold  #Próg Poszukiwania
        # self.conditions = conditions        #Ograniczenia

    def __str__(self):
        return (
            f"Mission Roster Band:\n"
            f"  Readiness   (Sprawność):        {self.readiness}\n"
            f"  Rally       (Dzielność):        {self.rally}\n"
            f"  War         (Bitność):          {self.war}\n"
            f"  Expertise   (Fachowość):        {self.expertise}\n"
            f"  Manoeuvre   (Mobilność):        {self.manoeuvre}\n"
            f"  Vigilance   (Ostrożność):       {self.vigilance}\n"
            f"  Hope        (Nadzieja):         {self.hope}\n"
            f"  ShadowPts   (Punkty Cienia):    {self.shadowPts}\n"
            f"  Conditions  (Ograniczenia):     \n"
            f"    Weary       (Wyczepranie):      TODO\n"
            f"    Miserable   (Przygnębienie):    {self.isMiserable()}\n"
        )
    
    def __repr__(self):
        # Możesz zwrócić taki sam string jak w __str__
        return self.__str__()
    
    def getTN(self) -> int:
        tn:int = 20 - self.readiness
        return tn
    
    def getWar(self) -> int:
        return self.war
    
    def getRally(self) -> int:
        return self.rally
    
    def getExpertise(self) -> int:
        return self.expertise
    
    def getManoeuvre(self) -> int:
        return self.manoeuvre
    
    def getVigilance(self) -> int:
        return self.vigilance
    
    def getHope(self) -> int:
        return self.hope
    
    def setHope(self, hope:int) -> None:
        self.hope = hope

    def changeHope(self, hope:int) -> int:
        self.hope += hope
        if self.hope < 0:
            self.hope = 0
        return self.hope
    
    def isMiserable(self) -> bool:
        if self.hope <= self.shadowPts:
            return True
        else:
            return False 
    
    