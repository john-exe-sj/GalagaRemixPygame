import pygame, sys
from pygame.locals import QUIT
import Constants
from ShipController import Ship
from GameField import GameStatus
from BulletController import updateBullets
from AsteroidController import updateAsteroids, generateAsteroids
from CrosshairController import Crosshair

if __name__ == "__main__": 
  pygame.init()
  SCREEN = pygame.display.set_mode(Constants.SCREEN_SIZE, pygame.RESIZABLE)
  pygame.display.set_caption('First Game')

  gameStat = GameStatus()
  ship = Ship()
  crosshair = Crosshair()

  gameStat.addPlayerSprite([ship, crosshair])

  
  while gameStat.isGameStillRunning:

    for event in pygame.event.get(): #grabs all the events in the list
        if event.type == QUIT: #exit button in the window.
          gameStat.isGameStillRunning = False

          pygame.quit()
          sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN: # tell pygame to track our "mouse-events" aka if a button was clicked. 

          if pygame.mouse.get_pressed()[0] and ship in gameStat.player_sprites: # checks to see if the left button was clicked and making sure that the mouse is at an appropriate distance. 
            ship.generateBullet(gameStat)


    ship.move()
    crosshair.move()
    generateAsteroids(gameStat, ship)
    updateBullets(gameStat)
    updateAsteroids(gameStat)
    gameStat.handleCollisions()
    gameStat.handleAnimations()
    gameStat.handleDestruction()
    gameStat.handleReset()

    SCREEN.fill(Constants.SCREEN_COLOR)
    gameStat.updateSprites(SCREEN)
    pygame.display.flip()
