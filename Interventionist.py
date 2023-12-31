from Agent import Agent
from GPTObject import GPTObject
from AssistiveType import AssistiveType

class Interventionist(Agent):
    def __init__(self):
        super().__init__()
        # Additional initialization code specific to Interventionist class
        self.GPTObject = GPTObject(mode="interventionist")
        self.AssistiveTypeObj = AssistiveType()
        self.assistance_type = "assistance_type="+self.AssistiveTypeObj.selectAction().asReadable()
    def updateAssistanceType(self, rl_action=None):
        if rl_action is None:
            self.AssistiveTypeObj.selectAction()
            self.assistance_type = "assistance_type="+self.AssistiveTypeObj.selectAction().asReadable()
            print("Reroled assistance type: "+self.assistance_type)
        else:
            self.assistance_type = "assistance_type="+self.AssistiveTypeObj.asReadable(at_action=rl_action)
            print("Manually set assistance type: "+self.assistance_type+" from rl_action: "+str(rl_action))
    # Any additional methods specific to Interventionist class
        
