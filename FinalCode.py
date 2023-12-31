import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec

ResponseRelevance = {0 : 'NR', 1 : 'IR', 2 : 'RR'}
EmotionPleasure = {-1 : 'Neg', 0 : 'Neu', 1 :'Pos'}
EmotionConfusion = {0 : 'No', 1: 'Yes'}
ActionSpace = {0 : 'ProvideEasyPrompt', 1 : 'ProvideModeratelyPrompt', 2 : 'ProvideDifficultPrompt',
               3 : 'Repeat', 4 : 'Explain', 5 : 'Comfort', 6 : 'GiveChoice'}

class Human_Robot_interaction(object):
    def __init__(self):
        self.df = pd.read_excel('PatientModel_v3.xlsx', engine = 'openpyxl')
        self.dimen_StateSpace = 18
        self.dimen_ActionSpace = 6
        self.Num_totalPictures = 15
        self.Num_maximalRound = 50 # Considering ~30min reminiscene
        # self.QuestionOrder = list(range(0,10)); random.shuffle(self.QuestionOrder)
        self.done = False
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
                r += 3 # 1.75; 3
            else:# Providng moderately difficult prompt or other actions
                r += 0.3
        if self.Response == 2:
            if action == 1:
                r += 2
            elif action == 2:
                r += 10 # 10; 3
            else:
                r += 0.75
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
    
    def get_action_Random(self, timeNegativeEmotion, timeConfusion):
        
        if timeConfusion == 2 or timeNegativeEmotion == 2:
            action = 6
            timeNegativeEmotion, timeConfusion = 0, 0
        else: # exclusive action_6
            timeNegativeEmotion, timeConfusion = timeNegativeEmotion, timeConfusion
            action = np.random.randint(0,self.env.dimen_ActionSpace)
        
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
                    action, timeNegativeEmotion, timeConfusion = self.get_action(state, timeNegativeEmotion, timeConfusion)
                    
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

OptimalAction_RFunct6 = pd.read_csv('OptimalAction_Q_RewardFunction6.csv')

Last_600Episodes = OptimalAction_RFunct6.loc[45000-601:45000-1][1:]
item_counts = Last_600Episodes[Last_600Episodes.columns[1:]].value_counts()

AveReturn_DifferentPolicy = []
for i in range(5):
    print('i=',i)
    policy = item_counts[item_counts == item_counts.iloc[i]].index
    
    R = 0
    for test in range(1000):
        state = RL_agent.env.reset()
        done = False
        timeNegativeEmotion, timeConfusion = 0, 0
        while not done:
            index_state = 6*state[0] + 2*(state[1]+1) + state[2]
            action = policy[0][index_state]
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
    
    AveReturn_DifferentPolicy.append(R/1000)

print(AveReturn_DifferentPolicy)

# ################################################################################
# ################################################################################
# ####### Test Final Optimal Action Policy
# final_actionPolicy = item_counts[item_counts == item_counts.iloc[4]].index
# for i in range(20):
#     State_Action_Test = []
#     state = RL_agent.env.reset()
#     done = False
#     timeNegativeEmotion, timeConfusion = 0, 0
#     # roundCount = 0
#     while not done:
#         index_state = 6*state[0] + 2*(state[1]+1) + state[2]
#         action = final_actionPolicy[0][index_state]
        
#         if timeConfusion == 2 or timeNegativeEmotion == 2:# action == 6:
#             action = 6
#             reward, next_state, done, choice = RL_agent.env.step_Action6_ProvideChoice(action)
#             State_Action_Test.append([state,action, choice])
#         if action != 6:
#             State_Action_Test.append([state,action])
#             reward, next_state, done = RL_agent.env.step(action)
        
#         state = next_state
#         # roundCount += 1
        
#         if state[1] == -1:
#             timeNegativeEmotion += 1
#         if state[1] != -1:
#             timeNegativeEmotion = 0
#         if state[2] == 1:
#             timeConfusion += 1
#         if state[2] == 0:
#             timeConfusion = 0
    
#     # df = cudf.DataFrame(State_Action_Test)
#     # df.to_csv('SATest_DoubleQ_NoCountPic_YesStop_NoGoalAchieved_PrevStateApplied_{}.csv'.format(i))
#     df = pd.DataFrame(State_Action_Test)
#     df.to_excel('SATest_Q_RewardFunct6_{}.xlsx'.format(i))

