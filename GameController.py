"""
Main game field module that handles the core game mechanics and state management.
This module contains the Game class which manages the game loop, sprite groups,
collisions, animations, and other game-related functionality.
"""

import pygame, sys
import Constants
from pygame.locals import QUIT
from typing import List
from Sprites import Sprite
from AnimationController import obtainSpriteAnimationImages
from SoundController import playExplosionSound
from ButtonController import ResetButton
from ShipController import Ship
from CrosshairController import Crosshair
from BulletController import addBullet
from AsteroidController import generateAsteroids

class Game(): 
    """
    Main game state manager that handles all game mechanics and state.
    
    Attributes:
        player_sprites (pygame.sprite.Group): Group containing player-related sprites
        player_bullet_sprites (pygame.sprite.Group): Group containing player bullet sprites
        enemy_sprites (pygame.sprite.Group): Group containing enemy sprites
        asteroid_sprites (pygame.sprite.Group): Group containing asteroid sprites
        score (int): Current game score
        isGameStillRunning (bool): Flag indicating if the game is still active
        clock (pygame.time.Clock): Game clock for controlling frame rate
        screen (pygame.Surface): Main game screen surface
        explosion_animation_images (List): List of explosion animation frames
        player_ship (Ship): Player's ship instance
        crosshair (Crosshair): Crosshair instance for aiming
    """

    def __init__(self, screen: pygame.Surface):
        """Initialize the game state with the given screen surface."""
        self.player_sprites = pygame.sprite.Group()
        self.player_bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.asteroid_sprites = pygame.sprite.Group()

        # TODO-OPTIONAL:
        #   keep track of score and display it onto the screen.
        self.score = 0

        self.isGameStillRunning = True
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.explosion_animation_images = obtainSpriteAnimationImages(Constants.EXPLOSION_IMAGE_FILE)

        self.player_ship = Ship()
        self.crosshair = Crosshair()
        self.addPlayerSprites([self.crosshair, self.player_ship])

    def addPlayerSprites(self, listOfSprites: List[Sprite]) -> None: 
        """Add multiple sprites to the player sprite group."""
        self.player_sprites.add(listOfSprites)

    def addPlayerSprite(self, sprite: Sprite) -> None: 
        """Add a single sprite to the player sprite group."""
        self.player_sprites.add(sprite)

    def addPlayerBulletSprites(self, sprite: List[Sprite]) -> None: 
        """Add multiple bullet sprites to the player bullet group."""
        self.player_bullet_sprites.add(sprite)

    def addPlayerBulletSprite(self, sprite: Sprite) -> None: 
        """Add a single bullet sprite to the player bullet group."""
        self.player_bullet_sprites.add(sprite)

    def addAsteroidSprite(self, sprite:Sprite) -> None: 
        """Add a single asteroid sprite to the asteroid group."""
        self.asteroid_sprites.add(sprite)

    def addAsteroidSprites(self, sprite: List[Sprite]) -> None: 
        """Add multiple asteroid sprites to the asteroid group."""
        self.asteroid_sprites.add(sprite)

    def updateSprites(self) -> None:
        """Update and render all sprites on the screen."""
        self.screen.fill(Constants.SCREEN_COLOR)
        for sprite in self.player_sprites: 
            self.screen.blit(sprite.image, sprite.rect)

        for sprite in self.asteroid_sprites: 
            self.screen.blit(sprite.image, sprite.rect)

        for sprite in self.player_bullet_sprites: 
            self.screen.blit(sprite.image, sprite.rect)

        self.dt = self.clock.tick(60)
        pygame.display.flip()

    def getExplosionAnimationImage(self): 
        """Return the explosion animation frames."""
        return self.explosion_animation_images
  
  
    def handleAsteroidBulletCollision(self, asteroid, bullet): 
        """
        Handle collision between an asteroid and a bullet.
        
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
                playExplosionSound()


    def handleShipAsteroidCollision(self, ship):
        if not ship.should_animate: 
            ship.should_animate = True
            ship.animation_images = self.getExplosionAnimationImage()
            ship.health -= 1
            playExplosionSound()
      

    def handleCollisions(self):
        """Handle all collision detection and response in the game."""
        # Handle bullet-asteroid collisions
        for asteroid in self.asteroid_sprites:
            for bullet in self.player_bullet_sprites:
                if asteroid.collision_rect.colliderect(bullet.rect):
                    self.handleAsteroidBulletCollision(asteroid, bullet)

        for sprite in self.player_sprites: 
            if isinstance(sprite, Ship):
                for asteroid in self.asteroid_sprites:
                    if sprite.collision_rect.colliderect(asteroid.collision_rect):
                        self.handleShipAsteroidCollision(sprite)
                        self.asteroid_sprites.empty()
      

    def handleAnimations(self): 
        """Update all sprite animations in the game."""
        for asteroid in self.asteroid_sprites: 
            if asteroid.should_animate: 
                asteroid.animate()

        for sprite in self.player_sprites:
            if isinstance(sprite, Ship) and sprite.should_animate:
                sprite.animate()

    def handleDestruction(self): 
        """Remove sprites that have completed their destruction sequence."""
        for asteroid in self.asteroid_sprites: 
            if asteroid.should_destroy: 
                asteroid.kill()

        for bullet in self.player_bullet_sprites: 
            if bullet.should_destroy: 
                bullet.kill()

        for player_sprite  in self.player_sprites: 
            if player_sprite.should_destroy: 
                player_sprite.kill()

    def handleButtonGeneration(self):
        """Handle game reset logic and reset button management."""
        # TODO-OPTIONAL: 
        #   - Re-implement and clean up. 
        #   - Add code to generate a QuitButton
        is_player_present = False
        is_reset_button_present = False

        for sprite in self.player_sprites: 
            if isinstance(sprite, Ship):
                is_player_present = True
            elif isinstance(sprite, ResetButton):
                is_reset_button_present = True

        if not is_player_present and not is_reset_button_present:
            self.addPlayerSprite(ResetButton())   
        elif is_player_present:
            for sprite in self.player_sprites: 
                if isinstance(sprite, ResetButton):
                    sprite.kill()
       
    def handleGameEvents(self):
        for event in pygame.event.get(): #grabs all the events in the list
            if event.type == QUIT: #exit button in the window.
                self.isGameStillRunning = False

                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN: # tell pygame to track our "mouse-events" aka if a button was clicked. 

                if pygame.mouse.get_pressed()[0] and self.player_ship in self.player_sprites and self.player_ship.should_animate == False: # checks to see if the left button was clicked and making sure that the mouse is at an appropriate distance. 
                    addBullet(self, self.player_ship.rect.center, self.player_ship.angle + Constants.SHIP_ANGLE_OFFSET)

                if pygame.mouse.get_pressed()[0]:
                    for sprite in self.player_sprites: 
                        if isinstance(sprite, ResetButton):
                            if sprite.clicked():
                                self.player_ship = Ship()
                                self.addPlayerSprite(self.player_ship)
                                for asteroid in self.asteroid_sprites:
                                    asteroid.should_destroy = True 

                        # TODO-OPTIONAL: 
                        #    - Trigger a "quit" if the QuitButton has been "clicked" similarly to how ResetButton was "clicked"
                        #    - Trigger a sound when buttons are clicked
                  
    def handleSpriteMotion(self): 
        for player_sprite in self.player_sprites: 
            player_sprite.move()
        
        for bullet in self.player_bullet_sprites:
            bullet.move()

        for asteroid in self.asteroid_sprites: 
            if not asteroid.should_animate: 
                asteroid.move()

    def handleEnemyAndObstacleGeneration(self): 
        generateAsteroids(self, self.player_ship)


def initiateGameScreen():
    """
    Initialize and return the game screen.
    
    Returns:
        pygame.Surface: The initialized game screen
    """
    pygame.init()
    screen = pygame.display.set_mode(Constants.SCREEN_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption('GalagaRemix')
    return screen
       