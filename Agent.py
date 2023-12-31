from GPTObject import GPTObject
from Parseparams import Parseparams
class Agent:
    def __init__(self):
        self.current_task = ""
        self.current_step = 0
        self.current_step_text = ""
        self.latest_response = ""
        self.latest_response_dict = None
        #GPTObject must be initialized in the child class
        self.GPTObject = None
        self.last_message_other_agent = ""
        self.assistance_type = ""
        self.specified_reaction = ""
    
    def currentStep(self):
        # Common implementation for currentStep
        self.current_step_text = self.GPTObject.getInterventionistCurrentStep()
        if self.current_step == 0:
            #This is the 0th step, meaning we need to explain the task to the patient
            #Add this context
            ##extra_context = "This is the first step of this task. You should explain the general concept of the task to the patient using the provided information as context. Task context:"
            extra_context = ""
            self.current_step_text = extra_context + self.current_step_text
            #print(f"[{self.current_step_text}]")

    def incrementStep(self):
        # Common implementation for incrementStep
        self.current_step += 1
        self.GPTObject.incrementStep()

    def setTask(self, task):
        # Common implementation for setTask
        self.GPTObject.setTask(task)
        self.current_task = task
        self.current_step = 0
        self.current_step_text = ""
        self.latest_response = ""


    def doCurrentStep(self):
        # Common implementation for doCurrentStep
        self.currentStep()
        self.latest_response = self.GPTObject.completeFromText("current_step=" + str(self.current_step)+" "+self.current_step_text)
        #self.incrementStep()

    def doRespondOtherAgent(self):
        # Common implementation for doRespondOtherAgent
        self.latest_response = self.GPTObject.completeFromText(self.last_message_other_agent+" "+self.specified_reaction)
        self.last_message_other_agent = ""
    
    def doCurrentStepWithContext(self):
        self.currentStep()
        context_text = self.last_message_other_agent
        context_text += "current_step=" + str(self.current_step) + " "
        if self.assistance_type != "":
            context_text += " assistance_type=" + self.assistance_type
        if self.specified_reaction != "":
            context_text += " specified_reaction:" + self.specified_reaction
        #Is this the final step in this pass?
        if self.current_step == len(self.GPTObject.passlist[self.current_task]) - 1:
            context_text += " final_step=true"
            print(f"CURRENT STEP IS {self.current_step} AND LENGTH OF PASSLIST IS {len(self.GPTObject.passlist[self.current_task])}")
        else:
            context_text += " final_step=false"
        context_text += " " + self.current_step_text
        #print(f"Preparing to complete from text: {context_text}")
        self.latest_response = self.GPTObject.completeFromText(context_text)
        print(self.assistance_type)
        self.latest_response_dict = Parseparams.parse_parameters(self.latest_response)
        
        #Was this a continuing response? If so, we must increment the step
        #Does the key "ready_to_continue" exist in the response?
        if "ready_to_continue" not in self.latest_response_dict:
            print("No ready_to_continue key in response")
            return
        else:
            if self.latest_response_dict["ready_to_continue"] == "true":
                self.incrementStep()
                print("Ready to continue step. New step is " + str(self.current_step))
            else:
                print("Not ready to continue step. ready_to_continue is " + self.latest_response_dict["ready_to_continue"])

