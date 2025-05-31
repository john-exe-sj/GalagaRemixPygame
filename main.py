"""
Main entry point for the Galaga Remix game.
This module initializes the game and runs the main game loop.
"""

from GameController import Game, initiateGameScreen


def main():
    """Initialize and run the main game loop."""
    # Initialize game screen and state
    SCREEN = initiateGameScreen()
    game = Game(SCREEN)
    
    # Main game loop
    while game.isGameStillRunning:
        game.handleGameEvents()
        game.handleEnemyAndObstacleGeneration()
        game.handleSpriteMotion()
        game.handleCollisions()
        game.handleAnimations()
        game.handleDestruction()
        game.handleButtonGeneration()
        game.updateSprites()


if __name__ == "__main__":
    main()
