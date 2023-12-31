import time
from Interventionist import Interventionist
from Patient import Patient

class SimManager:

    def __init__(self):
        #self.Logger = Logger()
        #print("SimManager initialized")
        self.interventionist = Interventionist()
        #print("Interventionist initialized")
        self.patient = Patient()
        #print("Patient initialized")
        self.doNextWithContext = False
        self.timeOfInit = time.time()
        #Format timeOfInit as human readable
        self.timeOfInit = time.strftime("%Y%m%d-%H%M%S", time.localtime(self.timeOfInit))
        self.logpath = "./logs/" + str(self.timeOfInit) + ".txt"
        self.printLog("SimManager initialized at " + str(self.timeOfInit))


        


    def printLog(self, text):
        with open(self.logpath, "a") as logFile:
            logFile.write(text + "\n")

    def printAndLog(self, text):
        print(text)
        self.printLog(text)

    def doOneStep(self):
        if self.doNextWithContext:
            self.interventionist.doCurrentStepWithContext()
        else:
            self.interventionist.doCurrentStep()
        self.printAndLog("Interventionist did a step.")
        self.printAndLog(f"\t{self.interventionist.latest_response}")
        self.printAndLog("\n")
        
        #If the interventionist responded properly
        if self.interventionist.latest_response:
            self.patient.last_message_other_agent = self.interventionist.latest_response
            #Prompt the patient using doRespondOtherAgent
            self.patient.doRespondOtherAgent()
            self.printAndLog("Patient did a step.")
            self.printAndLog(f"\t{self.patient.latest_response}")
            self.printAndLog("\n")

            #If the patient's response is not empty, check if it is a task breakdown - does it start with "TASKBREAKDOWN:"?
            if self.patient.latest_response.startswith("TASKBREAKDOWN:"):
                #Implement this later
                pass
            else:
                self.interventionist.last_message_other_agent = "Patient: " + self.patient.latest_response + "|||Context:"
                #Ready to prompt interventionist with doCurrentStepWithContext
                self.doNextWithContext = True
    
    def doPass(self, passStr):
        self.interventionist.setTask(passStr)
        self.patient.setTask(passStr)


#If we're running from the command line, run the main function
if __name__ == "__main__":
    newSimManager = SimManager()
    newSimManager.doPass("pass1")
    for i in range(5):
        newSimManager.doOneStep()
    
