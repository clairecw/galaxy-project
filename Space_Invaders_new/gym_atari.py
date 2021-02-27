"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
import gym
from gaze_tracking import GazeTracking
from control_map import *
from gym.envs.classic_control import rendering
import numpy as np

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

env = gym.make("SpaceInvadersNoFrameskip-v4")
state_dim = env.observation_space.shape[0]
env.reset()
viewer = rendering.SimpleImageViewer()

eyes_action = ""
while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()
    
    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()

    if gaze.is_blinking():
        eyes_action = "blink"
    elif gaze.is_right():
        eyes_action = "right"
    elif gaze.is_left():
        eyes_action = "left"
    elif gaze.is_center():
        eyes_action = "center"
    
    act = eyes_to_act[eyes_action]
    print(act)

    obs, rew, done, info = env.step(act)
    rgb = env.render('rgb_array')
    upscaled = np.repeat(np.repeat(rgb, 4, axis=0), 4, axis=1)
    viewer.imshow(upscaled)