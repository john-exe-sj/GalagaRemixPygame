"""
Sprites Module
Provides base sprite functionality and utility functions for game objects.
Handles rotation, angle calculations, and trajectory computations.
"""

from math import sqrt, atan2, degrees
from pygame.sprite import Sprite
import pygame

def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate the Euclidean distance between two points.
    
    Args:
        x1 (float): X coordinate of first point
        y1 (float): Y coordinate of first point
        x2 (float): X coordinate of second point
        y2 (float): Y coordinate of second point
        
    Returns:
        float: The distance between the two points
    """
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def rotate(sprite: Sprite, angle_change: int, offset=0):
    """Rotate a sprite's image by the given angle.
    
    Args:
        sprite (Sprite): The sprite to rotate
        angle_change (int): The angle to rotate by in degrees
        offset (int, optional): Additional angle offset. Defaults to 0.
    """
    # Update the angle
    sprite.angle += angle_change + offset
    # Keep angle between 0 and 360 degrees
    sprite.angle = sprite.angle % 360
    # Rotate the image
    sprite.image = pygame.transform.rotate(sprite.original_image, sprite.angle)
    # Get the new rect and maintain the center position
    old_center = sprite.rect.center
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = old_center

def calculateAngleToTarget(origin_x, origin_y, target_x, target_y, old_angle, offset=0): 
    """Calculate the angle needed to point from origin to target.
    
    Args:
        origin_x: X coordinate of the origin point
        origin_y: Y coordinate of the origin point
        target_x: X coordinate of the target point
        target_y: Y coordinate of the target point
        old_angle: Current angle of the sprite
        offset: Additional angle offset
        
    Returns:
        float: The angle in degrees to point at the target
    """
    v_x, v_y = target_x - origin_x, target_y - origin_y
    v_angle = atan2(v_y, -v_x)

    if abs(calculate_distance(origin_x, origin_y, target_x, target_y)) < 70: 
        return old_angle
    else: 
        return degrees(v_angle) + offset

def calculateTrajectoryVector(origin_x, origin_y, target_x, target_y):
    """Calculate a normalized vector from origin to target.
    
    Args:
        origin_x: X coordinate of the origin point
        origin_y: Y coordinate of the origin point
        target_x: X coordinate of the target point
        target_y: Y coordinate of the target point
        
    Returns:
        tuple: Normalized (x, y) vector pointing from origin to target
    """
    v_x, v_y = target_x - origin_x, target_y - origin_y
    unit_vector = sqrt(v_x ** 2 + v_y ** 2)
    try: 
        return (v_x / unit_vector, v_y / unit_vector)
    except Exception as e: 
        print(e, "Failure to calculate vector in Sprites Wrapper Class")

class Sprite(Sprite):
    """Base sprite class with rotation and targeting capabilities."""

    def __init__(self):
        """Initialize the sprite with default properties."""
        super().__init__()
        self.angle = 0
  
    def rotateSprite(self, angle_of_change): 
        """Rotate the sprite by the given angle.
        
        Args:
            angle_of_change: The angle to rotate by in degrees
        """
        rotate(self, angle_of_change)

    def pointTowardsMousePointer(self, offset=0):
        """Make the sprite point towards the current mouse position.
        
        Args:
            offset: Additional angle offset
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Calculate angle from sprite to mouse (origin to target)
        self.angle = calculateAngleToTarget(self.rect.x, self.rect.y, mouse_x, mouse_y, self.angle, offset)
        
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def calculateTrajectoryToMouse(self): 
        """Calculate a normalized vector pointing towards the mouse.
        
        Returns:
            tuple: Normalized (x, y) vector pointing towards mouse position
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Calculate vector from bullet to mouse (target - origin)
        v_x = mouse_x - self.rect.x
        v_y = mouse_y - self.rect.y
        # Normalize the vector
        unit_vector = sqrt(v_x ** 2 + v_y ** 2)
        try:
            return (v_x / unit_vector, v_y / unit_vector)
        except Exception as e:
            print(e, "Failure to calculate vector in calculateTrajectoryToMouse")
            return (0, 0)  # Return zero vector if calculation fails


     


  
    