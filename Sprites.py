from math import sqrt, atan2, degrees
from pygame.sprite import Sprite
import pygame

def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
  """
  Calculates the distance between two points (x1, y1) and (x2, y2).
  """
  return sqrt((x2 - x1)**2 + (y2 - y1)**2) # obtains the distance between two points. 


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

def calculateAngleToTarget(origin_x, origin_y, target_x, target_y, old_angle, offset=0): 
  """
  Calculates an angle to point towards given a target (x, y) position
  and an orirgin (x, y) position.
  """
  v_x, v_y = target_x - origin_x, target_y - origin_y
  v_angle = atan2(v_y, -v_x)

  print(calculate_distance(origin_x, origin_y, target_x, target_y))

  if abs(calculate_distance(origin_x, origin_y, target_x, target_y)) < 1: 
    print("case 1")
    return old_angle
  else: 
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
    self.angle = 0
  
  def rotateSprite(self, angle_of_change): 
    rotate(self, angle_of_change)

  def pointTowardsMousePointer(self, offset=0):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Calculate angle from sprite to mouse (origin to target)
    self.angle = calculateAngleToTarget(self.rect.x, self.rect.y, mouse_x, mouse_y, self.angle, offset)
    
    self.image = pygame.transform.rotate(self.original_image, self.angle)
    old_center = self.rect.center
    self.rect = self.image.get_rect()
    self.rect.center = old_center

  def calculateTrajectoryToMouse(self): 
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


     


  
    