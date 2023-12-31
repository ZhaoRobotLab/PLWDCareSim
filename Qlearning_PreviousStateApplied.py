# from numba import jit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ResponseRelevance = {0 : 'NR', 1 : 'IR', 2 : 'RR'}
EmotionPleasure = {-1 : 'Neg', 0 : 'Neu', 1 :'Pos'}
EmotionConfusion = {0 : 'No', 1: 'Yes'}
ActionSpace = {0 : 'ProvideEasyPrompt', 1 : 'ProvideModeratelyPrompt', 2 : 'ProvideDifficultPrompt',
               3 : 'Repeat', 4 : 'Explain', 5 : 'Comfort', 6 : 'GiveChoice'}

# StateMapping = []
# for relevance in range(0,3):
#     for e_pleasure in range(-1,2):
#         for confusion in range(0,2):
#             StateMapping.append([relevance, e_pleasure, confusion, 6*relevance+2*(e_pleasure+1)+confusion])

class Human_Robot_interaction(object):
    def __init__(self):
        self.df = pd.read_excel('PatientModel_v3.xlsx', engine = 'openpyxl')
        # self.df = cudf.read_excel('PatientModel_v2_Copy.xlsx', engine = 'openpyxl')
        # self.df = pd.read_excel(r"G:\My Drive\1ResearchForPhD\Experiment\InteractiveRL_for_HRI_In_Healthcare\InteractiveReinforcementLearningFramework\Simulated Patients\PatientModel_v2_Copy.xlsx")
        self.dimen_StateSpace = 18
        self.dimen_ActionSpace = 6
        self.Num_totalPictures = 15
        self.Num_maximalRound = 50 # Considering ~30min reminiscene
        # self.QuestionOrder = list(range(0,10)); random.shuffle(self.QuestionOrder)
        self.done = False
        # Parameters for immediate reward function
        # self.weight_picture = 0.1
        # self.weight_response = 2 # 1.5; 1
        # self.weight_pleasure = 3
        # self.weight_confusion = 2
        ###### Additional reward consideration
        # self.weight_easy = 0.75
        self.weight_mode = 1.25
        self.weight_diff = 1.5
        self.weight_OneMoreHRRound = 0 #0.5; 0
        self.weight_OneMorePicture = 0 #0.5; 0
        self.R_stop = 0 # -20; 0
        self.R_goalAchieved = 0 #15; 0 # N_HRround=='Num_maximalRound' OR N_pictures=='Num_totalPictures'  

    def reset(self):
        # self.picture_index = self.QuestionOrder[0]
        self.Response, self.Pleasure, self.Confusion = 0, 0, 0
        self.pictureCount, self.roundCount = 0, 0
        self.timeConfusion, self.timeNegativeEmotion = 0, 0
        state = [self.Response, self.Pleasure, self.Confusion]
        return state

    def getRward(self, action):
        r = 0
        #######
        # Regarding ResponseRelevance
        if self.Response == 0:#NR
            r += -2
        if self.Response == 1:
            if action == 1:# Providing moderately difficult prompt
                r += 0.75
            elif action == 2:# Providing difficult prompt
                r += 1.75 # 1.75; 3
            else:# Providng moderately difficult prompt or other actions
                r += 0.3 #+0.5; 1
        if self.Response == 2:
            if action == 1:
                r += 2
            elif action == 2:
                r += 3 # 10; 3
            else:
                r += 0.75 #+0.5; 1
        # Regarding Emotion_Pleasure
        if self.Pleasure == -1:
            r += -3
        if self.Pleasure == 0:
            r += 1 #+0.5; 1
        if self.Pleasure == 1:
            r += 2
        # Regarding Emotion_Confusion
        if self.Confusion == 1:
            r += -2.5
        if self.Confusion == 0:
            r += 2
        return r
    
    ########
        # if self.Response == 0:#NR
        #     r += -2
        # if self.Response == 1:
        #     if action == 1:# Providing easy prompt
        #         r += self.weight_mode * 0.75
        #     elif action == 2:# Providing difficult prompt
        #         r += self.weight_diff * 0.75
        #     else:# Providng moderately difficult prompt or other actions
        #         r += 0.75 #+0.5; 1
        # if self.Response == 2:
        #     if action == 1:
        #         r += self.weight_mode * 1.5
        #     elif action == 2:
        #         r += self.weight_diff * 1.5
        #     else:
        #         r += 1.5 #+0.5; 1
        # # Regarding Emotion_Pleasure
        # if self.Pleasure == -1:
        #     r += -3
        # if self.Pleasure == 0:
        #     r += 1 #+0.5; 1
        # if self.Pleasure == 1:
        #     r += 2
        # # Regarding Emotion_Confusion
        # if self.Confusion == 1:
        #     r += -2.5
        # if self.Confusion == 0:
        #     r += 2
        # return r
    ##############
    
        ##############
        # # Regarding ResponseRelevance
        # if self.Response == 0:
        #     r += self.weight_response*(-1)
        # if self.Response == 1:
        #     r += 1 #+0.5; 1
        # if self.Response == 2:
        #     r += self.weight_response * 1
        # # Regarding Emotion_Pleasure
        # if self.Pleasure == -1:
        #     r += self.weight_pleasure * (-1) #-3
        # if self.Pleasure == 0:
        #     r += 1
        # if self.Pleasure == 1:
        #     r += self.weight_pleasure * 1
        # # Regarding Emotion_Confusion
        # if self.Confusion == 1:
        #     r += self.weight_confusion * (-1)
        # if self.Confusion == 0:
        #     r += self.weight_confusion * (1)
        
        # return r
    
    def CalStateAndReward_UsingState(self, nextstate_text, action):
        # Regarding ResponseRelevance
        if nextstate_text.__contains__('NR'):
            self.Response = 0
        if nextstate_text.__contains__('IR'):
            self.Response = 1
        if nextstate_text.__contains__('RR'):
            self.Response = 2
        # Regarding Emotion_Pleasure
        if nextstate_text.__contains__('Neg'):
            self.Pleasure = -1
        if nextstate_text.__contains__('Neu'):
            self.Pleasure = 0
        if nextstate_text.__contains__('Pos'):
            self.Pleasure = 1
        # Regarding Emotion_Confusion    
        if nextstate_text.__contains__('No'):
            self.Confusion = 0
        if nextstate_text.__contains__('Yes'):
            self.Confusion = 1
            
        reward = self.getRward(action)
        return reward
    
    def TransitionToAllStates(self, P_actionStateTransition, action):
        p = np.random.uniform(0,1)
        if p < P_actionStateTransition[1]:
            nextstate_text = P_actionStateTransition.index[1]
        elif (P_actionStateTransition[1] <=p) and (p < np.sum(P_actionStateTransition[1:3].tolist())):
            nextstate_text = P_actionStateTransition.index[2]
        elif (np.sum(P_actionStateTransition[1:3].tolist()) <=p) and (p < np.sum(P_actionStateTransition[1:4].tolist())):
            nextstate_text = P_actionStateTransition.index[3]
        elif (np.sum(P_actionStateTransition[1:4].tolist()) <=p) and (p < np.sum(P_actionStateTransition[1:5].tolist())):
            nextstate_text = P_actionStateTransition.index[4]
        elif (np.sum(P_actionStateTransition[1:5].tolist()) <=p) and (p < np.sum(P_actionStateTransition[1:6].tolist())):
            nextstate_text = P_actionStateTransition.index[5]
        elif (np.sum(P_actionStateTransition[1:6].tolist()) <=p) and (p < np.sum(P_actionStateTransition[1:7].tolist())):
            nextstate_text = P_actionStateTransition.index[6]
        elif (np.sum(P_actionStateTransition[1:7].tolist()) <=p) and (p < np.sum(P_actionStateTransition[1:8].tolist())):
            nextstate_text = P_actionStateTransition.index[7]
        elif (np.sum(P_actionStateTransition[1:8].tolist()) <=p) and (p < np.sum(P_actionStateTransition[1:9].tolist())):
            nextstate_text = P_actionStateTransition.index[8]
        elif (np.sum(P_actionStateTransition[1:9].tolist()) <=p) and (p < np.sum(P_actionStateTransition[1:10].tolist())):
            nextstate_text = P_actionStateTransition.index[9]
        elif (np.sum(P_actionStateTransition[1:10].tolist()) <=p) and (p < np.sum(P_actionStateTransition[1:11].tolist())):
            nextstate_text = P_actionStateTransition.index[10]
        elif (np.sum(P_actionStateTransition[1:11].tolist()) <=p) and (p < np.sum(P_actionStateTransition[1:12].tolist())):
            nextstate_text = P_actionStateTransition.index[11]
        elif (np.sum(P_actionStateTransition[1:12].tolist()) <=p) and (p < np.sum(P_actionStateTransition[1:13].tolist())):
            nextstate_text = P_actionStateTransition.index[12]
        elif (np.sum(P_actionStateTransition[1:13].tolist()) <=p) and (p < np.sum(P_actionStateTransition[1:14].tolist())):
            nextstate_text = P_actionStateTransition.index[13]
        elif (np.sum(P_actionStateTransition[1:14].tolist()) <=p) and (p < np.sum(P_actionStateTransition[1:15].tolist())):
            nextstate_text = P_actionStateTransition.index[14]
        elif (np.sum(P_actionStateTransition[1:15].tolist()) <=p) and (p < np.sum(P_actionStateTransition[1:16].tolist())):
            nextstate_text = P_actionStateTransition.index[15]
        elif (np.sum(P_actionStateTransition[1:16].tolist()) <=p) and (p < np.sum(P_actionStateTransition[1:17].tolist())):
            nextstate_text = P_actionStateTransition.index[16]
        elif (np.sum(P_actionStateTransition[1:17].tolist()) <=p) and (p < np.sum(P_actionStateTransition[1:18].tolist())):
            nextstate_text = P_actionStateTransition.index[17]
        else:
            nextstate_text = P_actionStateTransition.index[18]
        
        reward = self.CalStateAndReward_UsingState(nextstate_text, action)
        
        return reward
    
    def a0_provideEasyPrompt(self):
        ind = self.df.index[(self.df['State'].str.contains('State')) & (self.df['State'].str.contains(ResponseRelevance[self.Response])) & (self.df['State'].str.contains(EmotionPleasure[self.Pleasure])) & (self.df['State'].str.contains(EmotionConfusion[self.Confusion]))]
        RowActionStateTransition = self.df.loc[ind[0]+2]
        immediateReward = self.TransitionToAllStates(RowActionStateTransition, action = 0)
        self.done= False
        # nextState = [self.Response, self.Pleasure, self.Confusion] 
        return immediateReward
    
    def a1_provideModeratelyDifficultPrompt(self):
        ind = self.df.index[(self.df['State'].str.contains('State')) & (self.df['State'].str.contains(ResponseRelevance[self.Response])) & (self.df['State'].str.contains(EmotionPleasure[self.Pleasure])) & (self.df['State'].str.contains(EmotionConfusion[self.Confusion]))]
        RowActionStateTransition = self.df.loc[ind[0]+3]
        immediateReward = self.TransitionToAllStates(RowActionStateTransition, action = 1)
        self.done= False
        return immediateReward
    
    def a2_provideDifficultPrompt(self):
        ind = self.df.index[(self.df['State'].str.contains('State')) & (self.df['State'].str.contains(ResponseRelevance[self.Response])) & (self.df['State'].str.contains(EmotionPleasure[self.Pleasure])) & (self.df['State'].str.contains(EmotionConfusion[self.Confusion]))]
        RowActionStateTransition = self.df.loc[ind[0]+4]
        immediateReward = self.TransitionToAllStates(RowActionStateTransition, action = 2)
        self.done= False
        return immediateReward
    
    def a3_repeat(self):
        ind = self.df.index[(self.df['State'].str.contains('State')) & (self.df['State'].str.contains(ResponseRelevance[self.Response])) & (self.df['State'].str.contains(EmotionPleasure[self.Pleasure])) & (self.df['State'].str.contains(EmotionConfusion[self.Confusion]))]
        RowActionStateTransition = self.df.loc[ind[0]+5]
        immediateReward = self.TransitionToAllStates(RowActionStateTransition, action = 3)
        self.done= False
        return immediateReward
    
    def a4_explain(self):
        ind = self.df.index[(self.df['State'].str.contains('State')) & (self.df['State'].str.contains(ResponseRelevance[self.Response])) & (self.df['State'].str.contains(EmotionPleasure[self.Pleasure])) & (self.df['State'].str.contains(EmotionConfusion[self.Confusion]))]
        RowActionStateTransition = self.df.loc[ind[0]+6]
        immediateReward = self.TransitionToAllStates(RowActionStateTransition, action = 4)
        self.done = False
        return immediateReward
    
    def a5_comfort(self):
        ind = self.df.index[(self.df['State'].str.contains('State')) & (self.df['State'].str.contains(ResponseRelevance[self.Response])) & (self.df['State'].str.contains(EmotionPleasure[self.Pleasure])) & (self.df['State'].str.contains(EmotionConfusion[self.Confusion]))]
        RowActionStateTransition = self.df.loc[ind[0]+7]
        immediateReward = self.TransitionToAllStates(RowActionStateTransition, action = 5)
        self.done= False
        return immediateReward
    
    def a6_giveUserChoice(self):
        ind = self.df.index[(self.df['State'].str.contains('State')) & (self.df['State'].str.contains(ResponseRelevance[self.Response])) & (self.df['State'].str.contains(EmotionPleasure[self.Pleasure])) & (self.df['State'].str.contains(EmotionConfusion[self.Confusion]))]
        Continuous_P_Transition = self.df.loc[ind[0]+8]
        # ChangePic_P_Transition = self.df.loc[ind[0]+9]
        Stop_P_Transition = self.df.loc[ind[0]+10]
        
        coin = np.random.uniform(0,1)
        # Stop or terminal
        if coin < Stop_P_Transition[0]:
            self.Response, self.Pleasure, self.Confusion = 0, 0, 0 # Here it should NOT influence the training process.
            immediateReward = self.R_stop
            self.done= True
            choice = 'Stop'
        # Change picture
        elif (Stop_P_Transition[0] <= coin) and (coin < 1- Continuous_P_Transition[0]):
            self.Response, self.Pleasure, self.Confusion = 0, 0, 0
            immediateReward = self.getRward(action = 6)
            self.pictureCount = self.pictureCount + 1
            immediateReward += self.weight_OneMorePicture
            self.done= False
            choice = 'ChangePic'
        # Continuous
        else:
            self.Response, self.Pleasure, self.Confusion = self.Response, self.Pleasure, self.Confusion
            immediateReward = self.getRward(action = 6)
            self.done= False
            choice = 'Continue'
        # nextState = [self.Response, self.Pleasure, self.Confusion]
        return immediateReward, choice
    
    def step(self, action):
        if action == 0:
            r = self.a0_provideEasyPrompt()
            self.roundCount = self.roundCount +1
            ######
            # Reward caused by additional roundCount
            r += self.weight_OneMoreHRRound
            ######
        if action == 1:
            r = self.a1_provideModeratelyDifficultPrompt()
            self.roundCount = self.roundCount +1
            r += self.weight_OneMoreHRRound
        if action == 2:
            r = self.a2_provideDifficultPrompt()
            self.roundCount = self.roundCount +1
            r += self.weight_OneMoreHRRound
        if action == 3:
            r = self.a3_repeat()
            self.roundCount = self.roundCount +1
            r += self.weight_OneMoreHRRound
        if action == 4:
            r = self.a4_explain()
            self.roundCount = self.roundCount +1
            r += self.weight_OneMoreHRRound
        if action == 5:
            r = self.a5_comfort()
            self.roundCount = self.roundCount +1
            r += self.weight_OneMoreHRRound
            
        if (self.roundCount > self.Num_maximalRound) or (self.pictureCount >= self.Num_totalPictures):
            self.done = True
            r += self.R_goalAchieved
        nextState = [self.Response, self.Pleasure, self.Confusion]
        return r, nextState, self.done
    
    def step_Action6_ProvideChoice(self, action):
        if action == 6:
            r, choice = self.a6_giveUserChoice()
            self.roundCount += 1
            r += self.weight_OneMoreHRRound
        
        if (self.roundCount > self.Num_maximalRound) or (self.pictureCount >= self.Num_totalPictures):
            self.done = True
            r += self.R_goalAchieved
        nextState = [self.Response, self.Pleasure, self.Confusion]
        return r, nextState, self.done, choice

