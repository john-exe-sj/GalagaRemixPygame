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
        self.positionRandomlyWithinScreen()
        self.calculateTrajectoryToSprite(ship)
        self.speed = randint(*Constants.ASTEROID_SPEED)
        self.rotation_speed = randint(*Constants.ASTEROID_ROTATION_SPEED)
        self.should_explode = False
        self.should_destroy_asteroid = False
        self.explosion_animation_images = None
        self.explosion_animation_idx = 0

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

    def animateExplosion(self):
        """
        Handles the explosion animation sequence for an asteroid.
        When triggered, cycles through explosion animation frames and marks the asteroid for destruction
        when the animation completes.
        """
        # Initialize explosion if not already started
        if not self.should_explode:
            self.should_explode = True
            return

        # Check if we have more frames to animate
        if int(self.explosion_animation_idx) - 1 < len(self.explosion_animation_images):
            # Get the current frame and apply transformations
            current_frame = self.explosion_animation_images[int(self.explosion_animation_idx) - 1]
            self.image = pygame.transform.scale(
                pygame.transform.rotate(current_frame, self.angle),
                self.dimmensions
            )

            # Maintain the asteroid's position during animation
            old_image_rect_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_image_rect_center

            # Advance to next frame
            self.explosion_animation_idx += 1
        else:
            # Animation complete - mark for destruction
            self.should_explode = False
            self.should_destroy_asteroid = True

def updateAsteroids(gameStat: GameStatus) -> None:
    """
    Updates all asteroids in the game, handling movement, collision detection, and explosion animations.
    
    Args:
        gameStat (GameStatus): The current game state containing all game objects and sprites
    """
    for asteroid in gameStat.asteroid_sprites:
        # Handle collision with player bullets
        colliding_bullet = asteroid.rect.collideobjects(list(gameStat.player_bullet_sprites))
        if colliding_bullet:
            # Reduce asteroid health and remove bullet
            asteroid.health -= 1
            
            # Remove the colliding bullet
            colliding_bullet.kill()

            # Trigger explosion when health reaches zero
            if asteroid.health == 0:
                asteroid.should_explode = True
                playExplosionSound()

        # Handle asteroid state
        if asteroid.should_explode:
            # Initialize and play explosion animation
            asteroid.explosion_animation_images = gameStat.getExplosionAnimationImage()
            asteroid.animateExplosion()
        elif asteroid.should_destroy_asteroid and asteroid in gameStat.asteroid_sprites:
            # Remove asteroid after explosion animation completes
            asteroid.kill()
        else:
            # Normal asteroid movement
            asteroid.move()

# Timer for asteroid spawning
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
    
        
