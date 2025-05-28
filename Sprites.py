"""
Sprites Module
Provides base sprite functionality and utility functions for game objects.
Handles rotation, angle calculations, and trajectory computations.
"""

from math import sqrt, atan2, degrees, radians, cos, sin
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
        self.should_animate = False
        self.should_destroy = False
        self.animation_images = None
        self.animation_idx = 0

    def move(self) -> None:
        """Base movement method that should be overridden by subclasses that need movement.
        This method provides a common interface for sprite movement in the game.
        Subclasses should implement their specific movement logic by overriding this method.
        """
        pass

    def initializeImage(self, image_file: str, dimmenions: tuple):
        """Initialize the ship's image and rect"""
        self.original_image = pygame.transform.scale(
            pygame.image.load(image_file), 
            dimmenions
        )
        self.image = self.original_image
        self.rect = self.image.get_rect()
  
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
        self.angle = calculateAngleToTarget(
            self.rect.center[0], 
            self.rect.center[1], 
            mouse_x, 
            mouse_y, 
            self.angle, 
            offset
        )
        
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
        
    def calculateTrajectoryToSprite(self, sprite:Sprite): 
        """Calculates a normalized vector pointing towards another Sprite object. 
        Args: 
            sprite: a specified sprite to create a trajectory for
        """
        self.trajectory_vx_vy = calculateTrajectoryVector(
            self.rect.x, 
            self.rect.y, 
            sprite.rect.x, 
            sprite.rect.y
        )

    def calculateTrajectoryFromAngle(self, angle: float) -> tuple:
        """Calculate a normalized vector based on an angle in degrees.
        Args:
            angle (float): The angle in degrees (0 is right, 90 is down, 180 is left, 270 is up)
        Returns:
        tuple: Normalized (x, y) vector pointing in the direction of the angle
        """
        # Convert angle to radians
        angle_rad = radians(angle)
        # Calculate the x and y components
        # Note: In Pygame, y is positive downward, so we negate the y component
        x = cos(angle_rad)
        y = -sin(angle_rad)
        self.trajectory_vx_vy = (x, y)

    def kill(self) -> None:
        super().kill()
        del self

    def animate(self):
        """
        Handles the explosion animation sequence for an asteroid.
        When triggered, cycles through explosion animation frames and marks the asteroid for destruction
        when the animation completes.
        """
        # Initialize explosion if not already started
        if not self.should_animate:
            self.should_animate = True
            return

        # Check if we have more frames to animate
        if int(self.animation_idx) - 1 < len(self.animation_images):
            # Get the current frame and apply transformations
            current_frame = self.animation_images[int(self.animation_idx) - 1]
            self.image = pygame.transform.scale(
                pygame.transform.rotate(current_frame, self.angle),
                self.dimmensions
            )

            # Maintain the asteroid's position during animation
            old_image_rect_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_image_rect_center
            # Advance to next frame
            self.animation_idx += 1
        else:
            # Animation complete - mark for destruction
            self.should_animate = False
            self.should_destroy = True