# define the class for Reinforcement learning algorithm
class RLAgent(object):
    
    def __init__(self, env):#, learning_parameters, exploration_parameters): 
        # init the Q-table, ONLY considering the first 6 actions
        self.env = env
        self.qtable = np.zeros((self.env.dimen_StateSpace, self.env.dimen_ActionSpace))
        # self.qtable[0] = self.qtable[0]-5
        self.LearningRate = 0.05 # 0.05; 0.1
        self.epsilon = 0.1
        self.gamma = 0.95
    
    def get_action(self, state, timeNegativeEmotion, timeConfusion):
        
        if timeConfusion == 2 or timeNegativeEmotion == 2:
            action = 6
            timeNegativeEmotion, timeConfusion = 0, 0
        else: # exclusive action_6
            coin = np.random.uniform(0,1)
            timeNegativeEmotion, timeConfusion = timeNegativeEmotion, timeConfusion
            if  coin <= 1 - self.epsilon:
                # Action selection based on MERELY RL
                index_state = 6*state[0] + 2*(state[1]+1) + state[2]
                #################
                max_qs = np.where(np.max(self.qtable[index_state, :])==self.qtable[index_state, :])[0]
                action = np.random.choice(max_qs)
                # action = np.argmax(self.qtable[index_state, :])
            else:
                action = np.random.randint(0,self.env.dimen_ActionSpace)
        
        return action, timeNegativeEmotion, timeConfusion
    
    # def get_action_NoRandom(self, state, timeNegativeEmotion, timeConfusion):
        
    #     if timeConfusion == 2 or timeNegativeEmotion == 2:
    #         action = 6
    #         timeNegativeEmotion, timeConfusion = 0, 0
    #     else: # exclusive action_6
    #         timeNegativeEmotion, timeConfusion = timeNegativeEmotion, timeConfusion
    #         index_state = 6*state[0] + 2*(state[1]+1) + state[2]
    #         max_qs = np.where(np.max(self.qtable[index_state, :])==self.qtable[index_state, :])[0]
    #         action = np.random.choice(max_qs)
        
    #     return action, timeNegativeEmotion, timeConfusion
    
    def get_action_Random(self, timeNegativeEmotion, timeConfusion):
        
        if timeConfusion == 2 or timeNegativeEmotion == 2:
            action = 6
            timeNegativeEmotion, timeConfusion = 0, 0
        else: # exclusive action_6
            timeNegativeEmotion, timeConfusion = timeNegativeEmotion, timeConfusion
            action = np.random.randint(0,self.env.dimen_ActionSpace)
        
        return action, timeNegativeEmotion, timeConfusion
    
    def get_action_alwaysEasy(self, timeNegativeEmotion, timeConfusion):
        
        if timeConfusion == 2 or timeNegativeEmotion == 2:
            action = 6
            timeNegativeEmotion, timeConfusion = 0, 0
        else: # exclusive action_6
            timeNegativeEmotion, timeConfusion = timeNegativeEmotion, timeConfusion
            action = 0
        
        return action, timeNegativeEmotion, timeConfusion
    
    def update_qtable(self, state, new_state, action, reward):
        index_state = 6*state[0] + 2*(state[1]+1) + state[2]
        index_nextState = 6*new_state[0] + 2*(new_state[1]+1) + new_state[2]
        td_target = reward + self.gamma * np.max(self.qtable[index_nextState, :])
        td_delta = td_target - self.qtable[index_state, action]
        self.qtable[index_state,action] += self.LearningRate * td_delta          
            
        return self.LearningRate * td_delta
    
    def GetOptimalAction(self):
        optimalAction = np.argmax(self.qtable, axis=1)
        
        return optimalAction
    
    # @jit
    def q_learning(self, total_episodes, Total_Epochs):
        
        # self.Reward_AllEpisodes = np.zeros(total_episodes*Total_Epochs)
        # self.Action_AllEpisodes = np.zeros(total_episodes*Total_Epochs)
        self.OptimalAction_AllEpisodes = []
        self.Epoch_AverageReturn = np.zeros(Total_Epochs)
        self.Epoch_OptimalAction = []
        self.StartStateValue = []
        self.Sum_QTable = np.zeros(Total_Epochs)
        self.Update_SumQTable = np.zeros(Total_Epochs)
        self.Epoch_QValue_Update = np.zeros(Total_Epochs)
        
        for epoch_i in range (Total_Epochs):
            self.StartStateValue.append(self.qtable.max(axis=1))
            episode_rewards = 0
            sum_qtable = 0
            
            for episode_i in range(total_episodes):
                timeNegativeEmotion, timeConfusion = 0, 0
                done = False
                # reward_oneEpisode = 0
                state = self.env.reset()
                # i = 1
                while not done:        
                    # action, timeNegativeEmotion, timeConfusion = self.get_action(state, timeNegativeEmotion, timeConfusion)
                    action, timeNegativeEmotion, timeConfusion = self.get_action_alwaysEasy(timeNegativeEmotion, timeConfusion)
                    
                    #########
                    if action == 6:
                        reward, next_state, done, _ = self.env.step_Action6_ProvideChoice(action)
                        self.update_qtable(previous_state, next_state, previous_action, reward)
                    if action != 6:
                        reward, next_state, done = self.env.step(action)
                        self.update_qtable(state, next_state, action, reward)
                    
                    episode_rewards += reward
                    previous_state = state
                    previous_action = action
                    state = next_state
                    
                    if state[1] == -1:
                        timeNegativeEmotion += 1
                    if state[1] != -1:
                        timeNegativeEmotion = 0
                    if state[2] == 1:
                        timeConfusion += 1
                    if state[2] == 0:
                        timeConfusion = 0
                
                sum_qtable += self.qtable.sum()
                self.OptimalAction_AllEpisodes.append(self.GetOptimalAction())
                
            self.Epoch_AverageReturn[epoch_i] = episode_rewards/total_episodes
            self.Sum_QTable[epoch_i] = sum_qtable/total_episodes
            
            if epoch_i == 0:
                self.Update_SumQTable[epoch_i] = self.Sum_QTable[epoch_i]
            if epoch_i != 0:
                self.Update_SumQTable[epoch_i] = self.Sum_QTable[epoch_i] - self.Sum_QTable[epoch_i-1] 
        
        return self.Epoch_AverageReturn, self.Sum_QTable, self.Update_SumQTable, self.OptimalAction_AllEpisodes, self.qtable


