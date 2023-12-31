from openai import OpenAI
from passlist_SubtaskGuidance import Passlist
from PatientContext import PatientContext
from InterventionistContext import InterventionistContext

class GPTObject:

    def __init__(self, model="gpt-4-1106-preview", mode="patient", temperature=0.5, top_p=0.5):
        self.model = model
        self.chat = []
        self.temperature = temperature
        self.top_p = top_p
        self.passlist = Passlist().passlist
        self.api_key = "API_KEY"
        self.client = OpenAI(api_key=self.api_key)
        # If the mode is not "patient" or "interventionist", throw an error
        if mode != "patient" and mode != "interventionist":
            raise ValueError("Mode must be either 'patient' or 'interventionist'")

        self.mode = mode
        patient_context = PatientContext().patient_context

        interventionist_context = InterventionistContext().interventionist_context

        if self.mode == "patient":
            self.chat = [{"role": "system", "content": patient_context},]
        elif self.mode == "interventionist":
            self.chat = [{"role": "system", "content": interventionist_context}]

        self.current_task = ""
        self.current_step = 0

    def completeFromText(self, text):
        self.chat.append({"role": "user", "content": text})
        agent = self.client.chat.completions.create(
            model=self.model,
            messages=self.chat,
            temperature=self.temperature,
            top_p=self.top_p
        )
        print("\tGPT prompted with: " + text)
        reply_content = agent.choices[0].message.content
        # print("GPT prompted with: " + text)
        return reply_content

    def setTask(self, task):
        # Does key "task" exist in the passlist?
        if task not in self.passlist:
            raise ValueError("Task not found in passlist")
        else:
            self.current_task = task
            self.current_step = 0

    def getInterventionistCurrentStep(self):
        # If the current task is empty, throw an error
        if self.current_task == "":
            raise ValueError(
                "Current task is empty. Please set a task using setTask()")
        # If the current step is greater than the length of the task, throw an error
        if self.current_step >= len(self.passlist[self.current_task]):
            raise ValueError(
                "Current step is greater than the length of the task")
        # If the current step is less than the length of the task, increment the step and return the next step
        else:
            return self.passlist[self.current_task][self.current_step]

    def incrementStep(self):
        self.current_step += 1
