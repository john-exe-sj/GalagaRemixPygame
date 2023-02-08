from Sprites import Sprite
import pygame
import Constants

class GruntEnemyShip(Sprite):

  def __init__(self): 
    super().__init__()
    fixedImage = pygame.transform.scale(pygame.image.load('./images/enemyship.png'), Constants.ENEMY_SHIP_DIMMENSIONS)
    self.image = pygame.transform.rotate(fixedImage, 180)
    self.rect = self.image.get_rect()
    self.velocity = Constants.SHIP_VELOCITY
    self.rect.x = Constants.X_ENEMY_SHIP
    self.rect.y = Constants.Y_ENEMY_SHIP

  #def move(self):
    