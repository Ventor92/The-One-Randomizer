import cmd

from TheOneRingDetails.BandTOR import BandTOR
from TheOneRingDetails.EnemyTOR import EnemyTOR
from TheOneRingDetails.ClashTORService import ClashTORService, StancesTOR
from TheOneRingDetails.ResultTOR import ResultTOR, SuccessTORType

class FightTORCtrl(cmd.Cmd):
    intro = "Jestes w kontrolerze walki. Wpisz 'help' lub '?' aby zobaczyć dostępne komendy."
    prompt = "(Walka) "
    
    band: BandTOR
    enemy: EnemyTOR
    stance: StancesTOR

    lastClashResult: ResultTOR | None = None

    @staticmethod
    def enterFight(band: BandTOR):
        
        app = FightTORCtrl()
        app.band = band
        # app.do_chooseAssets("nothing")
        app.cmdloop()  # Rozpoczyna interaktywną pętlę komend

    def do_exit(self, arg):
        """Wyjście z aplikacji"""
        print("Wyszedłeś z Bitwy!")
        return True
    
    def do_createEnemy(self, arg):
        """Utwórz wroga
        createEnemy
        <name>
        mighty: int
        resistance: int
        e.g: createEnemy Orcs_Band 2 9"""
        # Tutaj powinien być kod do utworzenia wroga

        try:
            str1, str2, str3 = arg.split()
            name = str1
            mighty = int(str2)
            resistance = int(str3)
        except ValueError:
            name = "Orcs_Band"
            mighty = 2
            resistance = 9
        
        self.enemy = EnemyTOR(mighty, resistance)
        print(f"Enemy created: {self.enemy}")
        print(f"Next cmd: chooseStance")

    def do_chooseStance(self, arg):
        """Wybierz postawę kompanii
        chooseStance
        [FORWARD, OPEN, DEFENSIVE, REARWARD]
        e.g: chooseStance FORWARD"""

        try:
            stance = StancesTOR[arg.strip().upper()]
            self.stance = stance
            print(f"Band stance chosen: {self.stance}")
        except KeyError:
            print("Invalid stance. Please choose a valid stance.")
        
        print(f"Next cmd: makeClash")

    def do_makeClash(self, arg):
        """Wykonaj Clash
        makeClash
        [spentHope] [bonusSuccess]
        e.g: makeClash 0 1"""
        
        spentHope = 0
        bonusSuccess = 0    
        try:
            spentHope, bonusSuccess = map(int, arg.split())
        except ValueError:
            print("Using default values: spentHope=0, bonusSuccess=0")

        result = ClashTORService.makeClash(self.band, self.enemy, self.stance, spentHope, bonusSuccess)
        self.lastClashResult = result
        print(f"Clash result: {result}")

        print(f"Next cmd: resolveClash")

    def do_resolveClashSucceeded(self, arg):
        """Rozwiąż Clash
        resolveClashSucceeded
        [hit]
        e.g: resolveClashSucceeded 1"""
        
        if self.lastClashResult is None:
            print("No clash result to resolve. Please make a clash first.")
            return
        
        hit = 0   
        try:
            hit = int(arg.strip())
        except ValueError:
            hit = 1 + ClashTORService.mapUsableSuccess(self.stance, self.lastClashResult)
            print(f"Using max possible value: hit = {hit}")
        
        ClashTORService.onClashSucceeded(self.band, self.enemy, self.stance, self.lastClashResult, hit)
        print("Clash resolved.")

        print(f"Next cmd: exitFight")

    def do_makeRally(self, arg):
        """Rozwiąż Clash
        makeRally
        [spentHope] [bonusSuccess]
        e.g: makeRally 0 1"""
        
        if self.lastClashResult is None:
            print("No clash result to resolve. Please make a clash first.")
            return
        
        spentHope = 0
        bonusSuccess = 0    
        try:
            spentHope, bonusSuccess = map(int, arg.split())
        except ValueError:
            print("Using default values: spentHope=0, bonusSuccess=0")
        
        result = ClashTORService.makeRally(self.band, self.enemy, spentHope, bonusSuccess)
        
        match result.success:
            case SuccessTORType.FAILURE | SuccessTORType.MISERABLE:
                print(f"Rally Failed with result: {result.success.name}")
                print(f"Choose 1 ally to injure.")
                self.band.printAlliesActive()
                print(f"Next cmd: injureAlly <allyName>")
            case SuccessTORType.EXTRAORDINARY | SuccessTORType.GREAT | SuccessTORType.CRITICAL | SuccessTORType.NORMAL:
                print(f"Rally succeeded with result: {result.success.name}")
                print(f"Next cmd: endClash")


    def do_injureAlly(self, arg):
        """Kontuzjuj sojusznika
        injureAlly
        <allyName>
        e.g: injureAlly Aragorn"""

        try:
            allyName = arg.strip()
        except ValueError:
            print("Please provide a valid ally name.")
            return
        
        ally = self.band.getAllyByName(allyName)
        if ally is None:
            print(f"No ally found with name: {allyName}")
            print(f"Choose 1 ally to injure.")
            self.band.printAllies()
            print(f"Next cmd: injureAlly <allyName>")
        else:
            ally.incrementInjury()
            print(f"Ally {ally} has been injured.")
            print(f"Next cmd: endClash")
        
        # Tutaj powinien być kod do zranienia sojusznika