#######################################################################################################
#######################################################################################################
OptimalAction_RFunct6_Change10 = pd.read_csv('OptimalAction_Q_RewardFunction6_Change10.csv')

Last_600Episodes_Change10 = OptimalAction_RFunct6_Change10.loc[45000-601:45000-1][1:]
item_counts_Change10 = Last_600Episodes_Change10[Last_600Episodes_Change10.columns[1:]].value_counts()

AveReturn_DifferentPolicy_Change10 = []
for i in range(5):
    # print('i=',i)
    policy = item_counts_Change10[item_counts_Change10 == item_counts_Change10.iloc[i]].index
    
    R = 0
    for test in range(1000):
        state = RL_agent.env.reset()
        done = False
        timeNegativeEmotion, timeConfusion = 0, 0
        while not done:
            index_state = 6*state[0] + 2*(state[1]+1) + state[2]
            action = policy[0][index_state]
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
    
    AveReturn_DifferentPolicy_Change10.append(R/1000)

print(AveReturn_DifferentPolicy_Change10)

Frist5_OptimalPolicy_Return_Change10 = []
for i in range(5):
    a = []
    pol = item_counts_Change10[item_counts_Change10 == item_counts_Change10.iloc[i]].index
    a.append(pol)
    a.append(item_counts_Change10.iloc[i])
    a.append(AveReturn_DifferentPolicy_Change10[i])
    # frequency = item_counts_Change10.iloc[i]
    Frist5_OptimalPolicy_Return_Change10.append(a)
    

########################################
####### Test Final Optimal Action Policy
final_actionPolicy = item_counts_Change10[item_counts_Change10 == item_counts_Change10.iloc[0]].index
for i in range(20):
    State_Action_Test = []
    state = RL_agent.env.reset()
    done = False
    timeNegativeEmotion, timeConfusion = 0, 0
    # roundCount = 0
    while not done:
        index_state = 6*state[0] + 2*(state[1]+1) + state[2]
        action = final_actionPolicy[0][index_state]
        
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

########################### Plot of final optimal Policy
final_actionPolicy = item_counts[item_counts == item_counts.iloc[4]].index
final_actionPolicy_Change10 = item_counts_Change10[item_counts_Change10 == item_counts_Change10.iloc[0]].index
Action_final = []
Action_final_Change10 = []
for relev in range(3):
    for pleas in range(-1,2):
        for confus in range(2):
            s = [ResponseRelevance[relev], EmotionPleasure[pleas], EmotionConfusion[confus]]
            Action_final.append(final_actionPolicy[0][6*relev + 2*(pleas+1) + confus])
            Action_final_Change10.append(final_actionPolicy_Change10[0][6*relev + 2*(pleas+1) + confus])

plt.figure()
Labels = ['[NR,Neg,No]','[NR,Neg,Yes]','[NR,Neu,No]','[NR,Neu,Yes]','[NR,Pos,No]','[NR,Pos,Yes]','[IR,Neg,No]','[IR,Neg,Yes]','[IR,Neu,No]','[IR,Neu,Yes]','[IR,Pos,No]','[IR,Pos,Yes]','[RR,Neg,No]','[RR,Neg,Yes]','[RR,Neu,No]','[RR,Neu,Yes]','[RR,Pos,No]','[RR,Pos,Yes]']
plt.scatter(list(range(0, 18)), Action_final, marker='s', color='b', s=48, label ='Reward 1')
plt.scatter(list(range(0, 18)), Action_final_Change10, marker='o',color='red', s=20, label ='Reward 2')
plt.legend(fontsize = 'small')
plt.xticks(np.arange(len(Labels)), Labels, rotation=90)
yLabels = ['a1','a2','a3','a4','a5','a6']
plt.yticks(np.arange(6), yLabels)
plt.xlabel("State")
plt.ylabel("Optimal action")

plt.subplot(211)
plt.bar(np.arange(len(Labels)), Action_final, width=0.4)
plt.ylim([-1, 5.5])
# plt.xticks(np.arange(len(Labels)), Labels, rotation=90)
plt.xticks([])

plt.subplot(212)
plt.bar(np.arange(len(Labels)), Action_final_Change10, width=0.4)
plt.ylim([-1, 5.5])
plt.xticks(np.arange(len(Labels)), Labels, rotation=90)
plt.xlabel("State")

