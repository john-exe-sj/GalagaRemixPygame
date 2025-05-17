import pygame
from Sprites import Sprite
from BulletController import Bullet

class GameStatus(): 

  def __init__(self):
    self.player_sprites = pygame.sprite.Group()
    self.enemy_sprites = pygame.sprite.Group()
    self.score = 0
    self.isGameStillRunning = True
    self.clock = pygame.time.Clock()
    self.shipHasFired = False
    self.shipCoordinates = None
    self.listOfActiveBullets = []

  def updateShipCoord(self, coord: tuple) -> None: 
    self.shipCoordinates = coord

  def addPlayerSprites(self, listOfSprites: list) -> None: 
    self.player_sprites.add(listOfSprites)

  def addPlayerSprite(self, sprite: Sprite) -> None: 
    self.player_sprites.add(sprite)

  def removeRemoveSprite(self, sprite: Sprite) -> None: 
    self.player_sprites.remove(sprite)

  def updateSprites(self, screen: pygame.Surface) -> None:
    self.player_sprites.update()
    for sprite in self.player_sprites: 
      screen.blit(sprite.image, sprite.rect)
    self.dt = self.clock.tick(60)
