import pygame
import Constants
from Sprites import Sprite
#from GameField import GameStatus


class ResetButton(Sprite): 

    def __init__(self):
        super().__init__()
        self.initializeImage("./images/resetbutton.png", (200, 100))
        self.rect.center = pygame.display.get_surface().get_rect().center

    def clicked(self) -> bool:
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())