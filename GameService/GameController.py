from GameService.Game import Game
from GameService.GameService import GameService
from TheOneRingDetails.GameTOR import GameTOR

class GameController:
    @staticmethod
    def __getGame() -> Game:
        return GameTOR()
    
    @staticmethod
    def chooseAssets():
        """Choose assets for the game."""
        game: Game = GameController.__getGame()
        GameService.chooseAssets(game)

    @staticmethod
    def modifyAssets():
        """Modify assets for the game."""
        game: Game = GameController.__getGame()
        GameService.modifyAssets(game)
    
    @staticmethod
    def test(arg):
        """Test method for the game."""
        game: Game = GameController.__getGame()
        GameService.test(game, arg)

    @staticmethod
    def randomTable(arg):
        """Random table"""
        game: Game = GameController.__getGame()
        GameService.randomTable(game, arg)

    @staticmethod
    def grantAward(arg):
        """Grant award to the game."""
        game: Game = GameController.__getGame()
        GameService.grantAward(game, arg)

    @staticmethod
    def showCharacter(arg):
        """Show character details."""
        game: Game = GameController.__getGame()
        GameService.showCharacter(game, arg)
