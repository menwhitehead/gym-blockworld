import logging
import math
import gym
from gym import error, spaces
from gym import utils
from gym.utils import seeding
import numpy as np


from blockworld.envs.blockworld_env import BlockworldEnv
from blockworld.envs.engine.tasks.Walkway import *

logger = logging.getLogger(__name__)

WALKWAY_WIDTH = 10
WALKWAY_LENGTH = 100


class BlockworldWalkway(BlockworldEnv):

    def __init__(self):
        self.setup(Walkway(WALKWAY_WIDTH, WALKWAY_LENGTH))