env = Human_Robot_interaction()

RL_agent = RLAgent(env)#, learning_parameters, exploration_parameters)
Total_Epochs, total_episodes = 1500, 30
AveReturn_Epoch, AveSumQ_Epoch, AveUpdatedSumQ_Epoch, OptimalAction_Episode, Qtable = RL_agent.q_learning(total_episodes, Total_Epochs)

OptimalAction = pd.DataFrame(OptimalAction_Episode)
OptimalAction.to_csv('OptimalAction_Q_RewardFunction6_Change10.csv')

def CalReturnChange(target_episode, Num_test):
    Ave_R = []
    for epo in range(Total_Epochs):
        action_policy = OptimalAction_Episode[epo*total_episodes+target_episode]
        R = 0
        for test in range(Num_test):
            state = RL_agent.env.reset()
            done = False
            timeNegativeEmotion, timeConfusion = 0, 0
            while not done:
                index_state = 6*state[0] + 2*(state[1]+1) + state[2]
                action = action_policy[index_state]
                
                if timeConfusion == 2 or timeNegativeEmotion == 2:# action == 6:
                    action = 6
                    reward, next_state, done, _ = RL_agent.env.step_Action6_ProvideChoice(action)
                    # State_Action_Test.append([state,action, choice])
                if action != 6:
                    # State_Action_Test.append([state,action])
                    reward, next_state, done = RL_agent.env.step(action)
        
                R += reward
                state = next_state
            
                if state[1] == -1:
                    timeNegativeEmotion += 1
                if state[1] != -1:
                    timeNegativeEmotion = 0
                if state[2] == 1:
                    timeConfusion += 1
                if state[2] == 0:
                    timeConfusion = 0
        Ave_R.append(R/Num_test)
    
    return Ave_R

