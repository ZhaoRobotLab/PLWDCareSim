import random
import time

class AgentParameters:
    def __init__(self):
        self.moderate_dementia = self.moderate_dementia()
        self.status_forgetfulness = False
        self.status_frustration = False
        self.status_anger = False
        self.status_disengagement = False
        self.random_value = None

    class moderate_dementia: 
        def __init__(self):
            '''
            The probabilities below describe the likelihood that a dementia patient will exhibit a specific affective state.
            The values represent the following idea:
            "Given the response of the interventionist, what is the probability that the patient will exhibit a specific affective state?"
            For example, self.probs["intervention_verbalSupportive"]["react_forgetful"] = 0.1 means that if the interventionist provides verbal supportive assistance, there is a 10% chance that the patient will exhibit forgetfulness.
            '''
            self.probs = {
                #This item set to same as verbalSupportive for now
                "intervention_none": {
                    "react_forgetful": 0.1,
                    "react_frustration": 0.1,
                    "react_anger": 0.01,
                    "react_disengaged": 0.02,
                },
                "intervention_verbalSupportive": {
                    "react_forgetful": 0.1,
                    "react_frustration": 0.1,
                    "react_anger": 0.01,
                    "react_disengaged": 0.02,
                },
                "intervention_verbalNonDirective": {
                    "react_forgetful": 0.05,
                    "react_frustration": 0.05,
                    "react_anger": 0.08,
                    "react_disengaged": 0.05,
                },
                "intervention_verbalDirective": {
                    "react_forgetful": 0.02,
                    "react_frustration": 0.02,
                    "react_anger": 0.08,
                    "react_disengaged": 0.05,
                },
            }
        


    def check_cognitive_affective_state(self, probability_set):
        """
        Generates a random number and checks if it's less than the given threshold.
        Used to simulate whether a dementia patient exhibits a specific affective state.

        :param threshold: A float representing the threshold probability.
        """
        # Generate a random number between 0 and 1
        random_number = random.random()

        this_set = probability_set
        #Sort the map by value ascending
        this_set = {k: v for k, v in sorted(this_set.items(), key=lambda item: item[1])}
        probability_sum = 0
        for key, value in this_set.items():
            probability_sum += value
        
        probability_none = 1 - probability_sum

        thresholds = {"react_normal": probability_none}
        current_threshold = probability_none
        for key, value in this_set.items():
            current_threshold += value
            thresholds[key] = current_threshold

        #Sort the map by value ascending
        thresholds = {k: v for k, v in sorted(thresholds.items(), key=lambda item: item[1])}
        
        #print(thresholds)
        # Iterate over the value_map and find the key corresponding to the random number
        for key, value in thresholds.items():
            #print(f"Is {random_number} <= {value}?" + str(random_number <= value))
            if random_number <= value:
                return (key, random_number)

    

        #So, for example if random_number p = 0.01 given


    def perform_task_breakdown(self, interventionist_response):
        ##### Task breakdown module
        #What is the probability we should use?
        check_state = self.check_cognitive_affective_state(self.moderate_dementia.probs[interventionist_response])
        check_state, self.random_value = check_state

        match check_state:
            case "react_forgetful":
                self.status_forgetfulness = True
                self.status_frustration = self.status_anger = self.status_disengagement = False
            case "react_frustration":
                self.status_frustration = True
                self.status_forgetfulness = self.status_anger = self.status_disengagement = False
            case "react_anger":
                self.status_anger = True
                self.status_forgetfulness = self.status_frustration = self.status_disengagement = False
            case "react_disengaged":
                self.status_disengagement = True
                self.status_forgetfulness = self.status_frustration = self.status_anger = False
            case "react_normal":
                self.status_forgetfulness = self.status_frustration = self.status_anger = self.status_disengagement = False

        #Flip self.status_disengagement because it's represented as "engagement_status" in the output string
        #self.status_disengagement = not self.status_disengagement
        #Do a switch on check_state
        

        self.patient_status_behavior = {"forgetfulness": self.status_forgetfulness, "frustration": self.status_frustration, "anger": self.status_anger, "disengagement": self.status_disengagement}
        #Create the string to match the format:
        #forgetfulness_status=no, frustration_status=yes, anger_status=no, engagement_status=yes
        output_str = f"(forgetfulness_status={'yes' if self.status_forgetfulness else 'no'}, frustration_status={'yes' if self.status_frustration else 'no'}, anger_status={'yes' if self.status_anger else 'no'}, engagement_status={'yes' if not self.status_disengagement else 'no'}, verbal_utterance=None, nonverbal_behavior=None)"
        return output_str
            
