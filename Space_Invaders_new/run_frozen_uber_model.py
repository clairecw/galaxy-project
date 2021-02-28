
import os
import atari_zoo
import tensorflow as tf
import gym
from control_map import *
from bar import *
import random

"""## Download trained model and precomputed rollout data"""

import atari_zoo
from atari_zoo import MakeAtariModel
from atari_zoo.rollout import generate_rollout
from pylab import *
import matplotlib.pyplot as plt
import argparse
#from utils import *
#from models import *
#from ga_vis import create_ga_model 
import pickle
from time import sleep

import lucid
from lucid.modelzoo.vision_base import Model
from lucid.misc.io import show
import lucid.optvis.objectives as objectives
import lucid.optvis.param as param
import lucid.optvis.transform as transform
import lucid.optvis.render as render
import tensorflow as tf

from atari_zoo import MakeAtariModel
from lucid.optvis.render import import_model
import gym
import atari_zoo.atari_wrappers as atari_wrappers
import numpy as np
import random
from atari_zoo.dopamine_preprocessing import AtariPreprocessing as DopamineAtariPreprocessing	
from atari_zoo.atari_wrappers import FireResetEnv, NoopResetEnv, MaxAndSkipEnv,WarpFrameTF,FrameStack,ScaledFloatFrame 

algo = "a2c" #or try.... es, ga, dqn, a2c, apex
env = "SpaceInvadersNoFrameskip-v4"  #or try... ZaxxonNoFrameSkip-v4
run_id = 2
tag = "final"
m = MakeAtariModel(algo,env,run_id,tag)()
#from machado
sticky_action_prob = 0.0

preprocessing = 'np'

m.load_graphdef()

#modify graphdef with gaussian noise
layer_names = [z['name'] for z in m.weights]

config = tf.ConfigProto(
    device_count = {'GPU': 0}
)
config.gpu_options.allow_growth=True

from gym.envs.classic_control import rendering
def repeat_upsample(rgb_array, k=1, l=1, err=[]):
    return np.repeat(np.repeat(rgb_array, k, axis=0), l, axis=1)


with tf.Graph().as_default() as graph, tf.Session(config=config) as sess:
    if preprocessing == 'dopamine': #dopamine-style preprocessing
        env = gym.make(m.environment)
        if hasattr(env,'unwrapped'):
            env = env.unwrapped
        env = DopamineAtariPreprocessing(env)
        env = FrameStack(env, 4)
        env = ScaledFloatFrame(env,scale=1.0/255.0)
    elif preprocessing == 'np': #use numpy preprocessing
        env = gym.make(m.environment)
        env = atari_wrappers.wrap_deepmind(env, episode_life=False,preproc='np')
    else:  #use tensorflow preprocessing
        env = gym.make(m.environment)
        env = atari_wrappers.wrap_deepmind(env, episode_life=False,preproc='tf')

    nA = env.action_space.n
    X_t = tf.placeholder(tf.float32, [None] + list(env.observation_space.shape))

    T = import_model(m,X_t,X_t)
    action_sample = m.get_action(T)

    #get intermediate level representations
    activations = [T(layer['name']) for layer in m.layers]
    high_level_rep = activations[-2] #not output layer, but layer before

    sample_observations = []
    sample_frames = []
    sample_ram = []
    sample_representation = []
    sample_score = []
    actions = []

    obs = env.reset()

    ep_count = 0
    rewards = []; ep_rew = 0
    frame_count = 0

    prev_action = None

    render = True
    verbose = True

    viewer = rendering.SimpleImageViewer()

    pygame.init()
    screen = pygame.display.set_mode((800,800))
    clock = pygame.time.Clock()
    bar_obj = Bar(screen)
    bar = pygame.sprite.GroupSingle(bar_obj)
    
    # Evaluate policy over test_eps episodes
    while ep_count < 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    bar.sprite.up(100)
                if event.key == pygame.K_DOWN:
                    bar.sprite.down(5)

        screen.fill((30,30,30))
        bar.draw(screen)
        bar.update()
        pygame.display.update()
        clock.tick(10)

        if render:
            rgb = env.render('rgb_array')
            upscaled = repeat_upsample(rgb,4, 4)
            viewer.imshow(upscaled)
            
        train_dict = {X_t:obs[None]}
        results = sess.run([action_sample,high_level_rep], feed_dict=train_dict)

        #grab action
        act = results[0]

        if bar_obj.randomize and random.uniform(0, 1) < bar_obj.prob:
            act = np.array([env.action_space.sample()])
            print(act)
        actions.append(act[0])

        # translate to amy
        # eye_movement = act_to_eyes[act]

        #get high-level representation
        representation = results[1][0]

        frame = env.render(mode='rgb_array')
        sample_frames.append(np.array(frame,dtype=np.uint8))
        sample_ram.append(env.unwrapped._get_ram())
        sample_representation.append(representation)
        sample_observations.append(np.array(obs))

        sample_score.append(ep_rew)

        if prev_action != None and random.random() < sticky_action_prob:
            act = prev_action

        prev_action = act

        obs, rew, done, info = env.step(np.squeeze(act))

        ep_rew += rew
        frame_count+=1

        if done:
            obs = env.reset()
            ep_count += 1
            rewards.append(ep_rew)
            ep_rew = 0.

    if verbose:
        print("Avg. Episode Reward: ", np.mean(rewards))
        print("rewards:",rewards)
        print("frames:",frame_count)

    results = {'observations':sample_observations,'frames':sample_frames,'ram':sample_ram,'representation':sample_representation,'score':sample_score,'ep_rewards':rewards,'actions':actions}
