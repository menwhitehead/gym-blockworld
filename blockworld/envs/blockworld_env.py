import os, subprocess, time, signal
import gym
from gym import error, spaces
from gym import utils
from gym.utils import seeding
import numpy as np
from os import path
from blockworld.envs.engine.game import *
from blockworld.envs.engine.tasks.Walkway import *

import logging
logger = logging.getLogger(__name__)

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

        shape = (TRAIN_WINDOW_SIZE, TRAIN_WINDOW_SIZE)
        self.observation_space = spaces.Box(np.zeros(shape), np.ones(shape))
        self.action_space = spaces.Discrete(len(self.game.player.task.actions))

        self.curr_screen = np.zeros((TRAIN_WINDOW_SIZE, TRAIN_WINDOW_SIZE, 3), dtype=np.uint8)

        opengl_setup()
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
        return self._get_obs()

    def _get_obs(self):
        screen = self.game.get_screen()
        result = np.array(screen, dtype='uint8')
        return result.astype(np.uint8)

    def _render(self, mode='rgb_array', close=False):
        return self.curr_screen
