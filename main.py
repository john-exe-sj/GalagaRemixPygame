import pygame, sys
from pygame.locals import QUIT
import Constants
from ShipController import Ship
from EnemyController import GruntEnemyShip # TODO: generate ships and create their AI
from GameField import GameStatus
from BulletController import updateBullets

if __name__ == "__main__": 
  pygame.init()
  SCREEN = pygame.display.set_mode(Constants.SCREEN_SIZE)
  pygame.display.set_caption('First Game')

  gameStat = GameStatus()
  ship = Ship()
  #enemyShip = GruntEnemyShip()
  #bullet = Bullet((ship.rect.x, ship.rect.y), True)
  gameStat.addSprites([ship])


  while gameStat.isGameStillRunning:
    for event in pygame.event.get(): #grabs all the events in the list
        if event.type == QUIT: #exit button in the window.
          gameStat.isGameStillRunning = False
          print(gameStat.isGameStillRunning)
          pygame.quit()
          sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
              ship.generateBullet(gameStat)
  
    ship.move(gameStat)
    updateBullets(gameStat)
    gameStat.shipHasFired = False

    
    SCREEN.fill(Constants.SCREEN_COLOR)
    gameStat.updateSprites(SCREEN)
    pygame.display.flip()
