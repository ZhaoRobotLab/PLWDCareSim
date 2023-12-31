from enum import Enum
import random

class ATEnum(Enum):
    NONE = 0
    VERBAL_SUPPORTIVE = 1
    VERBAL_NON_DIRECTIVE = 2
    VERBAL_DIRECTIVE = 3

class AssistiveType:

    def __init__(self, verbal_supportive=None, verbal_nondirective=None, verbal_directive=None):
        self.verbal_supportive = verbal_supportive
        self.verbal_nondirective = verbal_nondirective
        self.verbal_directive = verbal_directive

        self.value_map = {}

        #How many assistive types are there?
        self.num_params = 3.0

        self.default_verbal_supportive = 1/self.num_params
        self.default_verbal_nondirective = 2/self.num_params
        self.default_verbal_directive = 3/self.num_params

        self.random_number = None
        self.random_number = self.randomize()

        #For each parameter, if it is None, use a default value. Otherwise, use the value provided.
        if self.verbal_supportive is None:
            self.verbal_supportive = self.default_verbal_supportive
        if self.verbal_nondirective is None:
            self.verbal_nondirective = self.default_verbal_nondirective
        if self.verbal_directive is None:
            self.verbal_directive = self.default_verbal_directive


        #Create a map of values to assistive types
        self.value_map[ATEnum.VERBAL_SUPPORTIVE] = self.verbal_supportive
        self.value_map[ATEnum.VERBAL_NON_DIRECTIVE] = self.verbal_nondirective
        self.value_map[ATEnum.VERBAL_DIRECTIVE] = self.verbal_directive
        #Sort the map by value in descending order
        self.value_map = {k: v for k, v in sorted(self.value_map.items(), key=lambda item: item[1], reverse=True)}

    def randomize(self):
        self.random_number = random.random()
        return self.random_number
    def selectAction(self, returnRandom=False):
            # Generate a random number between 0 and 1
            self.randomize()
            return_action = ATEnum.NONE
            # Iterate over the value_map and find the key corresponding to the random number
            for action, value in self.value_map.items():
                if self.random_number <= value:
                    return_action = action
            if returnRandom == False:
                # If no key is found, return NONE as the default action
                self.selectedAction = return_action
                return self
            else:
                self.selectedAction = (return_action, self.random_number)
                return self


    def asReadable(self, at_action=None):
        # Use the provided argument if available; otherwise, use the stored value
        action_to_convert = at_action if at_action is not None else self.selectedAction
        #Is action_to_convert a tuple?
        if isinstance(action_to_convert, tuple):
            #If so, return the (ACTION, VALUE) string
            return str(action_to_convert[0].name) + ", " + str(action_to_convert[1])
        elif isinstance(action_to_convert, int):
            #If so, return the (ACTION, VALUE) string
            return str(ATEnum(action_to_convert).name)
        else:
            #If not, return the name of the action
            return action_to_convert.name if action_to_convert else None
    
            
#If we are running this file directly, run a test
if __name__ == "__main__":
    #Create an AssistiveType object with no parameters
    at = AssistiveType()
    # #Print the values of the parameters
    # print("Verbal Supportive: " + str(at.verbal_supportive))
    # print("Verbal Nondirective: " + str(at.verbal_nondirective))
    # print("Verbal Directive: " + str(at.verbal_directive))
    # #Print the value map
    # print("Value Map: " + str(at.value_map))
    # #Print the default values
    # print("Default Verbal Supportive: " + str(at.default_verbal_supportive))
    # print("Default Verbal Nondirective: " + str(at.default_verbal_nondirective))
    # print("Default Verbal Directive: " + str(at.default_verbal_directive))
    # #Print the number of parameters
    # print("Number of Parameters: " + str(at.num_params))
    # #Print the action selected by the selectAction method
    # print("Select Action: " + str(at.selectAction()))
    # #Print the action selected by the selectAction method
    # print("Select Action (Random): " + at.selectAction().asReadable())
    # #Print the action selected by the selectAction method, with the returnRandom parameter set to True
    # print("Select Action (Random): " + at.selectAction(returnRandom=True).asReadable())
    #print(at.asReadable(at_action=1))