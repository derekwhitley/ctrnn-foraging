# # Generates the code for the agent brain
from CTRNN import CTRNN
import numpy as np
#import Agent
import math
import random as rand
import configparser
config = configparser.ConfigParser()
config.read("./config.ini")

RUN_DURATION              =       int(config['DEFAULT']['RUN_DURATION'])
NET_SIZE                  =       int(config['DEFAULT']['NET_SIZE'])
STEP_SIZE                 =       float(config['DEFAULT']['STEP_SIZE'])

#print(Agent.fov_distance)

class Brain:
    def __init__(self, individual_swarm, run_duration=RUN_DURATION, net_size=NET_SIZE, step_size=STEP_SIZE): # step_size should never be < 0.02; should be 1 > x > 0.02
        # Sets the simulation run duration
        self.run_duration = run_duration
        # Sets network size
        self.net_size = net_size
        # Sets brain step size compared to simulation duration
        self.step_size = step_size
        # Initializes the CTRNN
        self.network = individual_swarm #CTRNN(size=self.net_size,step_size=self.step_size)
        # Current outputs of len(net_size)
        self.hist_outputs = []
        self.current_outputs = []
        self.neuron_input_left = []
        self.neuron_input_right = []
        # Initial outputs for Phase 0 Shaping
        # self.network.randomize_outputs(.01, .05)
        # Wider range of outputs for Phase I shaping
        self.network.randomize_outputs(.01, .2)
        # Try (0.1, 0.2) as range
        # For sanity in generalization, fix the range, e.g., (0.01, 0.01)
        # Initial states for Phase 0 Shaping
        # self.network.randomize_states(.01, .05)
        # Wider range of states for Phase I shaping
        self.network.randomize_states(.01, .2)
        # Starting parameter
        # self.starting_parameter = starting_parameter
        # self.starting_parameter = starting_parameter
        # if self.starting_parameter == 'zeroize':
        #     self.starting_parameter = 0.0
        self.precision = 5


    def step(self, rscs_detected, num_steps=1):
        # Step through network
        # print("Before Outputs:", self.network.outputs)
        # print("Before States:", self.network.states)

        for _ in range(int(num_steps/self.step_size)):
            
            # Input neurons
            neuron_input = rscs_detected # [Lredvalue, Rredvalue, Lgreenvalue, Rgreenvalue, Lbluevalue, Rbluevalue]
            self.neuron_input_left.append(neuron_input[0])
            self.neuron_input_right.append(neuron_input[1])
            
            # Makes a list of external inputs for the entire network size
            if len(neuron_input) < self.net_size:
                for j in range(6, self.net_size):
                    neuron_input.append(0.0001)
                
            self.network.euler_step(neuron_input)         
            # Clamping neurons to bootstrap shaping
            # Green Neurons
            self.network.outputs[2] = 0.0
            self.network.outputs[3] = 0.0
            # Blue Neurons
            self.network.outputs[4] = 0.0
            self.network.outputs[5] = 0.0
            # Inter Neurons
            self.network.outputs[6] = 0.0
            self.network.outputs[7] = 0.0
            self.network.outputs[8] = 0.0
            self.network.outputs[9] = 0.0
            #self.network.outputs[10] = 0.0
            # Forward Neuron
            self.network.outputs[11] = 0.0
            # Left/Right Motor Neurons
            #self.network.outputs[12] = 0.0
            #self.network.outputs[13] = 0.0
            # Grasping Neuron
            self.network.outputs[14] = 0.0

            self.hist_outputs.append([self.network.outputs[i] for i in range(self.net_size)])

            #print("These are my outputs", self.hist_outputs[-1])

        self.current_outputs = np.asarray(self.hist_outputs[-1])
        # print("After Weights:\n"+str(self.network.weights))
        # print("After Taus:", self.network.taus, "\n")
        # print("After Biases:", self.network.biases, "\n")
        # print("After Outputs:", self.current_outputs, "\n")
