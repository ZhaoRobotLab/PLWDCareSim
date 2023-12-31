from Agent import Agent
from GPTObject import GPTObject
from AgentParameters import AgentParameters
class Patient(Agent):
    def __init__(self):
        super().__init__()
        # Additional initialization code specific to Patient class
        self.GPTObject = GPTObject(mode="patient")
        self.agent_parameters = AgentParameters()
    def updateSpecifiedReaction(self, intervention_type):
        self.specified_reaction = self.agent_parameters.perform_task_breakdown(intervention_type)
        
    # Any additional methods specific to Patient class
