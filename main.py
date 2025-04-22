import cmd
import random

from DiceService.Dice import DiceType, Dice
from TheOneRingDetails.DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType, DiceFeatType
from DispositionsService import DispositionsService, DispositionsType, MissionRosterBand
from SheetMissionRoster import SheetMissionRoster
from TableService.EventService.EventService import EventService

from TheOneRingDetails.EventTheOneRing import EventTheOneRing
from TheOneRingDetails.ThreadTheOneRing import ThreadTOR
from TheOneRingDetails.MissionTOR import MissionTOR

from TableService.RecordFactory import RecordFactory
from TableService.EventService.TableEvent import TableEvent
from TableService.ThreadService.TableThread import TableThread
from TableService.MissionService.TableMission import TableMission

from JourneyTOR import JourneyTor

from typing import List

diceFeat = DiceTheOneRing(DiceTheOneRingType.FEAT)
diceSuccess = DiceTheOneRing(DiceTheOneRingType.SUCCESS)

RecordFactory.register(id(EventTheOneRing), EventTheOneRing.fromRow)
RecordFactory.register(id(ThreadTOR), ThreadTOR.fromRow)
RecordFactory.register(id(MissionTOR), MissionTOR.fromRow)

sheetMissionRoster: SheetMissionRoster = SheetMissionRoster()
actualMissionRosterBand: MissionRosterBand = MissionRosterBand(readiness=0)

def main():
    print("Witaj w moim dice rollerze!")

class DiceApp(cmd.Cmd):
    intro = "Witaj w aplikacji kości! Wpisz 'help' lub '?' aby zobaczyć dostępne komendy."
    prompt = "(Kości) "

    # Komenda do wypisania dostępnych kości
    def do_list(self, arg):
        """Wypisz dostępne kości"""
        print("Dostępne kości: D4, D6, D8, D10, D12, D20")

    # Komenda do wyjścia z aplikacji
    def do_exit(self, arg):
        """Wyjście z aplikacji"""
        print("Do widzenia!")
        return True
    
    def do_event(self, arg):
        """Wylosuj event"""
        table:TableEvent = TableEvent(id(EventTheOneRing))
        try:
            strNumFeat, strNumSucc = arg.split()
            numFeat = int(strNumFeat)
            numSucc = int(strNumSucc)
            table.getEvent([numFeat, numSucc])
        except ValueError:
            # print("Error, default number")
            table.rollEvent()

    def do_thread(self, arg):
        """Wylosuj Wątek"""
        table: TableThread = TableThread(id(ThreadTOR))

        try:
            strNumFeat, strNumSucc = arg.split()
            numFeat = int(strNumFeat)
            numSucc = int(strNumSucc)
            table.getThread([numFeat, numSucc])
        except ValueError:
            # print("Error, default number")
            table.rollThread()
        
    def do_mission(self, arg):
        """Wylosuj Wątek"""
        table: TableMission = TableMission(id(MissionTOR))

        try:
            strNumFeat, strNumSucc = arg.split()
            numFeat = int(strNumFeat)
            numSucc = int(strNumSucc)
            table.getMission([numFeat, numSucc])
        except ValueError:
            # print("Error, default number")
            table.rollMission()

    def do_rollCombo(self, arg):
        """Rzuć wybraną ilością kośćmi TOR. Składnia: rollCombo <numFeat> <numSucc>"""

        numFeat: int = 1;
        numSucc: int = 1;
        targetNumber: int = 1;
        try:
            strNumFeat, strNumSucc, strTargetNumber = arg.split()
            numFeat = int(strNumFeat)
            numSucc = int(strNumSucc)
            targetNumber = int(strTargetNumber)
        except ValueError:
            print("Error, default number")
        
        rollsFeat:List[int] = diceFeat.roll(numFeat)
        rollsSuccess:List[int] = diceSuccess.roll(numSucc)

        successSum:int = sum(rollsSuccess)
        rollsFeatTemp = [0 if x == 11 else x for x in rollsFeat]
        featMax:int = max(rollsFeatTemp)
        featMin:int = min(rollsFeatTemp)
        feat:int = featMin


        count = rollsSuccess.count(6)
        if ((successSum + feat) >= targetNumber) or (feat == 12):
            strResult = f"SUCCESS! Quality: ({count})"
        else:
            strResult = f"FAIL!"
            
        print(f"Result: {strResult} -> TN:{targetNumber} Total:{successSum+feat}")
        print(f"Details: Feat:{rollsFeat}->{feat} Success:{rollsSuccess}->{successSum}")

    def do_chooseMissionRoster(self, arg):
        global actualMissionRosterBand
        actualMissionRosterBand = DispositionsService.chooseMissionRoster(sheetMissionRoster)
    
    def do_dispositionsTest(self, arg):

        try:
            str1, str2, str3, str4 = arg.split()
        except ValueError:
            str1 = "" 
            str2 = ""

        
        type: DispositionsType = DispositionsType.NONE
        match str1:
            case DispositionsType.RALLY.name:
                type:DispositionsType = DispositionsType.RALLY
            case DispositionsType.MANOEUVRE.name:
                type:DispositionsType = DispositionsType.MANOEUVRE
            case DispositionsType.EXPERTISE.name:
                type:DispositionsType = DispositionsType.EXPERTISE
            case DispositionsType.VIGILANCE.name:
                type:DispositionsType = DispositionsType.VIGILANCE
            case DispositionsType.WAR.name:
                type:DispositionsType = DispositionsType.WAR
            case _:
                # raise TypeError(f"{cls.__name__} Zły typ Kompenencji.")
                # type:DispositionsType = DispositionsType.UNKNOWN 
                type:DispositionsType = DispositionsType.RALLY
                pass
        
        diceFeat: DiceFeatType = DiceFeatType.NORMAL
        match str2:
            case DiceFeatType.FAVOURED.name:
                diceFeat = DiceFeatType.FAVOURED
            case DiceFeatType.ILL.name:
                diceFeat = DiceFeatType.ILL
            case DiceFeatType.NORMAL.name | _:
                diceFeat = DiceFeatType.NORMAL

        print(f"{type.name} {diceFeat.name}")

        DispositionsService.test(actualMissionRosterBand, type, diceFeat)

    def do_travelEvent(self, arg):
        table:TableEvent = TableEvent(id(EventTheOneRing))
        journey = JourneyTor(actualMissionRosterBand, table)
        journey.doTravelEvent()

    # Inne komendy mogą być dodane tutaj...

if __name__ == "__main__":
    main()
    app = DiceApp()
    app.do_chooseMissionRoster("nothing")
    app.cmdloop()  # Rozpoczyna interaktywną pętlę komend