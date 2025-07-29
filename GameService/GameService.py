from GameService.Game import Game

class GameService:
    @staticmethod
    def chooseAssets(game: Game) -> None:
        """Choose assets for the game."""
        game.chooseAssets()

    @staticmethod
    def modifyAssets(game: Game) -> None:
        """Modify assets for the game."""
        game.modifyAssets()

    @staticmethod
    def test(game: Game, arg) -> None:
        """Test method for the game."""
        game.test(arg)
        pass

    @staticmethod
    def randomTable(game: Game, arg) -> None:
        """Random table"""
        game.randomTable(arg)

    @staticmethod
    def grantAward(game, arg) -> None:
        """Grant award to the game."""
        game.grantAward(arg)

    @staticmethod
    def showCharacter(game, arg) -> None:
        """Show character details."""
        game.showCharacter(arg)

    @staticmethod
    def enterTheFight(game: Game, arg) -> None:
        """Enter the fight."""
        game.enterTheFight()