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
from GameTOR import GameTOR, BandDispositionType

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

    def do_chooseMissionRoster(self, arg):
        global actualMissionRosterBand
        actualMissionRosterBand = DispositionsService.chooseMissionRoster(sheetMissionRoster)
    
    def do_dispositionsTest(self, arg):
        """dispositionsTest 
        NONE RALLY WAR EXPERTISE MANOEUVRE VIGILANCE
        ILL NORMAL FAVOURED
        spentHope bonusSuccess
        e.g: dispositionsTest EXPERTISE ILL 0 1"""
        try:
            str1, str2, str3, str4 = arg.split()
            type = DispositionsService.str2DispositionType(str1)
            diceFeat = DispositionsService.str2DiceFeatType(str2)
            spentHope = int(str3)
            bonusSuccess = int(str4)
        except ValueError:
            type = BandDispositionType.NONE
            diceFeat = DiceFeatType.NORMAL
            spentHope = 0
            bonusSuccess = 0

        print(f"{type.name} {diceFeat.name}")

        DispositionsService.testBand(GameTOR().band, type, diceFeat, spentHope, bonusSuccess)

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
    game: Game = GameTOR()
    game.chooseAssets()
    app.cmdloop()  # Rozpoczyna interaktywną pętlę komend