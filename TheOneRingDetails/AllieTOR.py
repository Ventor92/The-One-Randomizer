from dataclasses import dataclass
from enum import Enum, auto

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from TheOneRingDetails.BandTOR import BandTOR  # Import tylko dla adnotacji typów


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
    band: 'BandTOR | None' = None  # Type hint for BandTOR, set to None by default
    id: int = 0

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

    def isSeriouslyOffended(self) -> bool:
        """Check if the ally is seriously offended."""
        return self.injuries in {InjuryTORType.SEVERE, InjuryTORType.GRIEVOUS, InjuryTORType.LINGERING}
    
    def isSeriousTired(self) -> bool:
        """Check if the ally is seriously tired."""
        return self.fatigue in {FatigueTORType.SPENT, FatigueTORType.COLLAPSED}
    
    def isActive(self) -> bool:
        """Check if the ally is active."""
        return self.active
    
    def __str__(self) -> str:
        return (f"{self.id} Name:{self.name:<8} {'HARD' if self.hardened else 'BEG':<8}{'(ACTIVE)' if self.active else '(CAMP)':<10}"
                f"Inj.:{self.injuries.name + '(' + str(self.injuries.value) + '/5)':<14} Fatg.:{self.fatigue.name+'('+str(self.fatigue.value)+'/5)':<14}"
                f"N.Gift:{self.gift + ('(*)' if self.giftWasted else '( )'):<18}" 
                f"K.Gift:{self.kinglyGift + ('(*)' if self.kinglyGiftWasted else '( )'):<18}" 
                # f"Quirks/Notes:'{self.quirksOrNotes}'"
                )
    
    def __repr__(self) -> str:
        return (f"AllieTOR(id={self.id}, idBand={self.idBand}, active={self.active}, name={self.name!r}, "
                f"injuries={self.injuries!r}, fatigue={self.fatigue!r}, hardened={self.hardened}, "
                f"gift={self.gift!r}, giftWasted={self.giftWasted}, kinglyGift={self.kinglyGift!r}, "
                f"kinglyGiftWasted={self.kinglyGiftWasted}, quirksOrNotes={self.quirksOrNotes!r})")