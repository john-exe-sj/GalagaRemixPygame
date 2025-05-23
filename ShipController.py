"""
Ship Controller Module
Handles player ship movement, rotation, and bullet generation.
"""

import pygame
from Sprites import Sprite
import Constants
from GameField import GameStatus
from BulletController import addBullet

class Ship(Sprite):
    """Represents the player's ship in the game."""
    
    def __init__(self) -> None: 
        """Initialize the player's ship with default position and properties."""
        super().__init__()
        self.initializeImage(Constants.SHIP_IMAGE_FILE, Constants.SHIP_DIMMENSION)
        self.initializePosition()
        self.velocity = Constants.SHIP_VELOCITY
        
    def initializePosition(self) -> None:
        """Set initial ship position"""
        self.rect.center  = pygame.display.get_surface().get_rect().center

    def move(self) -> None: 
        """Update ship position based on keyboard input and screen boundaries.
        
        Args:
            gameStat: The game state object containing screen dimensions
        """
        self.pointTowardsMousePointer(Constants.SHIP_ANGLE_OFFSET)
        self.handleMovement()

    def handleMovement(self) -> None:
        """Handle ship movement based on key presses"""
        curr_x, curr_y = self.rect.center
        
        width_of_screen, height_of_screen = pygame.display.get_surface().get_size()

        keys = pygame.key.get_pressed()
        
        # Handle movement based on key presses and screen boundaries
        if keys[pygame.K_a] and curr_x >= 0:  # Left
            self.rect.x -= self.velocity 
        
        if keys[pygame.K_d] and curr_x <= width_of_screen:  # Right
            self.rect.x += self.velocity 

        if keys[pygame.K_w] and curr_y >= 0:  # Up
            self.rect.y -= self.velocity

        if keys[pygame.K_s] and curr_y <= height_of_screen:  # Down
            self.rect.y += self.velocity

    def generateBullet(self, gameStat: GameStatus) -> None: 
        """Create a new bullet at the ship's current position and angle.
        Args:
            gameStat: The game state object
        """
        addBullet(gameStat, self.rect.center, self.angle + Constants.SHIP_ANGLE_OFFSET) # add bullet into the game, giving the ship's center position/coordinates. 
