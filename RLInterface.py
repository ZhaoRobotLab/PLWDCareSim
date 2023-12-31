import gymnasium as gym

from gymnasium import spaces
import numpy as np

from SimManagerJSON import SimManager


#RL Caregiver
class PWDSim(gym.Env):
    def __init__(self, sim):
        super(PWDSim, self).__init__()
        self.sim = sim
        self.default_pass="pass1"
        self.sim.doPass(self.default_pass)

        # 4 possible actions: NONE, VERBAL_SUPPORTIVE, VERBAL_NON_DIRECTIVE, VERBAL_DIRECTIVE
        self.action_space = spaces.Discrete(4)

        #Observation space is int completed steps, int completed substeps, bool forgetfulness, bool frustration, bool anger, bool engagement
        self.observation_space = spaces.Box(low=np.array([0,0,0,0,0,0]), high=np.array([100,100,1,1,1,1]), dtype=np.float32)

        self.current_state = None
    def reset(self):
        self.current_state = None
    def step(self, action):
        #First, record the current state of the sim
        self.current_state = self.sim.getCurrentSimState()
        #Then, do a step in the sim
        self.sim.doOneStep(rl_action=action)
        
        new_state = self.sim.getCurrentSimState()

        #######REWARD FUNCTION#######
        #This is not tested yet.#

        #0=STEPS COMPLETED
        #1=SUBSTEPS COMPLETED
        #2=COMBINATION OF BOTH STEP PARAMETERS
        #3=PATIENT STATE
        #4=COMBINATION OF ALL PARAMETERS
        reward_mode = 1
        
        reward = 0

        #0: STEPS COMPLETED
        if reward_mode == 0:
            reward_for_step = 1
    
            steps_before = self.current_state["steps_completed"]
            steps_after = new_state["steps_completed"]
            steps_dif = steps_after - steps_before
            #Did we complete a step?
            if steps_dif > 0:
                reward = reward_for_step
            else:
                reward = 0
        #1: SUBSTEPS COMPLETED
        elif reward_mode == 1:
            reward_for_substep = 1
    
            substeps_before = self.current_state["substeps_completed"]
            substeps_after = new_state["substeps_completed"]
            substeps_dif = substeps_after - substeps_before
            print(f"Substeps before: {substeps_before} | Substeps after: {substeps_after} | Substeps dif: {substeps_dif}")
            #Did we complete a substep?
            if substeps_dif > 0:
                reward = reward_for_substep
            else:
                reward = 0
        #2: COMBINATION OF BOTH
        elif reward_mode == 2:
            reward_for_step = 1
            reward_for_substep = 1
    
            steps_before = self.current_state["steps_completed"]
            steps_after = new_state["steps_completed"]
            steps_dif = steps_after - steps_before
            substeps_before = self.current_state["substeps_completed"]
            substeps_after = new_state["substeps_completed"]
            substeps_dif = substeps_after - substeps_before
            #Did we complete a step?
            if steps_dif > 0:
                reward += reward_for_step
            else:
                reward += 0
            #Did we complete a substep?
            if substeps_dif > 0:
                reward += reward_for_substep
            else:
                reward += 0
        #3: PATIENT STATE
        elif reward_mode == 3:
            reward_for_not_forgetful = 1
            reward_for_not_frustrated = 1
            reward_for_not_angry = 1
            reward_for_engaged = 1

            #Note: this could be done differently, instead also considering only state changes, not just state
            if new_state["forgetfulness"] == False:
                reward += reward_for_not_forgetful
            if new_state["frustration"] == False:
                reward += reward_for_not_frustrated
            if new_state["anger"] == False:
                reward += reward_for_not_angry
            if new_state["engagement"] == True:
                reward += reward_for_engaged
        #4: COMBINATION OF ALL
        elif reward_mode == 4:
            reward_for_step = 1
            reward_for_substep = 1
            reward_for_not_forgetful = 1
            reward_for_not_frustrated = 1
            reward_for_not_angry = 1
            reward_for_engaged = 1

            steps_before = self.current_state["steps_completed"]
            steps_after = new_state["steps_completed"]
            steps_dif = steps_after - steps_before
            substeps_before = self.current_state["substeps_completed"]
            substeps_after = new_state["substeps_completed"]
            substeps_dif = substeps_after - substeps_before
            #Did we complete a step?
            if steps_dif > 0:
                reward += reward_for_step
            else:
                reward += 0
            #Did we complete a substep?
            if substeps_dif > 0:
                reward += reward_for_substep
            else:
                reward += 0
            #Note: this could be done differently, instead also considering only state changes, not just state
            if new_state["forgetfulness"] == False:
                reward += reward_for_not_forgetful
            if new_state["frustration"] == False:
                reward += reward_for_not_frustrated
            if new_state["anger"] == False:
                reward += reward_for_not_angry
            if new_state["engagement"] == True:
                reward += reward_for_engaged
        



        self.current_state = new_state
        #Construct observation given the state
        observation = np.array([new_state["steps_completed"], new_state["substeps_completed"], new_state["forgetfulness"], new_state["frustration"], new_state["anger"], new_state["engagement"]])
        return observation, reward, False, {}

        
 
    


        