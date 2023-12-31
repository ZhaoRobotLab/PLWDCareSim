import json
import time
from Interventionist import Interventionist
from Patient import Patient
from Parseparams import Parseparams

class SimManager:

    def __init__(self):
        self.interventionist = Interventionist()
        self.patient = Patient()
        self.doNextWithContext = False
        self.timeOfInit = time.time()
        self.timeOfInit = time.strftime("%Y%m%d-%H%M%S", time.localtime(self.timeOfInit))
        self.logpath = "./logs/" + str(self.timeOfInit) + ".json"
        self.log_data = []
        self.last_assistance_type = None
        self.steps_completed = 0
        self.substeps_completed = 0
        self.epochs_completed = 0
        self.patient_status = {}

    def remove_trailing_comma(self, data):
        if isinstance(data, list):
            # Remove trailing comma for lists
            while data and not data[-1]:
                data.pop()
        elif isinstance(data, str):
            # Remove trailing comma for strings
            data = data.rstrip(',')

        return data

    def log_step(self, agent_type, response):
        parsed_response = Parseparams.parse_parameters(response)
        step_data = {
            "agent_type": agent_type,
            "verbal_utterance": parsed_response.get("verbal_utterance", ""),
            "nonverbal_behavior": parsed_response.get("nonverbal_behavior", []),
        }

        if agent_type == "Interventionist":
            step_data.update({
                "ready_to_continue": parsed_response.get("ready_to_continue", False),
                "current_step": self.remove_trailing_comma(parsed_response.get("current_step", 0)),
                "action_taken": parsed_response.get("action_taken", ""),
                "completed_steps": self.remove_trailing_comma(parsed_response.get("completed_steps", "")),
                "completed_substeps": self.remove_trailing_comma(parsed_response.get("completed_substeps", "")),
            })
            self.steps_completed = step_data["completed_steps"]
            self.substeps_completed = step_data["completed_substeps"]

        elif agent_type == "Patient":
            new_step_dict = {
                "forgetfulness_status": self.remove_trailing_comma(parsed_response.get("forgetfulness_status", "")),
                "frustration_status": self.remove_trailing_comma(parsed_response.get("frustration_status", "")),
                "anger_status": self.remove_trailing_comma(parsed_response.get("anger_status", "")),
                "engagement_status": self.remove_trailing_comma(parsed_response.get("engagement_status", "")),
            }
            step_data.update(new_step_dict)
            self.patient_status = new_step_dict

        self.log_data.append(step_data)


    def save_log_to_json(self):
        with open(self.logpath, "w") as log_file:
            json.dump(self.log_data, log_file, indent=4)

    def doOneStep(self, rl_action=None):
        if self.doNextWithContext:
            if rl_action is not None:
                self.interventionist.updateAssistanceType(rl_action=rl_action)
            else:
                self.interventionist.updateAssistanceType()
            self.interventionist.doCurrentStepWithContext()
            #What type of assistance did the interventionist provide?
            self.last_assistance_type = self.interventionist.assistance_type
            self.log_step("Interventionist", self.interventionist.latest_response)
        else:
            self.interventionist.doCurrentStep()
            #What type of assistance did the interventionist provide?
            self.last_assistance_type = self.interventionist.assistance_type
            #print("Interventionist provided assistance type: " + self.last_assistance_type)
            self.log_step("Interventionist", self.interventionist.latest_response)

        if self.interventionist.latest_response:
            self.patient.last_message_other_agent = self.interventionist.latest_response
            #Map the assistance type to the format needed by AgentParameters.py
            fixed_format = ""
            match self.last_assistance_type:
                case "assistance_type=VERBAL_DIRECTIVE":
                    fixed_format = "intervention_verbalDirective"
                case "assistance_type=VERBAL_SUPPORTIVE":
                    fixed_format = "intervention_verbalSupportive"
                case "assistance_type=VERBAL_NON_DIRECTIVE":
                    fixed_format = "intervention_verbalNonDirective"
                case "assistance_type=NONE":
                    fixed_format = "intervention_none"
                case _:
                    fixed_format = "ERR"

            
            self.patient.updateSpecifiedReaction(fixed_format)
            print("Patient was requested to do: " + self.patient.specified_reaction)
            self.patient.doRespondOtherAgent()
            self.log_step("Patient", self.patient.latest_response)


            self.interventionist.last_message_other_agent = "Patient: " + self.patient.latest_response + "|||Context:"
            self.doNextWithContext = True

        self.save_log_to_json()

    def doPass(self, passStr):
        self.interventionist.setTask(passStr)
        self.patient.setTask(passStr)
        self.epochs_completed += 1

    def getCurrentSimState(self):
        local_status = self.patient_status
        #Does the key forgetfulness_status exist in the dictionary?
        if "forgetfulness_status" not in local_status:
            local_status["forgetfulness_status"] = "no"
        if "frustration_status" not in local_status:
            local_status["frustration_status"] = "no"
        if "anger_status" not in local_status:
            local_status["anger_status"] = "no"
        if "engagement_status" not in local_status:
            local_status["engagement_status"] = "no"
        local_forgetfulness = True if local_status["forgetfulness_status"] == "yes" else False
        local_frustration = True if local_status["frustration_status"] == "yes" else False
        local_anger = True if local_status["anger_status"] == "yes" else False
        local_engagement = True if local_status["engagement_status"] == "yes" else False
        return {"steps_completed": int(self.steps_completed), "substeps_completed": int(self.substeps_completed), "epochs_completed": int(self.epochs_completed), "forgetfulness": local_forgetfulness, "frustration": local_frustration, "anger": local_anger, "engagement": local_engagement}
if __name__ == "__main__":
    newSimManager = SimManager()
    newSimManager.doPass("pass1")
    for i in range(15):
        newSimManager.doOneStep()
