"""
Bullet Controller Module
Handles bullet creation, movement, and cleanup in the game.
"""

import math
import pygame
from Sprites import Sprite
import Constants
from SoundController import playPlayerLaserShot
from GameField import GameStatus

class Bullet(Sprite):
    """Represents a bullet in the game that can be fired by the player's ship."""
    
    def __init__(self, coord: tuple, angle: int): 
        """Initialize a new bullet at the given coordinates and angle.
        Args:
            coord (tuple): The (x, y) coordinates of the ship
            angle (int): The angle in degrees at which the bullet should be fired
        """
        super().__init__()
        self.original_image = pygame.transform.scale(
            pygame.image.load(Constants.BULLET_IMAGE_FILE), 
            Constants.BULLET_DIMMENSIONS
        )
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        # Calculate bullet spawn position using ship's diagonal for consistent distance
        self.rect.x = coord[0]
        self.rect.y = coord[1]
        
        self.angle = angle
        self.pointTowardsMousePointer(Constants.BULLET_ANGLE_OFFSET)
        self.trajectory_vx_vy = self.calculateTrajectoryToMouse() # TODO: Once enemy ships are added. Re-configure or make new bullet class

    def updateBulletPosition(self): 
        """Update bullet position and check if it should be removed.
        Args:
            gameStat: The game state object containing screen dimensions
        """
        v_x, v_y = self.trajectory_vx_vy
        self.rect.x += v_x * Constants.BULLET_VELOCITY
        self.rect.y += v_y * Constants.BULLET_VELOCITY

        # Get screen dimensions
        width_of_screen, height_of_screen = pygame.display.get_surface().get_size()
        
        # Remove bullet if it goes off screen
        if (self.rect.y <= 0 or 
            self.rect.y >= height_of_screen or 
            self.rect.x <= 0 or 
            self.rect.x >= width_of_screen):
            removeBullet(self)

def updateBullets(gameStat:GameStatus) -> None: 
    """Update all active bullets in the game.
    Args:
        gameStat: The game state object containing active bullets
    """
    for bullet in gameStat.player_bullet_sprites: 
        bullet.updateBulletPosition()

def addBullet(gameStat: GameStatus, coord: tuple, angle: int) -> None:
    """Create and add a new bullet to the game.
    Args:
        gameStat: The game state object
        coord (tuple): The (x, y) coordinates where the bullet should spawn
        angle (int): The angle in degrees at which the bullet should be fired
    """
    newBullet = Bullet(coord, angle)
    gameStat.addPlayerBulletSprite(newBullet)
    playPlayerLaserShot()
  
def removeBullet(bullet: Bullet): 
    """Remove a bullet from the game and ensure proper cleanup.
    Args:
        bullet (Bullet): The bullet to remove
    """
    bullet.kill()  # Removes from all sprite groups
    del bullet     # Explicitly delete the reference

