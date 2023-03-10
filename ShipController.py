from Sprites import Sprite
import Constants
import pygame
from GameField import GameStatus

from BulletController import addBullet

class Ship(Sprite):
  def __init__(self): 
    super().__init__()
    fixedImage = pygame.transform.scale(pygame.image.load('./images/ship.png'), Constants.SHIP_DIMMENSION)
    self.image =  fixedImage
    self.rect = self.image.get_rect()
    self.velocity = Constants.SHIP_VELOCITY
    self.rect.x = Constants.X_SHIP_STARTPOINT
    self.rect.y = Constants.Y_SHIP_STARTPOINT

  def move(self, gameStat: GameStatus) -> None: 

    curr_x = self.rect.x
    curr_y = self.rect.y

    #print(curr_x, " : ", curr_y)
    keys = pygame.key.get_pressed()
    if(keys[pygame.K_a] and curr_x >= Constants.X_SHIP_LEFTBOUND): #left
      self.rect.x -= self.velocity 
  
    if(keys[pygame.K_d] and curr_x <= Constants.X_SHIP_RIGHTBOUND): #right
      self.rect.x += self.velocity 

    if(keys[pygame.K_w] and curr_y >= Constants.Y_SHIP_UPPERBOUND): #up
      self.rect.y -= self.velocity

    if(keys[pygame.K_s] and curr_y <= Constants.Y_SHIP_LOWERBOUND): #down
      self.rect.y += self.velocity

    gameStat.updateShipCoord((self.rect.x, self.rect.y))

  def generateBullet(self, gameStat: GameStatus) -> None: 
    #print("Ship has fired")
    addBullet(gameStat, (self.rect.x, self.rect.y), Constants.IS_HERO_BULLET)
