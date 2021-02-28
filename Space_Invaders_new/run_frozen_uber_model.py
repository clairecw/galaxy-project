
import os
import atari_zoo
import tensorflow as tf
import gym
from control_map import *
from bar import *
import random
from queue import Queue 
from threading import Thread 
import fam_feud as ff

from pygame import *

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

class Person:
    def __init__(self, x, y):
        self.BASE_PATH = os.path.abspath(os.path.dirname(__file__))
        self.IMAGE_PATH = self.BASE_PATH + '/images/'
        self.person = image.load(self.IMAGE_PATH + self.gen_name("center", False)).convert()
        self.x = x
        self.y = y

        self.target_width = 300
        self.target_height = int(self.target_width / (self.person.get_width() / self.person.get_height()))
        # import pdb; pdb.set_trace()
        self.person = pygame.transform.scale(self.person, (self.target_width, self.target_height))
        
    def gen_name(self, action, is_mad):
        mad_string = "_mad" if is_mad else ""
        name =  "jc_" + action + mad_string + ".png"
        return name
    def update(self, action, is_match):
        self.person = image.load(self.IMAGE_PATH + self.gen_name(action, not is_match)).convert()
        self.person = pygame.transform.scale(self.person, (self.target_width, self.target_height))

    def draw(self, screen):
        self.person = pygame.transform.scale(self.person, (self.target_width, self.target_height))
        screen.blit(self.person, (self.x, self.y))

class TextBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.txt_surface = pygame.font.SysFont("verdana", 20).render(text, True, self.color)
        self.active = False

    def update(self, text):
        self.text = text
        self.txt_surface = pygame.font.SysFont("verdana", 20).render(text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.fsize = 22
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.txt_surface = pygame.font.SysFont("verdana", self.fsize).render(text, True, self.color)
        self.active = True

    def handle_event(self, event):
        ans = ''
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = True
            # Change the current color of the input box.
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    ans = self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = pygame.font.SysFont("verdana", self.fsize).render(self.text, True, self.color)
        return ans

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

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

def bar_loop_shit(q, q_actions):
    pygame.init()
    screen = pygame.display.set_mode((1200,800))
    clock = pygame.time.Clock()
    bar_obj = Bar(screen, 0, 0)
    bar = pygame.sprite.GroupSingle(bar_obj)

    input_box1 = InputBox(10, 150, 140, 32)
    input_boxes = [input_box1]
    randomize = False
    prob = 0

    feud = ff.FamFeud()
    idx, qn = feud.draw_next_q()
    leftcoord = 850
    jc = Person(300, 300)
    lastscoreText = TextBox(leftcoord, 5, 140, 32, text="Previous question answers:")
    prevansboxes = [
        TextBox(leftcoord, 40 + 20 * i, 140, 20, text="") for i in range(10)
    ]

    while True:
        titleText = TextBox(20, 100, 140, 32, text=qn)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
            for box in input_boxes:
                ans = box.handle_event(event)
                if ans:
                    score, sols = feud.score_ans(idx, ans)
                    for i, sol in enumerate(sols):
                        prevansboxes[i].update(sol)
                    while i < len(prevansboxes):
                        prevansboxes[i].update("")
                        i += 1

                    if score > 0:
                        bar.sprite.up(score)
                    else:
                        bar.sprite.down(5)

                    idx, qn = feud.draw_next_q()
                    titleText = TextBox(20, 100, 140, 32, text=qn)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes + prevansboxes:
            box.draw(screen)
        titleText.draw(screen)
        lastscoreText.draw(screen)
        bar.draw(screen)
        bar.update()

        

        if bar_obj.randomize and random.uniform(0, 1) < bar_obj.prob:
            randomize = bar_obj.randomize
            prob = bar_obj.prob

        q.put((randomize, prob))
        act, true_act = q_actions.get()
        jc.draw(screen)
        jc.update(act_to_eyes[act[0]], act==true_act)
        # print(act == true_act)
        

        pygame.display.flip()
        clock.tick(10)

def play_atari(q, q_actions):
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
        
        # Evaluate policy over test_eps episodes
        while ep_count < 10:
            
            if render:
                rgb = env.render('rgb_array')
                upscaled = repeat_upsample(rgb, 3, 3)
                viewer.imshow(upscaled)
                
            train_dict = {X_t:obs[None]}
            results = sess.run([action_sample,high_level_rep], feed_dict=train_dict)

            #grab action
            act = results[0]
            true_act = act
            randomize, prob = q.get()
            if randomize and (2 * random.uniform(0, 1)) < prob:
                true_act = np.array([env.action_space.sample()])
            q_actions.put((act, true_act))
            act = true_act
                # print(act)
            actions.append(act[0])

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

q = Queue() 
q_actions = Queue()
t1 = Thread(target = play_atari, args =(q, q_actions, )) 
t1.start()

bar_loop_shit(q, q_actions)

