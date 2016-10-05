import time
import gym
import blockworld
from pyglet import image

RENDER_MODE = 'human'

#env = gym.make('Blockworld-v0')
#env = gym.make('BlockworldWalkway-v0')
env = gym.make('BlockworldBigworld-v0')

env.monitor.start(".", force=True)#, seed=0)

env.reset()
done = False
start_time = time.time()
frame_number = 0
while not done:
    frame_number += 1
    env.render()
    #env.step(env.action_space.sample()) # take a random action
    act = env.action_space.sample()
    # act = 5
    observation, reward, done, info = env.step(act)
    # print("ACTION: %d" % act)
    # print("GOT REWARD: %d" % reward)
    # print("OBSERV:", observation)
    size, _ = env.observation_space.shape
    # img = image.ImageData(size, size, 'RGB', observation.tobytes(), pitch=size * -3)
    # img.save("screenshots/test%d.jpg" % frame_number)


    curr_time = time.time()
    print "%.4f FPS" % (frame_number / (curr_time - start_time))


    if done:
        print("Episode finished")
        print frame_number
        break

env.monitor.close()
