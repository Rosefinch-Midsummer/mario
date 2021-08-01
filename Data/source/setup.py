import pygame
from . import constants
from .  import tools

pygame.init()
SCREEN=pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

GRAPHICS = tools.load_graphics('resources/graphics')