Ave_Return = CalReturnChange(target_episode = 10, Num_test = 40)

AllCombined_Epoch = np.dstack((AveReturn_Epoch, AveSumQ_Epoch, AveUpdatedSumQ_Epoch, Ave_Return))

Diff = []
for i in range((Total_Epochs-20)*total_episodes, Total_Epochs*total_episodes):
    diff = 0
    for index in range(18):
        if OptimalAction_Episode[i][index] != OptimalAction_Episode[i-1][index]:
            diff += 1
    Diff.append(diff)


AveReturn_50Epochs = []
MaxReturn_50Epochs = []
MinReturn_50Epochs = []
for i in range(Total_Epochs):
    if i < 49:
        AveReturn_50Epochs.append(np.mean(AveReturn_Epoch[0:i+1]))
        MaxReturn_50Epochs.append(np.max(AveReturn_Epoch[0:i+1]))
        MinReturn_50Epochs.append(np.min(AveReturn_Epoch[0:i+1]))
    else:
        AveReturn_50Epochs.append(np.mean(AveReturn_Epoch[i-49:i+1]))
        MaxReturn_50Epochs.append(np.max(AveReturn_Epoch[i-49:i+1]))
        MinReturn_50Epochs.append(np.min(AveReturn_Epoch[i-49:i+1]))

