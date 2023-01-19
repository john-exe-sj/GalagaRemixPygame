import pygame
from Sprites import Sprite
from BulletController import Bullet

class GameStatus(): 

  def __init__(self):
    self.sprites = pygame.sprite.Group()
    self.score = 0
    self.isGameStillRunning = True
    self.clock = pygame.time.Clock()
    self.shipHasFired = False
    self.shipCoordinates = None
    self.listOfActiveBullets = []

  def updateShipCoord(self, coord: tuple) -> None: 
    self.shipCoordinates = coord

  def addSprites(self, listOfSprites: list) -> None: 
    self.sprites.add(listOfSprites)

  def addSprite(self, sprite: Sprite) -> None: 
    self.sprites.add(sprite)

  def removeSprite(self, sprite: Sprite) -> None: 
    self.sprites.remove(sprite)

  def updateSprites(self, screen: pygame.Surface) -> None:
    self.sprites.update()
    self.sprites.draw(screen)
    self.dt = self.clock.tick(60)
