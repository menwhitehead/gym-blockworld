import gym
import blockworld

# env = gym.make('Blockworld-v0')
env = gym.make('BlockworldWalkway-v0')
# env = gym.make('BlockworldBigworld-v0')


env.monitor.start(".", force=True, seed=0)

env.reset()
done = False
while not done:
    env.render()
    #env.step(env.action_space.sample()) # take a random action
    act = env.action_space.sample()
    # act = 5
    observation, reward, done, info = env.step(act)
    # print("ACTION: %d" % act)
    # print("GOT REWARD: %d" % reward)
    # print("OBSERV:", observation)
    if done:
        print("Episode finished")
        break

env.monitor.close()
