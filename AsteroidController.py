from Sprites import Sprite, calculateTrajectoryVector
from GameField import GameStatus
from ShipController import Ship
from random import choice, randint
import pygame
import Constants

class Asteroid(Sprite):
    """
    Represents an asteroid in the game. Asteroids are destructible objects that move across the screen
    and can be shot by the player. Their health and size are inversely proportional.
    """
    def __init__(self, ship: Ship):
        """
        Initialize a new asteroid with random properties.

        Args:
            ship (Ship): The player's ship, used to calculate initial trajectory
        """
        super().__init__()

        # Initialize asteroid with random size and image
        random_size = randint(*Constants.ASTEROID_DIMMENSIONS)
        self.initializeImage(
            choice(Constants.ASTEROID_IMAGE_FILES), 
            (random_size, random_size), 
        )
        
        # Set initial position and movement properties
        self.positionRandomlyWithinScreen()
        self.calculateTrajectoryToSprite(ship)
        self.speed = randint(*Constants.ASTEROID_SPEED)
        self.rotation_speed = randint(*Constants.ASTEROID_ROTATION_SPEED)

        # Set health based on size (larger asteroids have more health)
        if 100 <= random_size <= 150: 
            self.health = 2
        elif 150 < random_size < 170: 
            self.health = 3
        else: 
            self.health = 5

    def positionRandomlyWithinScreen(self) -> None:
        """Position the asteroid randomly within the screen boundaries."""
        screen = pygame.display.get_surface()
        screen_width, screen_height = screen.get_size()
        
        self.rect.x = randint(0, screen_width - self.rect.width)
        self.rect.y = randint(0, screen_height - self.rect.height)

    def move(self) -> None:
        """
        Update asteroid position based on its trajectory and handle screen wrapping.
        Asteroids that move off-screen will wrap around to the opposite side.
        """
        screen_width, screen_height = pygame.display.get_surface().get_size()
        v_x, v_y = self.trajectory_vx_vy

        # Update position
        self.rect.x += v_x * self.speed
        self.rect.y += v_y * self.speed
        self.rotateSprite(self.rotation_speed)

        # Handle screen wrapping
        if self.rect.x < 0: 
            self.rect.x = screen_width
        if self.rect.x > screen_width: 
            self.rect.x = 0
        if self.rect.y < 0: 
            self.rect.y = screen_height
        if self.rect.y > screen_height: 
            self.rect.y = 0

def updateAsteroids(gameStat: GameStatus) -> None:
    """
    Update all asteroids in the game, handling movement and collision detection.

    Args:
        gameStat (GameStatus): The current game state containing all game objects
    """
    for asteroid in gameStat.asteroid_sprites:
        asteroid.move()

        # Check for collisions with player bullets
        colliding_bullet = asteroid.rect.collideobjects(list(gameStat.player_bullet_sprites))
        if colliding_bullet:
            # Handle asteroid damage
            if asteroid.health == 0:
                asteroid.kill()
            else:
                asteroid.health -= 1
            
            # Remove the colliding bullet
            colliding_bullet.kill()
            continue
            


    
        