final_actionPolicy = OptimalAction_Episode[Total_Epochs*total_episodes-1]
Labels = []
Action_final = []
for relev in range(3):
    for pleas in range(-1,2):
        for confus in range(2):
            s = [ResponseRelevance[relev], EmotionPleasure[pleas], EmotionConfusion[confus]]
            Labels.append(s)
            Action_final.append(final_actionPolicy[6*relev + 2*(pleas+1) + confus])
    

plt.figure()
plt.subplot(331)
plt.plot(AveReturn_Epoch,linewidth=1)
plt.axis([0, Total_Epochs, 0, 370])
plt.ylabel("AveReturn_Epoch")
plt.xlabel("Epoch")

plt.subplot(332)
plt.plot(Ave_Return,linewidth=1)
plt.axis([0, Total_Epochs, 0, 370])
plt.ylabel("AveReturn_RegardingActionPolicy")
plt.xlabel("Epoch")

plt.subplot(333)
plt.plot(AveReturn_50Epochs,linewidth=1)
plt.fill_between(np.linspace(0,Total_Epochs-1,Total_Epochs), MinReturn_50Epochs, MaxReturn_50Epochs, alpha=0.2)
plt.axis([0, Total_Epochs, 0, 370])
plt.ylabel("AveReturn_Per50Epochs")
plt.xlabel("Epoch")

