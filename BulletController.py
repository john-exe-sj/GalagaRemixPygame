from Sprites import Sprite
import Constants
import pygame
import math

class Bullet(Sprite):
    def __init__(self, coord: tuple, angle: int): 
        super().__init__()
        self.original_image = pygame.transform.scale(pygame.image.load('./images/bullet.png'), Constants.BULLET_DIMMENSIONS)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        # Get the ship's center position
        ship_center_x = coord[0] + Constants.SHIP_DIMMENSION[0] // 2
        ship_center_y = coord[1] + Constants.SHIP_DIMMENSION[1] // 2
        
        # Calculate bullet spawn position based on ship's angle
        # Move bullet forward from ship's center in the direction it's facing
        spawn_distance = Constants.SHIP_DIMMENSION[1] // 2  # Distance from ship's center
        rad_angle = math.radians(angle)
        self.rect.x = ship_center_x + math.cos(rad_angle) * spawn_distance
        self.rect.y = ship_center_y + math.sin(rad_angle) * spawn_distance
        
        self.hasBeenFired = False
        self.angle = angle
        self.pointTowardsMousePointer(Constants.BULLET_ANGLE_OFFSET)
        self.trajectory_vx_vy = self.calculateTrajectoryToMouse()

    def updateBulletXYCoord(self, gameStat): 
        v_x, v_y = self.trajectory_vx_vy
        # Multiply by bullet velocity to control speed
        self.rect.x += v_x * Constants.BULLET_VELOCITY
        self.rect.y += v_y * Constants.BULLET_VELOCITY

        # Remove bullet if it goes off screen
        if self.rect.y <= 0: 
            removeBullet(gameStat, self)

def updateBullets(gameStat) -> None: 

    for bullet in gameStat.listOfActiveBullets: 
        bullet.updateBulletXYCoord(gameStat)

def addBullet(gameStat, coord: tuple, angle:int) -> None:
    newBullet = Bullet(coord, angle)
    gameStat.listOfActiveBullets.append(newBullet)
    gameStat.addSprite(newBullet)
    #print(self.listOfActiveBullets, " :list of active bullets")
    #print(self.sprites, ": list of sprites")
  
def removeBullet(gameStat, bullet: Bullet): 
    gameStat.listOfActiveBullets.remove(bullet)
    gameStat.sprites.remove(bullet)
    #print(self.listOfActiveBullets, " :list of active bullets")
    #print(self.sprites, ": list of sprites")