plt.ylabel("Optimal action")

##############################################################################
##############################################################################
##############################################################################
##############################################################################
Combine_RFunc6 = np.load('Combined_Q_RewardFunction6.npy')
AveReturn_Random = np.load('AverageReturn_Random.npy')
AveReturn_AlwaysAskEasy = np.load('AverageReturn_AlwaysAskEasy.npy')
Combine_RFunc6_Change10 = np.load('Combined_Q_RewardFunction6_Change10.npy')
# AllCombined_Epoch = np.dstack((AveReturn_Epoch, AveSumQ_Epoch, AveUpdatedSumQ_Epoch, Ave_Return_subPlot2))
AveReturn_Epoch_Q = Combine_RFunc6[:,:,0]
Ave_Return_subPlot2_Q = Combine_RFunc6[:,:,3]
AveSumQ_Epoch_Q = Combine_RFunc6[:,:,1]
AveUpdatedSumQ_Epoch_Q = Combine_RFunc6[:,:,2]

AveReturn_Epoch_Q_Change10 = Combine_RFunc6_Change10[:,:,0]
Ave_Return_subPlot2_Q_Change10 = Combine_RFunc6_Change10[:,:,3]
AveSumQ_Epoch_Q_Change10 = Combine_RFunc6_Change10[:,:,1]
AveUpdatedSumQ_Epoch_Q_Change10 = Combine_RFunc6_Change10[:,:,2]


# Diff = []
# Diff_Change10 = []
# for i in range(1,600):
#     diff, diff_Change10 = 0, 0
#     for index in range(1,19):
#         if Last_600Episodes.iloc[i][index] != Last_600Episodes.iloc[i-1][index]:
#             diff += 1
#         if Last_600Episodes_Change10.iloc[i][index] != Last_600Episodes_Change10.iloc[i-1][index]:
#             diff_Change10 +=1
    
#     Diff.append(diff)
#     Diff_Change10.append(diff_Change10)

def ForRangePlot(AveReturn_Epoch, Total_Epochs):
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
    
    return AveReturn_50Epochs, MaxReturn_50Epochs, MinReturn_50Epochs

Total_Epochs = 1500
MeanG_Q, MaxG_Q, MinG_Q = ForRangePlot(AveReturn_Epoch_Q[0,:].tolist(), Total_Epochs)
MeanG_Q_subPlot2, MaxG_Q_subPlot2, MinG_Q_subPlot2 = ForRangePlot(Ave_Return_subPlot2_Q[0,:].tolist(), Total_Epochs)
MeanG_Random, MaxG_Q_Random, MinG_Q_Random = ForRangePlot(AveReturn_Random[:,].tolist(), Total_Epochs)
MeanG_AlwaysEasy, MaxG_Q_AlwaysEasy, MinG_Q_AlwaysEasy = ForRangePlot(AveReturn_AlwaysAskEasy[:,].tolist(), Total_Epochs)

plt.figure()
plt.subplot(131)
plt.plot(MeanG_Q,color='b', linewidth=1, label = 'Epsilon-greedy QL')
plt.fill_between(np.linspace(0,Total_Epochs-1,Total_Epochs), MinG_Q, MaxG_Q,color='b',alpha=0.15)
plt.plot(MeanG_Q_subPlot2,color='m',linewidth=1, label = 'Greedy QL')
plt.fill_between(np.linspace(0,Total_Epochs-1,Total_Epochs), MinG_Q_subPlot2, MaxG_Q_subPlot2,color='m',alpha=0.15)
plt.plot(MeanG_Random,color='k', linewidth=1,label = 'Random action')
plt.fill_between(np.linspace(0,Total_Epochs-1,Total_Epochs), MinG_Q_Random, MaxG_Q_Random,color='k',alpha=0.1)
plt.plot(MeanG_AlwaysEasy,color='g', linewidth=1,label = 'Always action a1')
plt.fill_between(np.linspace(0,Total_Epochs-1,Total_Epochs), MinG_Q_AlwaysEasy, MaxG_Q_AlwaysEasy,color='g',alpha=0.1)
plt.legend(loc='best',bbox_to_anchor=(0.5, 0.10, 0.5, 0.25), fontsize='x-small')
plt.xlim([0, Total_Epochs])
plt.ylabel("Average return per epoch")
plt.xlabel("Epoch")
# plt.subplot(131)
# plt.plot(AveReturn_Epoch_Q[0,:].tolist(), color='b', linewidth=1, label = 'Epsilon-greedy Q-learning') #Reward6
# plt.plot(Ave_Return_subPlot2_Q[0,:].tolist(), color='m', alpha = 0.5, linewidth=1, label = 'Greedy Q-learning') #Reward6
# # plt.plot(AveReturn_Epoch_Q_Change10[0,:].tolist(), color='red', linewidth=1) #Reward6_Change to 10
# # plt.plot(Ave_Return_subPlot2_Q_Change10[0,:].tolist(), color='c') #Reward6_Change to 10
# plt.plot(AveReturn_Random[:,].tolist(), color='k', linewidth=1, label = 'Random action selection')
# plt.legend(loc='best',bbox_to_anchor=(0.5, 0.04, 0.5, 0.5), fontsize='small')
# plt.ylabel("Average return per epoch")
# plt.xlabel("Epoch")

