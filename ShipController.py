"""
Ship Controller Module
Handles player ship movement, rotation, and bullet generation.
"""

import pygame
from Sprites import Sprite
import Constants
from GameField import GameStatus
from BulletController import addBullet

SHIP_ANGLE_OFFSET = 110
class Ship(Sprite):
    """Represents the player's ship in the game."""
    
    def __init__(self): 
        """Initialize the player's ship with default position and properties."""
        super().__init__()
        # Store the original image for rotation
        self.original_image = pygame.transform.scale(
            pygame.image.load('./images/ship.png'), 
            Constants.SHIP_DIMMENSION
        )
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.velocity = Constants.SHIP_VELOCITY
        self.rect.x = Constants.X_SHIP_STARTPOINT
        self.rect.y = Constants.Y_SHIP_STARTPOINT

    def move(self, gameStat: GameStatus) -> None: 
        """Update ship position based on keyboard input and screen boundaries.
        
        Args:
            gameStat: The game state object containing screen dimensions
        """
        curr_x_ship_coord, curr_y_ship_coord = self.rect.x, self.rect.y
        width_of_screen, height_of_screen = pygame.display.get_surface().get_size()

        keys = pygame.key.get_pressed()
        self.pointTowardsMousePointer(Constants.SHIP_ANGLE_OFFSET)
        
        # Handle movement based on key presses and screen boundaries
        if keys[pygame.K_a] and curr_x_ship_coord >= 0:  # Left
            self.rect.x -= self.velocity 
        
        if keys[pygame.K_d] and curr_x_ship_coord <= width_of_screen:  # Right
            self.rect.x += self.velocity 

        if keys[pygame.K_w] and curr_y_ship_coord >= 0:  # Up
            self.rect.y -= self.velocity

        if keys[pygame.K_s] and curr_y_ship_coord <= height_of_screen:  # Down
            self.rect.y += self.velocity
        
        gameStat.updateShipCoord((self.rect.x, self.rect.y))

    def generateBullet(self, gameStat: GameStatus) -> None: 
        """Create a new bullet at the ship's current position and angle.
        
        Args:
            gameStat: The game state object
        """
        addBullet(gameStat, (self.rect.x, self.rect.y), self.angle + Constants.SHIP_ANGLE_OFFSET)
