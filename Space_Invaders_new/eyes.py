
from pygame import *
import sys
from os.path import abspath, dirname
from random import choice
import cv2
from gaze_tracking import GazeTracking

BASE_PATH = abspath(dirname(__file__))
IMAGE_PATH = BASE_PATH + '/images/'
DIRECTIONS = {"up":(0, 1), "down":(0, -1), "left":(-1, 0), "right":(1, 0)}
class PersonWithEyes(object):
    def __init__(self, screen):
        self.person = image.load(IMAGE_PATH + 'amy.png').convert()
        self.eyes = self.person
        self.eyes_rect = self.eyes.get_rect(topleft=(65, 65))
        # self.eyes = image.load(IMAGE_PATH + 'eyes.jpg').convert()
        self.eyes_position = 65
        self.screen = screen
        self.screen.blit(self.person, (0, 0))

    def updateEyes(self, direction):
        self.eyes_rect.x += DIRECTIONS[direction][0]
        self.eyes_rect.y += DIRECTIONS[direction][1]
        self.screen.blit(self.eyes, self.eyes_rect)




screen = display.set_mode((800, 600))
amy = PersonWithEyes(screen)

clock = time.Clock()


while True:
    for direction in DIRECTIONS:
        clock.tick(50)
        amy.updateEyes(direction)
        display.update()
