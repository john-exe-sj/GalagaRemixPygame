from Sprites import Sprite
import Constants
import pygame
from GameField import GameStatus
import math  # Add this import at the top with the others

from BulletController import addBullet

class Ship(Sprite):
  def __init__(self): 
    super().__init__()
    # Store the original image for rotation
    self.original_image = pygame.transform.scale(pygame.image.load('./images/ship.png'), Constants.SHIP_DIMMENSION)
    self.image = self.original_image
    self.rect = self.image.get_rect()
    self.velocity = Constants.SHIP_VELOCITY
    self.rect.x = Constants.X_SHIP_STARTPOINT
    self.rect.y = Constants.Y_SHIP_STARTPOINT
    self.angle = 0  # Track rotation angle


  def rotate(self, angle_change):
    # Update the angle
    self.angle += angle_change
    # Keep angle between 0 and 360 degrees
    self.angle = self.angle % 360
    # Rotate the image
    self.image = pygame.transform.rotate(self.original_image, self.angle)
    # Get the new rect and maintain the center position
    old_center = self.rect.center
    self.rect = self.image.get_rect()
    self.rect.center = old_center



  def move(self, gameStat: GameStatus) -> None: 

    curr_x = self.rect.x
    curr_y = self.rect.y

    keys = pygame.key.get_pressed()

    """
    # Add rotation controls using Q and E keys
    if keys[pygame.K_q]:  # Rotate counterclockwise
      self.rotate(5)
    if keys[pygame.K_e]:  # Rotate clockwise
      self.rotate(-5)
    """

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
    #gameStat.isGameStillRunning = False
    addBullet(gameStat, (self.rect.x, self.rect.y), Constants.IS_HERO_BULLET)
