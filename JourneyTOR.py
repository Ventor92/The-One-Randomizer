from enum import Enum
from enum import auto
from dataclasses import dataclass
from DiceService.Dice import Dice, DiceType
from MissionRosterBand import MissionRosterBand
from DispositionsService import DispositionsService, DispositionsType, DiceFeatType
from TableService.EventService.TableEvent import TableEvent

class ParticipantType(Enum):
    NONE = auto()
    BAND = auto()
    NPC = auto()
    PC = auto()

class JourneyTorStep(Enum):
    START_JOURNEY = auto()
    SPEC_DEST = auto()
    START_TRAVEL = auto()
    TEST_BAND_MANOEUVRE = auto()
    TEST_PC_TRAVEL = auto()
    TRAVEL_DISTANCE = auto()
    CHOOSE_PARTISIPANT = auto()
    ROLL_TRAVEL_EVENT = auto()
    TEST_PARTICIPANT = auto()
    GET_EVENT_FAITGE = auto()
    END_EVENT = auto()

class JourneyTor():
    def __init__(self, band, eventTable):
        self.band:MissionRosterBand = band
        self.travelDistance = 0
        self.travelEvent = None
        self.participant = None
        self.Step = JourneyTorStep.START_TRAVEL
        self.eventTable: TableEvent = eventTable
    
    def __str__(self):
        return (
            f"JourneyTor:\n"
            f"  Band: {self.band}\n"
            f"  Travel Distance: {self.travelDistance}\n"
            f"  Travel Event: {self.travelEvent}\n"
            f"  Participant: {self.participant}\n"
        )
    
    def specDest(self):
        dice = Dice(DiceType.D6)
        results: list[int] = dice.roll(2)
        distance = sum(results)*4
        return distance
    
    def testBandManoeuvre(self):
        isSuccess = DispositionsService.test(self.band, DispositionsType.MANOEUVRE, DiceFeatType.NORMAL)

    def rollTravelEvent(self):
        event = self.eventTable.rollEvent()
        if event is None:
            raise ValueError("Event is None")
        return event
    
    def testParticipant(self, participantType: ParticipantType, dispositions: DispositionsType, diceFeatType: DiceFeatType):
        if participantType == ParticipantType.BAND:
            isSuccess = DispositionsService.test(self.band, dispositions, diceFeatType)
        elif participantType == ParticipantType.PC:
            isSuccess = DispositionsService.test(self.band, dispositions, diceFeatType)
        else:
            raise ValueError("Invalid participant type")
        return isSuccess
    
    def doTravelEvent(self):
        self.rollTravelEvent()
        arg: str = input(">> dispositions featType")

        try:
            str1, str2 = arg.split()
        except ValueError:
            str1 = ""
            str2 = ""

        # Convert string to DispositionsType using getattr with a default
        type: DispositionsType = getattr(DispositionsType, str1.upper(), DispositionsType.NONE)

        # Convert string to DiceFeatType using getattr with a default
        diceFeat: DiceFeatType = getattr(DiceFeatType, str2.upper(), DiceFeatType.NORMAL)

        self.testParticipant(ParticipantType.BAND, type, diceFeat)


