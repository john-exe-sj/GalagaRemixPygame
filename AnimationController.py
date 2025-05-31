import pygame
import json
from typing import List
"""
Tutorial References and Credits: 
    CDcodes: "Pygame Sprite Sheet Tutorial: How to Load, Parse, and Use Sprite Sheets"
    - https://www.youtube.com/watch?v=ePiMYe7JpJo
    Clear Code: "Python / Pygame Tutorial: Animations with sprites"
    - https://www.youtube.com/watch?v=MYaxPa_eZS0
"""

def obtainSpriteAnimationImages(filename: str) -> List[pygame.Surface]:
    """Obtains a list of animation images given the file name of a sprite sheet.
    NOTE: the given image file must contain multiple images and must have a .json
    metadata file. 
    Arg: 
        filename String: name of the sprite sheet file
    Return: 
        List[pygame.Surface]: list of animation images pulled from the sprite sheet. 
    """
    sprite_sheet = pygame.image.load(filename).convert()
    sprite_sheet_meta_data_file_name = filename.replace("png", "json")

    data = None
    with open(sprite_sheet_meta_data_file_name) as json_file: 
        data = json.load(json_file)

    try: 
        if not data or not data['frames']: 
            raise Exception(f"data from {filename}, was unable to extract")
        
        num_frames = len(data['frames']) # grab number of frames
        image_names = list(data['frames'].keys()) # obtain frame names for referencing. 
        animation_images = []
        
        for i in range(num_frames):
            # obtains position and dimmensions of an image contained in a sheet.
            sprite_data = data['frames'][image_names[i]]["frame"]
            x_pos, y_pos, width, height = sprite_data["x"], sprite_data["y"], sprite_data["w"], sprite_data["h"]

            # creates a blank surface and sets to our background color. 
            sprite = pygame.Surface((width, height))
            sprite.set_colorkey((0, 0, 0))  # Set black as the transparent color
            # blit the specific section from the sprite sheet to our new surface
            sprite.blit(sprite_sheet, (0, 0), (x_pos, y_pos, width, height))
            animation_images.append(sprite)

        # give our list of surfaces/images to the main sprite
        return animation_images
    
    except Exception as e: 
        print(e)
        return None