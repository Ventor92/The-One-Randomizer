import cmd

from TheOneRingDetails.TreasuryTORService import TreasuryTORService
from TheOneRingDetails.TreasuryTOR import TreasuryTOR
from TheOneRingDetails.CharacterTOR import CharacterTOR

class TreasuryTORController(cmd.Cmd):
    intro = "Wszedłeś do skarbca. Co robisz?."
    prompt = "(Treasury) "

    treasury = None
    character = None

    @staticmethod
    def enterToTreasury(treasury: TreasuryTOR, character: CharacterTOR):
        """Enter a character into the treasury."""
        app = TreasuryTORController()
        app.treasury = treasury
        app.character = character
        app.cmdloop()  # Rozpoczyna interaktywną pętlę komend

    def __exit(self):
        """Exit the treasury"""
        print("Go out from the Treasury!")
        self.treasury = None
        self.character = None
        return True

    # Komenda do wyjścia z aplikacji
    def do_exit(self, arg):
        """Wyjście z aplikacji"""
        return self.__exit()
    
    def do_takeTreasure(self, arg):
        """Take treasure from the treasury."""
        if self.treasury is None or self.character is None:
            raise ValueError("Treasury or character is not set.")
        else:
            TreasuryTORService.takeTreasure(self.treasury, self.character)
    
    def do_takeMagicItems(self, arg):
        """Take magic items from the treasury."""
        if self.treasury is None or self.character is None:
            raise ValueError("Treasury or character is not set.")
        else:
            TreasuryTORService.takeMagicItems(self.treasury, self.character)

    def do_showTreasury(self, arg):
        """Show the treasury."""
        if self.treasury is None:
            raise ValueError("Treasury is not set.")
        else:
            TreasuryTORService.showTresure(self.treasury)