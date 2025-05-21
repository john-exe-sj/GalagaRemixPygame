from Sprites import Sprite
import Constants
import pygame


class Crosshair(Sprite): 

    def __init__(self): 
        """Initializes the crosshair."""
        super().__init__()
        self.initalizeImage()

    def initalizeImage(self): 
        """Initalizes the image of the crosshair."""
        self.image = pygame.transform.scale(
            pygame.image.load(Constants.CROSSHAIR_IMAGE_FILE), 
            Constants.CROSSHAIR_DIMMENSIONS
        )

        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()

    def move(self): 
        """Moves the crosshair to the mouse position."""
        self.rect.center = pygame.mouse.get_pos()