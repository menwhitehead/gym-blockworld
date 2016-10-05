import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='Blockworld-v0',
    entry_point='blockworld.envs:BlockworldEnv',
    timestep_limit=1000,
    reward_threshold=1.0,
    nondeterministic = True,
)

register(
    id='BlockworldWalkway-v0',
    entry_point='blockworld.envs:BlockworldWalkway',
    timestep_limit=100,
    reward_threshold=1.0,
    nondeterministic = True,
)

register(
    id='BlockworldBigworld-v0',
    entry_point='blockworld.envs:BlockworldBigworld',
    timestep_limit=2500,
    reward_threshold=1.0,
    nondeterministic = True,
)
