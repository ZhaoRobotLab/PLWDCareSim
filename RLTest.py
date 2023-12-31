import gymnasium as gym
from RLInterface import PWDSim
from SimManagerJSON import SimManager
gym.register(id='PWDSim-v0', entry_point='RLInterface:PWDSim', kwargs={'sim': PWDSim})

this_sim = SimManager()
env = gym.make('PWDSim-v0', sim=this_sim)
obs = env.reset()

for i in range(5):
    action = env.action_space.sample()
    #Action is expected to be a standard integer
    obs, reward, done, info = env.step(int(action))
    print("Action: " + str(action) + " | Observation: " + str(obs) + " | Reward: " + str(reward) + " | Done: " + str(done) + " | Info: " + str(info))
    if done:
        obs = env.reset()
        print("Done!")
        break