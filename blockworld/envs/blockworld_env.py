import os, subprocess, time, signal
import gym
from gym import error, spaces
from gym import utils
from gym.utils import seeding
import numpy as np
from os import path
from blockworld.envs.engine.game import *
from blockworld.envs.engine.tasks.Walkway import *

from gym.envs.classic_control import rendering

import logging
logger = logging.getLogger(__name__)


class BlockworldViewer(object):

    def __init__(self, display=None):
        self.window = None
        self.isopen = False
        self.display = display

    def imshow(self, arr):
        if self.window is None:
            height, width, channels = arr.shape
            self.window = pyglet.window.Window(width=width, height=height, display=self.display)
            self.width = width
            self.height = height
            self.isopen = True
        assert arr.shape == (self.height, self.width, 3), "You passed in an image with the wrong number shape"
        image = pyglet.image.ImageData(self.width, self.height, 'RGB', arr.tobytes(), pitch=self.width * -3)
        self.window.clear()
        self.window.switch_to()
        self.window.dispatch_events()
        image.blit(0,0)
        self.window.flip()

    def close(self):
        if self.isopen:
            self.window.close()
            self.isopen = False

    def __del__(self):
        self.close()

class BlockworldEnv(gym.Env):
    metadata = {
        'render.modes' : ['human', 'rgb_array'],
        'video.frames_per_second' : 20
    }

    def setup(self, task):
        self.game = Game()

        #self.window.set_phase(evaluate)
        self.p = Player()
        self.p.setTask(task)
        self.game.set_player(self.p)
        self.p.setGame(self.game)
        world_file = "test.txt"
        self.p.task.generateGameWorld(world_file)
        self.game.model.loadMap(world_file)
        opengl_setup()

        self.viewer = None

        shape = (TRAIN_WINDOW_SIZE, TRAIN_WINDOW_SIZE)
        self.observation_space = spaces.Box(np.zeros(shape), np.ones(shape))
        self.action_space = spaces.Discrete(len(self.game.player.task.actions))

        self.curr_screen = np.zeros((TRAIN_WINDOW_SIZE, TRAIN_WINDOW_SIZE, 3), dtype=np.uint8)

        print("Blockworld successfully initialized")

    def update(self):
        """
        Updates the game given the currently set params
        Called from act.
        """
        self.game.update(1)


    def _step(self, action):
        self.game.player.performAction(self.game.player.task.actions[action])  # map to task's actions
        self.update()
        reward = float(self.game.player.getReward(action))
        is_game_over = self.game.game_over or self.game.player.endGameEarly()
        self.curr_screen = self._get_obs()
        return self.curr_screen, reward, is_game_over, {}

    def _reset(self):
        self.game.reset()
        self.curr_screen = np.zeros((TRAIN_WINDOW_SIZE, TRAIN_WINDOW_SIZE, 3), dtype=np.uint8)
        return self._get_obs()

    def _get_obs(self):
        screen = self.game.get_screen()
        result = np.array(screen, dtype='uint8')
        return result.astype(np.uint8)

    def _render(self, mode='human', close=False):
        print "MODE:", mode
        # return self.curr_screen

        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return

        if mode == 'rgb_array':
            return self.curr_screen
        elif mode == 'human':
            if self.viewer is None:
                #self.viewer = pyglet.window.Window()
                self.viewer = BlockworldViewer()

            self.viewer.imshow(self.curr_screen)
