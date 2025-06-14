import cmd

from TheOneRingDetails.EventTheOneRing import EventTheOneRing
from TheOneRingDetails.ThreadTheOneRing import ThreadTOR
from TheOneRingDetails.MissionTOR import MissionTOR

from TableService.RecordFactory import RecordFactory

from GameService.GameController import GameController

RecordFactory.register((EventTheOneRing), EventTheOneRing.fromRow)
RecordFactory.register((ThreadTOR), ThreadTOR.fromRow)
RecordFactory.register((MissionTOR), MissionTOR.fromRow)

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
    
    def do_randomTable (self, arg):
        """Wylosuj Zasób"""
        GameController.randomTable(arg)

    def do_chooseAssets(self, arg):
        """Wybierz zasoby"""
        GameController.chooseAssets()
    
    def do_modifyAssets(self, arg):
        """Modyfikuj zasoby"""
        GameController.modifyAssets()

    def do_test(self, arg):
        """test 
        NONE RALLY WAR EXPERTISE MANOEUVRE VIGILANCE
        ILL NORMAL FAVOURED
        spentHope bonusSuccess
        e.g: test EXPERTISE ILL 0 1"""
        GameController.test(arg)

    def do_travelEvent(self, arg):
        # table:TableEvent = TableEvent(EventTheOneRing)
        # journey = JourneyTor(actualMissionRosterBand, table)
        # journey.doTravelEvent()
        pass

    # Inne komendy mogą być dodane tutaj...

if __name__ == "__main__":
    main()
    app = DiceApp()
    app.do_chooseAssets("nothing")
    app.cmdloop()  # Rozpoczyna interaktywną pętlę komend