import pygame
import Constants
from Sprites import Sprite
#from GameField import GameStatus


class Button(Sprite): 

    def __init__(self):
        super().__init__()

    def clicked(self) -> bool:
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())
    
class ResetButton(Button): 
    def __init__(self):
        super().__init__()
        self.initializeImage(Constants.RESET_BUTTON_IMAGE, Constants.RESET_BUTTON_DIMMENSION)
        self.rect.center = pygame.display.get_surface().get_rect().center

# TODO-OPTIONAL: 
#    - Create a QuitButton class that inherits from Button, place it below ResetButton