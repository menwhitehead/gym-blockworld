import logging
from blockworld.envs.blockworld_env import BlockworldEnv
from blockworld.envs.engine.tasks.BigWorld import *

logger = logging.getLogger(__name__)

class BlockworldBigworld(BlockworldEnv):

    def __init__(self):
        self.setup(BigWorld())