if __name__ == "__main__":
    print("Running AgentParameters.py in main")
    agent_parameters = AgentParameters()
    results_map = {}
    random_values_map = {}
    for i in range(10000):
        agent_parameters.perform_task_breakdown("intervention_verbalSupportive")
        #print(agent_parameters.patient_status_behavior)
        #print(agent_parameters.random_value)
        if round(agent_parameters.random_value,3) in random_values_map:
            random_values_map[round(agent_parameters.random_value,3)] += 1
        else:
            random_values_map[round(agent_parameters.random_value,3)] = 1
        if agent_parameters.patient_status_behavior["forgetfulness"] == True:
            if "forgetfulness" in results_map:
                results_map["forgetfulness"] += 1
            else:
                results_map["forgetfulness"] = 1
        elif agent_parameters.patient_status_behavior["frustration"] == True:
            if "frustration" in results_map:
                results_map["frustration"] += 1
            else:
                results_map["frustration"] = 1
        elif agent_parameters.patient_status_behavior["anger"] == True:
            if "anger" in results_map:
                results_map["anger"] += 1
            else:
                results_map["anger"] = 1
        elif agent_parameters.patient_status_behavior["disengagement"] == True:
            if "disengagement" in results_map:
                results_map["disengagement"] += 1
            else:
                results_map["disengagement"] = 1
        else:
            if "normal" in results_map:
                results_map["normal"] += 1
            else:
                results_map["normal"] = 1

    print(results_map)
    #What are the percentages of each? First, find the total number of results
    total_results = 0
    for key, value in results_map.items():
        total_results += value
    #Now, find the percentages
    percentages_map = {}
    for key, value in results_map.items():
        percentages_map[key] = value / total_results
        #Multiply by 100 to get the percentage
        percentages_map[key] *= 100
        #Truncate to 2 decimal places
        percentages_map[key] = round(percentages_map[key], 2)
    print(percentages_map)
    #Sort random_values_map by key ascending
    random_values_map = {k: v for k, v in sorted(random_values_map.items(), key=lambda item: item[0])}
    #What is the total sum of random values?
    total_randoms = 0
    for key, value in random_values_map.items():
        total_randoms += value
    #print(random_values_map)
    print(str(total_randoms) + " total random values")
    #How many random values <= 0.77?
    total_randoms_77 = 0
    for key, value in random_values_map.items():
        if key <= 0.77:
            total_randoms_77 += value
    print(str(total_randoms_77) + " total random values <= 0.77")
    #Collate random values into bins of size 0.01
    random_values_bins = {}
    for key, value in random_values_map.items():
        bin_number = int(key * 100)
        if bin_number in random_values_bins:
            random_values_bins[bin_number] += value
        else:
            random_values_bins[bin_number] = value

 
 
    # Uncomment the following code to plot the results
    #Using matplotlib, plot the random values as a scatter plot
    # import matplotlib.pyplot as plt
    # plt.scatter(random_values_bins.keys(), random_values_bins.values())
    # plt.show()
    
    # #Using matplotlib, plot the results map as a bar chart
    # plt.bar(results_map.keys(), results_map.values())
    # plt.show()