# plt.subplot(222)
# plt.plot(Diff, color = 'b', linewidth=1)
# # plt.plot(Diff_Change10, color = 'red', linewidth=1)
# # plt.xlim([(Total_Epochs-20)*total_episodes, Total_Epochs*total_episodes-1])
# plt.ylabel("Difference in policy")
# plt.xlabel("Last 600 episodes")

plt.subplot(132)
plt.plot(AveSumQ_Epoch_Q[0,:].tolist(), color = 'b',linewidth=1)
# plt.plot(AveSumQ_Epoch_Q_Change10[0,:].tolist(), color = 'red', linewidth=1)
plt.xlim([0, Total_Epochs])
# plt.axis([0, Total_Epochs, -1, 2])
plt.ylabel("Q-values sum")
plt.xlabel("Epoch")

plt.subplot(133)
plt.plot(AveUpdatedSumQ_Epoch_Q[0,:].tolist(), color = 'b',linewidth=1)
# plt.plot(AveUpdatedSumQ_Epoch_Q_Change10[0,:].tolist(), color = 'red', linewidth=1)
plt.xlim([0, Total_Epochs])
plt.ylabel("Q-values update")
plt.xlabel("Epoch")

#########################
##########################
#########################





fig = plt.figure(constrained_layout=True)
fig.set_figheight(8)
fig.set_figwidth(11)

ax0 = fig.add_subplot( GridSpec(2, 2)[0:1, 0:1] )
ax0.plot(AveSumQ_Epoch_Q[0,:].tolist(), color = 'b', linewidth=1)
ax0.plot(AveSumQ_Epoch_Q_Change10[0,:].tolist(), color = 'red', linewidth=1)
ax0.set_ylabel("Q-values sum")
ax0.set_xlabel("Epoch")

ax1 = fig.add_subplot( GridSpec(2, 2)[0:1, 1:2] )
ax1.plot(Diff, color = 'b', linewidth=1,label = 'Reward 1')
ax1.plot(Diff_Change10, color = 'red', linewidth=1,label = 'Reward 2')
ax1.legend(loc='best')
ax1.set_ylabel("Difference in policy")
ax1.set_xlabel("Last 600 episodes")

ax2 = fig.add_subplot( GridSpec(2, 2)[1:2, 0:2] )
Labels = ['[NR,Neg,No]','[NR,Neg,Yes]','[NR,Neu,No]','[NR,Neu,Yes]','[NR,Pos,No]','[NR,Pos,Yes]','[IR,Neg,No]','[IR,Neg,Yes]','[IR,Neu,No]','[IR,Neu,Yes]','[IR,Pos,No]','[IR,Pos,Yes]','[RR,Neg,No]','[RR,Neg,Yes]','[RR,Neu,No]','[RR,Neu,Yes]','[RR,Pos,No]','[RR,Pos,Yes]']
ax2.scatter(list(range(0, 18)), Action_final, marker='s', color='b', s=30, label ='Reward 1')
ax2.scatter(list(range(0, 18)), Action_final_Change10, marker='o',color='red', s=16, label ='Reward 2')

x = np.arange(len(Labels)) 
ax2.set_xlabel("State")
ax2.set_ylabel("Optimal action")
ax2.set_xticks(x)
ax2.set_xticklabels(Labels, rotation = 90)
ax2.legend()






