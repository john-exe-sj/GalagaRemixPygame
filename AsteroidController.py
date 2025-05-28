from Sprites import Sprite
from GameField import GameStatus
from ShipController import Ship
from SoundController import playExplosionSound
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
        self.dimmensions = (random_size, random_size)
        self.initializeImage(
            choice(Constants.ASTEROID_IMAGE_FILES), 
            self.dimmensions, 
        )
        
        # Set initial position and movement properties
        self.positionOutsideOfScreen()
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

    def positionOutsideOfScreen(self) -> None:
        """
        Position the asteroid randomly outside the screen boundaries.
        This ensures asteroids enter the screen from the edges.
        """
        screen = pygame.display.get_surface()
        screen_width, screen_height = screen.get_size()

        # Define spawn areas outside screen boundaries, refer to PDF.
        left = (-Constants.ASTEROID_SPAWN_PADDING - self.rect.width, -self.rect.width)
        up = left  # Due to pygame's inverted coordinate system
        right = (screen_width + self.rect.width, screen_width + self.rect.width + Constants.ASTEROID_SPAWN_PADDING)
        down = (screen_height + self.rect.height, screen_height + self.rect.height + Constants.ASTEROID_SPAWN_PADDING)

        # Randomly choose spawn position from edges
        self.rect.x = choice((randint(*left), randint(*right)))
        self.rect.y = choice((randint(*up), randint(*down)))

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
        if self.rect.x < (0 - Constants.ASTEROID_SPAWN_PADDING): 
            self.rect.x = screen_width + self.rect.width
        if self.rect.x > (screen_width + Constants.ASTEROID_SPAWN_PADDING): 
            self.rect.x = 0 - self.rect.width
        if self.rect.y < (0 - Constants.ASTEROID_SPAWN_PADDING): 
            self.rect.y = screen_height + self.rect.width 
        if self.rect.y > (screen_height + Constants.ASTEROID_SPAWN_PADDING): 
            self.rect.y = 0 - self.rect.height

def updateAsteroids(gameStat: GameStatus) -> None:
    """
    Updates all asteroid positions in the game.
    Only moves asteroids that are not currently animating.
    
    Args:
        gameStat (GameStatus): The current game state containing all game objects
    """
    for asteroid in gameStat.asteroid_sprites:
        if not asteroid.should_animate: 
            asteroid.move()

# Timer for asteroid spawning
asteroid_timer = 0
def generateAsteroids(gameStat: GameStatus, ship: Ship) -> None:
    """
    Generates new asteroids at random intervals.
    Args:
        gameStat (GameStatus): The current game state containing all game objects
        ship (Ship): The player's ship, used to calculate asteroid trajectories
    """
    time_limit = randint(*Constants.ASTEROID_SPAWN_TIMER_VALUES)
    amount_to_spawn = randint(*Constants.ASTEROID_POSSIBLE_SPAWN_AMOUNT)
    global asteroid_timer

    asteroid_timer += 1
    
    if asteroid_timer >= time_limit: 
        for _ in range(amount_to_spawn): 
            gameStat.addAsteroidSprite(Asteroid(ship))
        asteroid_timer = 0
    
        
