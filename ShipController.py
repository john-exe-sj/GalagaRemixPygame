"""
Ship Controller Module
Handles player ship movement, rotation, and bullet generation.
"""

import pygame
import Constants
from Sprites import Sprite
from BulletController import addBullet

class Ship(Sprite):
    """Represents the player's ship in the game."""
    
    def __init__(self) -> None: 
        """Initialize the player's ship with default position and properties."""
        super().__init__()
        self.initializeImage(Constants.SHIP_IMAGE_FILE, Constants.SHIP_DIMMENSION)
        self.initializePosition()
        self.velocity = Constants.SHIP_VELOCITY
        self.dimmensions = Constants.SHIP_DIMMENSION
        self.health = 3
        
    def initializePosition(self) -> None:
        """Set initial ship position"""
          # Create a smaller collision rectangle
        self.rect.center = pygame.display.get_surface().get_rect().center
        self.collision_rect = pygame.Rect(0, 0, self.rect.width * 0.4, self.rect.height * 0.4)
        self.collision_rect.center = self.rect.center
        self.collision_rect.center = self.rect.center

    def move(self) -> None: 
        """Update ship position based on keyboard input and screen boundaries.
        
        Args:
            gameStat: The game state object containing screen dimensions and animation images
        """
        if not self.should_animate: 
            self.pointTowardsMousePointer(Constants.SHIP_ANGLE_OFFSET)
            self.handleMovement()
        # Update collision rectangle position
        self.collision_rect.center = self.rect.center

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

    def animate(self):
        super().animate()
        if self.health >= 0: 
            self.should_destroy = False
        elif self.health < -1: 
            self.should_destroy = True
