import pygame, sys
from pygame.locals import QUIT
import Constants
from ShipController import Ship
from EnemyController import GruntEnemyShip # TODO: generate ships and create their AI
from GameField import GameStatus
from BulletController import updateBullets
from Sprites import calculate_distance

if __name__ == "__main__": 
  pygame.init()
  SCREEN = pygame.display.set_mode(Constants.SCREEN_SIZE, pygame.RESIZABLE)
  pygame.display.set_caption('First Game')

  gameStat = GameStatus()
  ship = Ship()
  gameStat.addPlayerSprite(ship)

  
  while gameStat.isGameStillRunning:

    for event in pygame.event.get(): #grabs all the events in the list
        if event.type == QUIT: #exit button in the window.
          gameStat.isGameStillRunning = False

          pygame.quit()
          sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN: # tell pygame to track our "mouse-events" aka if a button was clicked. 

          if (pygame.mouse.get_pressed()[0] and 
              calculate_distance(
                ship.rect.x, 
                ship.rect.y, 
                pygame.mouse.get_pos()[0], 
                pygame.mouse.get_pos()[1]) > 250
          ): # checks to see if the left button was clicked and making sure that the mouse is at an appropriate distance. 
            ship.generateBullet(gameStat)
  
    ship.move(gameStat)
    updateBullets(gameStat)
    gameStat.shipHasFired = False

    
    SCREEN.fill(Constants.SCREEN_COLOR)
    gameStat.updateSprites(SCREEN)
    pygame.display.flip()
