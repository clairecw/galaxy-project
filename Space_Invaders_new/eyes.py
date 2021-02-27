
from pygame import *
import pygame
import sys
from os.path import abspath, dirname
from random import choice
import cv2
import numpy as np
from skimage import io
from gaze_tracking import GazeTracking

BASE_PATH = abspath(dirname(__file__))
IMAGE_PATH = BASE_PATH + '/images/'
DIRECTIONS = {"up":(0, 10), "down":(0, -10), "left":(-10, 0), "right":(10, 0)}
WHITE = (255, 255, 255)

class PersonWithEyes(object):
    def __init__(self):
        
        self.screen = display.set_mode((1000, 700))
        self.person = image.load(IMAGE_PATH + 'amy.png').convert_alpha()
        self.eyes = image.load(IMAGE_PATH + 'eyes.png').convert_alpha()

        self.target_width = 600
        self.target_height = int(self.target_width * (self.person.get_width() / self.person.get_height()))

        transform.scale(self.person, (self.target_width, self.target_height))
        transform.scale(self.eyes, (self.target_width, self.target_height))
        
        self.x_pos = 70
        self.y_pos = 70

        self.person_rect = self.person.get_rect(topleft=(self.x_pos, self.y_pos))
        self.eyes_rect = self.eyes.get_rect(topleft=(self.x_pos, self.y_pos))

        self.eyelids_rect = Rect(self.x_pos, self.y_pos, self.target_height, self.target_width)

        self.mean_color = self.get_mean_color(self.person)
        # import pdb; pdb.set_trace()
        self.mean_color = self.person.get_at((self.person.get_width() // 2, self.person.get_width() // 2))[:3]

    def get_mean_color(self, surface):
        npimg = surfarray.array3d(surface)
        return tuple(npimg.mean(axis=0).mean(axis=0).astype(int))
        

    def update_eyes(self, direction, center=False, blink=False):
        if not blink:
            if center:
                self.eyes_rect.x = self.x_pos
                self.eyes_rect.y = self.y_pos
            else:
                self.eyes_rect.x += DIRECTIONS[direction][0]
                self.eyes_rect.y += DIRECTIONS[direction][1]

        self.screen.fill(WHITE)
        self.screen.blit(self.eyes, self.eyes_rect)
        if blink:
            self.screen.fill(self.mean_color, rect=self.eyelids_rect)
        self.screen.blit(self.person, (self.x_pos, self.y_pos))
        




amy = PersonWithEyes()

clock = time.Clock()

running = True
currentTime = time.get_ticks()
while running:
    for direction in DIRECTIONS:
        while time.get_ticks() - currentTime < 300:
            continue
        currentTime = time.get_ticks()
        amy.update_eyes(direction)
        display.update()
        while time.get_ticks() - currentTime < 300:
            continue
        currentTime = time.get_ticks()
        amy.update_eyes(None, center=True)
        display.update()
    while time.get_ticks() - currentTime < 300:
        continue
    currentTime = time.get_ticks()
    amy.update_eyes(None, center=False, blink=True)
    display.update()

    while time.get_ticks() - currentTime < 1000:
        continue
    currentTime = time.get_ticks()
    amy.update_eyes(None, center=True, blink=False)
    display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

quit()
