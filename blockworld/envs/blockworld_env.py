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
        'video.frames_per_second' : 60
    }

    def setup(self, task):
        evaluate = False
        print ("Initialing in evaluate mode: %s" % str(evaluate))
        if (evaluate):
            self.window = Window(width=TEST_WINDOW_SIZE, height=TEST_WINDOW_SIZE, caption='Blockworld', resizable=False, vsync=False)
        else:
            self.window = Window(width=TRAIN_WINDOW_SIZE, height=TRAIN_WINDOW_SIZE, caption='Blockworld', resizable=False, vsync=False)

        self.window.set_phase(evaluate)
        self.p = Player()
        self.p.setTask(task)
        self.window.set_player(self.p)
        self.p.setGame(self.window)
        world_file = "/test%d.txt" % random.randrange(10)
        self.p.task.generateGameWorld(world_file)
        self.window.model.loadMap(world_file)
        opengl_setup()

        shape = (TRAIN_WINDOW_SIZE, TRAIN_WINDOW_SIZE)
        self.observation_space = spaces.Box(np.zeros(shape), np.ones(shape))
        self.action_space = spaces.Discrete(len(self.window.player.task.actions))

        print("Blockworld successfully initialized")

    def update(self):
        """
        Updates the game given the currently set params
        Called from act.
        """
        dt = pyglet.clock.tick()
        self.window.update(dt * 1000)
        self.window.switch_to()
        self.window.dispatch_events()
        self.window.dispatch_event('on_draw')
        self.window.flip()

    def _step(self, action):
        self.window.player.performAction(self.window.player.task.actions[action])  # map to task's actions
        self.update()
        reward = float(self.window.player.getReward(action))
        is_game_over = self.window.game_over or self.window.player.endGameEarly()
        return self._get_obs(), reward, is_game_over, {}

    def _reset(self):
        self.window.reset()
        return self._get_obs()

    def _get_obs(self):
        screen = self.window.get_screen()
        return screen

    def _render(self, mode='human', close=False):
        pass
