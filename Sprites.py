from pygame.sprite import Sprite
import pygame
from math import sqrt, atan2, degrees

def rotate(sprite: Sprite, angle_change: int, offset=0):
  """
  Simply rotates an image based on an angle. Offset optional. 
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

def calculateAngleToTarget(origin_x, origin_y, target_x, target_y, offset): 
  """
  Calculates an angle to point towards given a target (x, y) position
  and an orirgin (x, y) position.
  """
  v_x, v_y = target_x - origin_x, target_y - origin_y
  v_angle = atan2(v_y, -v_x)
  return degrees(v_angle) + offset

def calculateTrajectoryVector(origin_x, origin_y, target_x, target_y):
  v_x, v_y = target_x - origin_x, target_y - origin_y
  unit_vector = sqrt(v_x ** 2 + v_y ** 2)
  try: 
    return (v_x / unit_vector, v_y / unit_vector)
  except Exception as e: 
    print(e, "Failure to calculate vector in Sprites Wrapper Class")

class Sprite(Sprite):

  def __init__(self):
    super().__init__()
    self.angle: int
  
  def rotateSprite(self, angle_of_change): 
    rotate(self, angle_of_change)

  def pointTowardsMousePointer(self, offset=0):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    print(f"{mouse_x}: {mouse_y}")
    
    self.angle = calculateAngleToTarget(mouse_x, mouse_y, self.rect.x, self.rect.y, offset)
    
    self.image = pygame.transform.rotate(self.original_image, self.angle)
    old_center = self.rect.center
    self.rect = self.image.get_rect()
    self.rect.center = old_center

  def calculateTrajectoryToMouse(self): 
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return calculateTrajectoryVector(self.rect.x, self.rect.y, mouse_x, mouse_y)


     


  
    