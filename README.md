# python_SimulatePwD_ADL
This is the public repo for using GPT4 to simulate PwD's task breakdown moments during ADLs.

Developed with Python 3.10.10 and GPT-4-1106.

To use:
* Install requirements from requirement.txt
* Insert your own API_KEY in GPTObject.py
* To run the simulation only, run SimManagerJSON.py. The example __main__ function runs 15 epochs of the simulation and logs them to ./logs in a JSON file.
* To run the simulation with an RL agent Interventionist, run RLTest.py. The RL framework is powered by Gymnasium, and is defined in RLInterface.py.
