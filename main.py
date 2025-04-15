import cmd
import random

from Dice import DiceType, Dice
from DiceTheOneRing import DiceTheOneRing, DiceTheOneRingType, DiceFeatType
from TableEvent import TableEvent
from TableThread import TableThread, Thread
from Event import Event
from DispositionsService import DispositionsService, DispositionsType, MissionRosterBand
from SheetMissionRoster import SheetMissionRoster
from EventService import EventService

from typing import List

diceFeat = DiceTheOneRing(DiceTheOneRingType.FEAT)
diceSuccess = DiceTheOneRing(DiceTheOneRingType.SUCCESS)
# tableEvent: TableEvent = TableEvent()
tableThread: TableThread = TableThread()


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
        # rollsFeat:List[int] = diceFeat.roll(1)
        # rollsSuccess:List[int] = diceSuccess.roll(1)

        # event: Event = tableEvent.getEvent(rollsFeat[0], rollsSuccess[0])
        # print(event)
        table = TableEvent()
        service = EventService(table)
        try:
            strNumFeat, strNumSucc = arg.split()
            numFeat = int(strNumFeat)
            numSucc = int(strNumSucc)
            service.getEvent(numFeat, numSucc)
        except ValueError:
            # print("Error, default number")
            service.rollEvent()

    def do_thread(self, arg):
        """Wylosuj Wątek"""
        rollsFeat:List[int] = diceFeat.roll(1)
        rollsSuccess:List[int] = diceSuccess.roll(1)
        thread: Thread | None = tableThread.getThread(rollsFeat[0], rollsSuccess[0])
        print(thread)

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
            str1, str2 = arg.split()
        except ValueError:
            str1 = "" 
            str2 = ""
        
        type: DispositionsType = DispositionsType.UNKNOWN
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
                type:DispositionsType = DispositionsType.UNKNOWN
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


    # Inne komendy mogą być dodane tutaj...

if __name__ == "__main__":
    main()
    app = DiceApp()
    app.cmdloop()  # Rozpoczyna interaktywną pętlę komend