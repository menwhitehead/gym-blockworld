"""
Walkway task specific code
"""

import random
from blockworld.envs.engine.tasks.Task import Task
from blockworld.envs.engine.ActionSet import *
from blockworld.envs.engine.game_config import *

class Walkway(Task):

    def __init__(self, pwidth=1, plength=100):
        super(Walkway, self).__init__()
        self.path_length = plength
        self.path_width = pwidth

        # self.MAXIMUM_GAME_FRAMES = max_frames
        self.actions = [GO_FORWARD, GO_BACKWARD, ROTATE_UP, ROTATE_DOWN, ROTATE_RIGHT, ROTATE_LEFT]

    def generateGameWorld(self, filename):
        locs = []
        locs = self.generateWalkwayWorld(locs)
        self.saveWorld(locs, filename)

    def generateWalkwayWorld(self, locations):
        # a block to start on
        locations.append((0, Task.GROUND, 0, "STONE"))

        # Make a snaking walkway
        i = 0
        j = 0
        block_count = 0
        while block_count < self.path_length:
            locations.append((i, Task.GROUND, j, "STONE"))
            new_i = random.randrange(i-1, i+2) #random.choice([i-1, i+1]) #
            for k in xrange(self.path_width):
                # -2 to move have agent in center
                if new_i+k-self.path_width/2 != i:
                    locations.append((new_i+k-(self.path_width/2), Task.GROUND, j, "STONE"))
            j = j-1
            i = new_i
            block_count += 1

        return locations



    def getReward(self, player, action_index):
        # Initialize a new reward for this current action
        reward = STARTING_REWARD

        # Check if farther than before. Then give reward.
        # Going away in the z dir is negative.
        # by rounding, the max score should be the z dist of the path
        if (player.position[2] < player.prev_max_z):
          player.prev_max_z = player.position[2]
          reward = 1.0
        elif (player.position[2] > player.prev_max_z):
          reward = -1.0

        if (player.position[1] < -1):
            reward = -1
        if (player.position[1] < -400):
            player.should_end_game = True
            player.prev_max_distance = 0

        #print ("Player reward = ", reward)
        return reward
