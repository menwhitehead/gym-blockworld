import Action
import random
import os


##############################
# Frequently Changed Globals #
##############################

# The width and height of the viewable game window (always square)
WINDOW_SIZE = 600

##############
# Game rules #
##############
# Rewards and penalties must fit into one byte!
# All accumulated rewards also must be non-negative!!!
# Rewards (these are added to reward)

# How much do you get for breaking different blocks?
BLOCK_BREAK_REWARDS = {
    "GRASS":1,
    "STONE":0,
    "BRICK":0
}

# Penalties (these are subtracted from reward)
SWING_PENALTY = 0
EXISTENCE_PENALTY = 0

# If you get all the penalties, then you get zero
STARTING_REWARD = SWING_PENALTY + EXISTENCE_PENALTY