plt.subplot(334)
plt.plot(AveSumQ_Epoch)
plt.xlim([0, Total_Epochs])
# plt.axis([0, Total_Epochs, -1, 2])
plt.ylabel("AveSumQ_Epoch")
plt.xlabel("Epoch")

plt.subplot(335)
plt.plot(AveUpdatedSumQ_Epoch)
plt.ylabel("AveUpdatedSumQ")
plt.xlabel("Epoch")

plt.subplot(336)
plt.plot(Diff)
# plt.xlim([(Total_Epochs-20)*total_episodes, Total_Epochs*total_episodes-1])
plt.ylabel("Abs_diff_OptimalPolicy")
plt.xlabel("Last 3000 episodes")

plt.subplot(337)
Labels = ['1[NR,Neg,No]','2[NR,Neg,Yes]','3[NR,Neu,No]','4[NR,Neu,Yes]','5[NR,Pos,No]','6[NR,Pos,Yes]','7[IR,Neg,No]','8[IR,Neg,Yes]','9[IR,Neu,No]','10[IR,Neu,Yes]','11[IR,Pos,No]','12[IR,Pos,Yes]','13[RR,Neg,No]','14[RR,Neg,Yes]','15[RR,Neu,No]','16[RR,Neu,Yes]','17[RR,Pos,No]','18[RR,Pos,Yes]']
plt.bar(np.arange(len(Labels)), Action_final, width=0.4)
plt.xticks(np.arange(len(Labels)), Labels, rotation=90)
plt.ylabel("Optimal action")

