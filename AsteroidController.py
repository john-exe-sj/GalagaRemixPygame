from Sprites import Sprite, calculateTrajectoryVector
from ShipController import Ship
from random import choice, randint
import pygame
import Constants

class Asteroid(Sprite):
    def __init__(self, ship:Ship):
        super().__init__()
        self.initializeImage()
        self.positionRandomlyWithinScreen()
        self.calculateTrajectory(ship)
        
    
    def initializeImage(self):
        """Initialize the asteroid's image with random size"""
        size = randint(*Constants.ASTEROID_DIMMENSIONS)
        self.image = pygame.transform.scale(
            pygame.image.load(choice(Constants.ASTEROID_IMAGE_FILES)),
            (size, size)
        )
        self.rect = self.image.get_rect()
    
    def positionRandomlyWithinScreen(self):
        """Position the asteroid randomly on screen"""
        screen = pygame.display.get_surface()
        screen_width, screen_height = screen.get_size()
        
        # Position asteroid randomly within screen bounds
        self.rect.x = randint(0, screen_width - self.rect.width)
        self.rect.y = randint(0, screen_height - self.rect.height)
    
    def calculateTrajectory(self, ship:Ship):
        self.trajectory_vx_vy = calculateTrajectoryVector(
            self.rect.x, 
            self.rect.y, 
            ship.rect.x, 
            ship.rect.y
        )

    def move(self):
        v_x, v_y = self.trajectory_vx_vy
        self.rect.x += v_x * Constants.ASTEROID_SPEED
        self.rect.y += v_y * Constants.ASTEROID_SPEED

def updateAsteroids(gameStat) -> None: 
    for asteroid in gameStat.asteroid_sprites: 
        asteroid.move()
    
        
