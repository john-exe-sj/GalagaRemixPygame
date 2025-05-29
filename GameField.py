import pygame
from typing import List
from Sprites import Sprite
from AnimationController import obtainSpriteAnimationImages
from SoundController import playExplosionSound
import ShipController
class GameStatus(): 

  def __init__(self):
    self.player_sprites = pygame.sprite.Group()
    self.player_bullet_sprites = pygame.sprite.Group()
    self.enemy_sprites = pygame.sprite.Group()
    self.asteroid_sprites = pygame.sprite.Group()
    self.score = 0
    self.isGameStillRunning = True
    self.clock = pygame.time.Clock()
    self.explosion_animation_images = obtainSpriteAnimationImages('./images/explosion/8BitExplosionData.png')

  def addPlayerSprites(self, listOfSprites: List[Sprite]) -> None: 
    self.player_sprites.add(listOfSprites)

  def addPlayerSprite(self, sprite: Sprite) -> None: 
    self.player_sprites.add(sprite)

  def addPlayerBulletSprites(self, sprite: List[Sprite]) -> None: 
    self.player_bullet_sprites.add(sprite)

  def addPlayerBulletSprite(self, sprite: Sprite) -> None: 
    self.player_bullet_sprites.add(sprite)

  def addAsteroidSprite(self, sprite:Sprite) -> None: 
    self.asteroid_sprites.add(sprite)

  def addAsteroidSprites(self, sprite: List[Sprite]) -> None: 
    self.asteroid_sprites.add(sprite)

  def updateSprites(self, screen: pygame.Surface) -> None:
    self.player_sprites.update()
    for sprite in self.player_sprites: 
      screen.blit(sprite.image, sprite.rect)

    for sprite in self.asteroid_sprites: 
      screen.blit(sprite.image, sprite.rect)

    for sprite in self.player_bullet_sprites: 
      screen.blit(sprite.image, sprite.rect)

    self.dt = self.clock.tick(60)

  def getExplosionAnimationImage(self): 
    return self.explosion_animation_images
  
  
  def handleAsteroidBulletCollision(self, asteroid, bullet): 
    """
    Handles the collision between an asteroid and a bullet.
    Reduces asteroid health, triggers explosion animation when health reaches zero,
    and manages the asteroid's animation state.
    Args:
        asteroid: The asteroid sprite that was hit
        bullet: The bullet sprite that hit the asteroid
    """
    if bullet:
        # Reduce asteroid health and remove bullet
        asteroid.health -= 1
        bullet.kill()

        # Trigger explosion when health reaches zero
        if asteroid.health == 0:
            asteroid.should_animate = True
            asteroid.animation_images = self.getExplosionAnimationImage()


  def handleShipAsteroidCollision(self, ship):
      if not ship.should_animate: 
          ship.should_animate = True
          ship.animation_images = self.getExplosionAnimationImage()
          ship.health -= 1
          playExplosionSound()
      

  def handleCollisions(self):
    """
    Handles all collision detection and response in the game.
    """
    # Handle bullet-asteroid collisions
    for asteroid in self.asteroid_sprites:
        for bullet in self.player_bullet_sprites:
          if asteroid.collision_rect.colliderect(bullet.rect):
            self.handleAsteroidBulletCollision(asteroid, bullet)

    for sprite in self.player_sprites: 
        if isinstance(sprite, ShipController.Ship):
            for asteroid in self.asteroid_sprites:
                  if sprite.collision_rect.colliderect(asteroid.collision_rect):
                      self.handleShipAsteroidCollision(sprite)
                      self.asteroid_sprites.empty()
      

  def handleAnimations(self): 
    """
    Updates all sprite animations in the game.
    """
    for asteroid in self.asteroid_sprites: 
        if asteroid.should_animate: 
            asteroid.animate()

    for sprite in self.player_sprites:
        if isinstance(sprite, ShipController.Ship):
          print(sprite.should_animate)
        if isinstance(sprite, ShipController.Ship) and sprite.should_animate:
            sprite.animate()

  def handleDestruction(self): 
    """
    Removes sprites that have completed their destruction sequence.
    """
    for asteroid in self.asteroid_sprites: 
        if asteroid.should_destroy: 
          asteroid.kill()

    for bullet in self.player_bullet_sprites: 
       if bullet.should_destroy: 
          bullet.kill()

    for player_sprite  in self.player_sprites: 
       if player_sprite.should_destroy: 
          player_sprite.kill()