plt.suptitle("Q_RewardFunct6_Change10")


########################################
####### Test Final Optimal Action Policy
final_actionPolicy = OptimalAction_Episode[Total_Epochs*total_episodes-1]
for i in range(20):
    State_Action_Test = []
    state = RL_agent.env.reset()
    done = False
    timeNegativeEmotion, timeConfusion = 0, 0
    # roundCount = 0
    while not done:
        index_state = 6*state[0] + 2*(state[1]+1) + state[2]
        action = final_actionPolicy[index_state]
        
        if timeConfusion == 2 or timeNegativeEmotion == 2:# action == 6:
            action = 6
            reward, next_state, done, choice = RL_agent.env.step_Action6_ProvideChoice(action)
            State_Action_Test.append([state,action, choice])
        if action != 6:
            State_Action_Test.append([state,action])
            reward, next_state, done = RL_agent.env.step(action)
        
        state = next_state
        # roundCount += 1
        
        if state[1] == -1:
            timeNegativeEmotion += 1
        if state[1] != -1:
            timeNegativeEmotion = 0
        if state[2] == 1:
            timeConfusion += 1
        if state[2] == 0:
            timeConfusion = 0
    
    # df = cudf.DataFrame(State_Action_Test)
    # df.to_csv('SATest_DoubleQ_NoCountPic_YesStop_NoGoalAchieved_PrevStateApplied_{}.csv'.format(i))
    df = pd.DataFrame(State_Action_Test)
    df.to_excel('SATest_Q_RewardFunct6_Change10_{}.xlsx'.format(i))
