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


class BlockworldEnv(gym.Env):
    metadata = {
        'render.modes' : ['human', 'rgb_array'],
        'video.frames_per_second' : 20
    }

    def setup(self, task):
        self.viewer = pyglet.window.Window(width=WINDOW_SIZE, height=WINDOW_SIZE, visible=False, vsync=False)
        self.game = Game()

        self.p = Player()
        self.p.setTask(task)
        self.game.set_player(self.p)
        self.p.setGame(self.game)

        world_file = "test.txt"
        self.p.task.generateGameWorld(world_file)
        self.game.model.loadMap(world_file)

        opengl_setup()

        shape = (WINDOW_SIZE, WINDOW_SIZE)
        self.observation_space = spaces.Box(np.zeros(shape), np.ones(shape))
        self.action_space = spaces.Discrete(len(self.game.player.task.actions))

        self.curr_screen = np.zeros((WINDOW_SIZE, WINDOW_SIZE, 3), dtype=np.uint8)

        print("Blockworld successfully initialized")

    def update(self):
        """
        Updates the game given the currently set params
        Called from act.
        """
        self.game.update()
        self.viewer.clear()
        self.viewer.switch_to()
        self.viewer.dispatch_events()
        self.game.on_draw()
        self.viewer.flip()

    def _step(self, action):
        self.game.player.performAction(self.game.player.task.actions[action])  # map to task's actions
        self.update()
        reward = float(self.game.player.getReward(action))
        is_game_over = self.game.game_over or self.game.player.endGameEarly()
        self.curr_screen = self._get_obs()
        return self.curr_screen, reward, is_game_over, {}

    def _reset(self):
        self.game.reset()
        self.curr_screen = np.zeros((WINDOW_SIZE, WINDOW_SIZE, 3), dtype=np.uint8)
        return self._get_obs()

    def _get_obs(self):
        # Need to flip OpenGL's screenshot data because it's upside down
        screen = np.flipud(self.game.get_screen())
        result = np.array(screen, dtype='uint8')
        return result.astype(np.uint8)

    def _render(self, mode='human', close=False):
        if close:
            # Since we are rendering with OpenGL,
            # the process of closing is really just making the window invisible
            if self.viewer.visible:
                self.viewer.set_visible(False)
            return

        if mode == 'rgb_array':
            return self.curr_screen
        elif mode == 'human':
            if not self.viewer.visible:
                self.viewer.set_visible(True)
