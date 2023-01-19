from Sprites import Sprite
import Constants
import pygame


class Bullet(Sprite):
    def __init__(self, coord: tuple, isHeroBullet: bool): 
        super().__init__()
        fixedImage = pygame.transform.scale(pygame.image.load('./images/bullet.png'), (10,20))
        self.image =  fixedImage
        self.rect = self.image.get_rect()
        self.rect.x = coord[0] + Constants.BULLET_OFFSET_X
        self.rect.y = coord[1] + Constants.BULLET_OFFSET_Y
        self.hasBeenFired = False
        self.BelongsToHero = isHeroBullet 

    def updateBulletXYCoord(self, gameStat): 

        #print(self.rect.x, ":", self.rect.y)
        if(self.BelongsToHero): 
            self.rect.y -= Constants.BULLET_VELOCITY
        
        #else: TODO: Unblock this when enemy ships have developed ai and bullet placement is fixed. 
        #    self.rect.y += Constants.BULLET_VELOCITY

        if(self.rect.y <= 0): 
            removeBullet(gameStat, self)

def updateBullets(gameStat) -> None: 

    for bullet in gameStat.listOfActiveBullets: 
        bullet.updateBulletXYCoord(gameStat)

def addBullet(gameStat, coord: tuple, isHeroBullet: bool) -> None:
    newBullet = Bullet(coord, isHeroBullet)
    gameStat.listOfActiveBullets.append(newBullet)
    gameStat.addSprite(newBullet)
    #print(self.listOfActiveBullets, " :list of active bullets")
    #print(self.sprites, ": list of sprites")
  
def removeBullet(gameStat, bullet: Bullet): 
    gameStat.listOfActiveBullets.remove(bullet)
    gameStat.sprites.remove(bullet)
    #print(self.listOfActiveBullets, " :list of active bullets")
    #print(self.sprites, ": list of sprites")

