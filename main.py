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

from GameFactory import GameFactory
from Game import Game
from GameTOR import GameTOR

from JourneyTOR import JourneyTor

from typing import List

diceFeat = DiceTheOneRing(DiceTheOneRingType.FEAT)
diceSuccess = DiceTheOneRing(DiceTheOneRingType.SUCCESS)

RecordFactory.register((EventTheOneRing), EventTheOneRing.fromRow)
RecordFactory.register((ThreadTOR), ThreadTOR.fromRow)
RecordFactory.register((MissionTOR), MissionTOR.fromRow)

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
        # table:TableEvent = TableEvent(id(EventTheOneRing))
        game: Game = GameTOR()
        try:
            strNumFeat, strNumSuccess = arg.split()
            numFeat = int(strNumFeat)
            numSuccess = int(strNumSuccess)
            game.getRecord(TableEvent, [numFeat, numSuccess])
        except ValueError:
            # print("Error, default number")
            game.rollRecord(TableEvent)

    def do_thread(self, arg):
        """Wylosuj Wątek"""
        game: Game = GameTOR()

        try:
            strNumFeat, strNumSuccess = arg.split()
            numFeat = int(strNumFeat)
            numSuccess = int(strNumSuccess)
            game.getRecord(TableThread, [numFeat, numSuccess])
        except ValueError:
            # print("Error, default number")
            game.rollRecord(TableThread)
        
    def do_mission(self, arg):
        """Wylosuj Wątek"""
        game: Game = GameTOR()

        try:
            strNumFeat, strNumSuccess = arg.split()
            numFeat = int(strNumFeat)
            numSuccess = int(strNumSuccess)
            game.getRecord(TableMission, [numFeat, numSuccess])
        except ValueError:
            # print("Error, default number")
            game.rollRecord(TableMission)

    def do_rollCombo(self, arg):
        """Rzuć wybraną ilością kośćmi TOR. Składnia: rollCombo <numFeat> <numSuccess>"""

        numFeat: int = 1;
        numSuccess: int = 1;
        targetNumber: int = 1;
        try:
            strNumFeat, strNumSuccess, strTargetNumber = arg.split()
            numFeat = int(strNumFeat)
            numSuccess = int(strNumSuccess)
            targetNumber = int(strTargetNumber)
        except ValueError:
            print("Error, default number")
        
        rollsFeat:List[int] = diceFeat.roll(numFeat)
        rollsSuccess:List[int] = diceSuccess.roll(numSuccess)

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
        """NONE RALLY WAR EXPERTISE MANOEUVRE VIGILANCE"""
        try:
            str1, str2, str3, str4 = arg.split()
            type = DispositionsService.str2DispositionType(str1)
            diceFeat = DispositionsService.str2DiceFeatType(str2)
            spentHope = int(str3)
            bonusSuccess = int(str4)
        except ValueError:
            type = DispositionsType.NONE
            diceFeat = DiceFeatType.NORMAL
            spentHope = 0
            bonusSuccess = 0

        print(f"{type.name} {diceFeat.name}")

        DispositionsService.test(actualMissionRosterBand, type, diceFeat, spentHope, bonusSuccess)

    def do_travelEvent(self, arg):
        # table:TableEvent = TableEvent(EventTheOneRing)
        # journey = JourneyTor(actualMissionRosterBand, table)
        # journey.doTravelEvent()
        pass

    # Inne komendy mogą być dodane tutaj...

if __name__ == "__main__":
    main()
    app = DiceApp()
    app.do_chooseMissionRoster("nothing")
    app.cmdloop()  # Rozpoczyna interaktywną pętlę komend