# python_SimulatePwD_ADL
This is the public repo for using GPT4 to simulate PwD's task breakdown moments during ADLs.

Developed with Python 3.10.10 and GPT-4-1106.

To use:
* Install requirements from requirement.txt
* Insert your own API_KEY in GPTObject.py
* To run the simulation only, run SimManagerJSON.py. The example __main__ function runs 15 epochs of the simulation and logs them to ./logs in a JSON file.
* To run the simulation with an RL agent Interventionist, run RLTest.py. The RL framework is powered by Gymnasium, and is defined in RLInterface.py.



To visualize:
A chat-like visualization tool is included in the ./js folder. This was used to generate the message bubble figure in the paper, but also functions as a website with animations. Simply place your chosen *.json file resulting from running SimManagerJSON in the ./js file and rename it to "your-messages.json". Load ./js/bubbles.html in a web browser.
