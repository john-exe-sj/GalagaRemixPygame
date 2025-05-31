from pygame import mixer
from Constants import PLAYER_LASER_SOUND_FILE, ENEMY_LASER_SOUND_FILE, EXPLOSION_SOUND_FILE
# Initialize the mixer
mixer.init()

player_laser_sound = mixer.Sound(PLAYER_LASER_SOUND_FILE)
enemy_laser_sound = mixer.Sound(ENEMY_LASER_SOUND_FILE)
explosion_sound = mixer.Sound(EXPLOSION_SOUND_FILE)

def playPlayerLaserShot():
    mixer.Sound.play(player_laser_sound)

def playExplosionSound(): 
    mixer.Sound.play(explosion_sound)

# TODO-OPTIONAL: 
#    - Create a sound function that plays when a button is "clicked"