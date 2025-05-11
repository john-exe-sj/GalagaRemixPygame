from Sprites import Sprite
import Constants
import pygame

class Bullet(Sprite):
    def __init__(self, coord: tuple, isHeroBullet: bool, angle: int): 
        super().__init__()
        self.original_image = pygame.transform.scale(pygame.image.load('./images/bullet.png'), Constants.BULLET_DIMMENSIONS)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = coord[0] + Constants.BULLET_OFFSET_X
        self.rect.y = coord[1] + Constants.BULLET_OFFSET_Y
        self.hasBeenFired = False
        self.BelongsToHero = isHeroBullet 
        self.angle = angle
        self.pointTowardsMousePointer(Constants.BULLET_ANGLE_OFFSET)
        self.trajectory_vx_vy = self.calculateTrajectoryToMouse()

    def updateBulletXYCoord(self, gameStat): 

        #print(self.rect.x, ":", self.rect.y)
        v_x, v_y = self.trajectory_vx_vy
        print(v_x, v_y)
        
        #else: TODO: Unblock this when enemy ships have developed ai and bullet placement is fixed. 
        #    self.rect.y += Constants.BULLET_VELOCITY

        if(self.rect.y <= 0): 
            removeBullet(gameStat, self)

def updateBullets(gameStat) -> None: 

    for bullet in gameStat.listOfActiveBullets: 
        bullet.updateBulletXYCoord(gameStat)

def addBullet(gameStat, coord: tuple, isHeroBullet: bool, angle:int) -> None:
    newBullet = Bullet(coord, isHeroBullet, angle)
    gameStat.listOfActiveBullets.append(newBullet)
    gameStat.addSprite(newBullet)
    #print(self.listOfActiveBullets, " :list of active bullets")
    #print(self.sprites, ": list of sprites")
  
def removeBullet(gameStat, bullet: Bullet): 
    gameStat.listOfActiveBullets.remove(bullet)
    gameStat.sprites.remove(bullet)
    #print(self.listOfActiveBullets, " :list of active bullets")
    #print(self.sprites, ": list of sprites")

