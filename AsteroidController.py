from Sprites import Sprite
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

        # refer to PDF
        left = (-Constants.ASTEROID_SPAWN_PADDING - self.rect.width, -self.rect.width) # left or up
        up = left # due to pygames inverted coordinate system. 
        right = (screen_width + self.rect.width, screen_width + self.rect.width + Constants.ASTEROID_SPAWN_PADDING) # right
        down = (screen_height + self.rect.height, screen_height + self.rect.height + Constants.ASTEROID_SPAWN_PADDING) # down

        self.rect.x = choice((randint(*left),randint(*right))) # chooses either left or right side
        self.rect.y = choice((randint(*up), randint(*down))) # chooses either up or down side

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

asteroid_timer = 0
def generateAsteroids(gameStat: GameStatus, ship: Ship) -> None:
    """Responsible for generating asteroids throughout the game
    Args: 
        gameStat (GameStatus): The current game state containing all game objects
        ship (Ship): The ship the player controls
    """
    time_limit = randint(*Constants.ASTEROID_SPAWN_TIMER_VALUES)
    amount_to_spawn = randint(*Constants.ASTEROID_POSSIBLE_SPAWN_AMOUNT)
    global asteroid_timer

    asteroid_timer += 1
    if asteroid_timer >= time_limit: 
        for _ in range(amount_to_spawn): 
            gameStat.addAsteroidSprite(Asteroid(ship))

        asteroid_timer = 0

            


    
        
