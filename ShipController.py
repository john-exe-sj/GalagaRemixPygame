from Sprites import Sprite
import Constants
import pygame
from GameField import GameStatus

from BulletController import addBullet

SHIP_ANGLE_OFFSET = 110
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

  def move(self, gameStat: GameStatus) -> None: 

    curr_x_ship_coord, curr_y_ship_coord = self.rect.x, self.rect.y
    width_of_screen, height_of_screen = pygame.display.get_surface().get_size() # returns the dimensions of the screen, note; the screen's dimmensions can change. 
    print(f"Ship Position: ({curr_x_ship_coord}, {curr_y_ship_coord}), Window Size: {width_of_screen}x{height_of_screen}, Mouse Position: {pygame.mouse.get_pos()}")

    keys = pygame.key.get_pressed()

    self.pointTowardsMousePointer(Constants.SHIP_ANGLE_OFFSET)
    
    if(keys[pygame.K_a] and curr_x_ship_coord >= 0): #left
      self.rect.x -= self.velocity 
  
    if(keys[pygame.K_d] and curr_x_ship_coord <= width_of_screen): #right
      self.rect.x += self.velocity 

    if(keys[pygame.K_w] and curr_y_ship_coord >= 0): #up
      self.rect.y -= self.velocity

    if(keys[pygame.K_s] and curr_y_ship_coord <= height_of_screen): #down
      self.rect.y += self.velocity
    
    gameStat.updateShipCoord((self.rect.x, self.rect.y))

  def generateBullet(self, gameStat: GameStatus) -> None: 

    addBullet(gameStat, (self.rect.x, self.rect.y), self.angle + Constants.SHIP_ANGLE_OFFSET)
