# # Code to test a selected agent's orientation ability
# # within a simulation not subjected to evolution
import Env
import Resource
import CTRNN
import turtle
import numpy as np
import matplotlib.pyplot as plt
import Stats

# change config params to readME params
import configparser
config = configparser.ConfigParser()
config.read("./config.ini")

POPULATION_SIZE         =       int(config['DEFAULT']['POPULATION_SIZE'])
RUN_DURATION            =       int(config['DEFAULT']['RUN_DURATION'])
NET_SIZE                =       int(config['DEFAULT']['NET_SIZE'])
STEP_SIZE               =       float(config['DEFAULT']['STEP_SIZE'])

population_size = POPULATION_SIZE
duration = RUN_DURATION
network_size = NET_SIZE
network_speed = .01

def get_taus_from_file(file):
    # If taus are not fixed at 1, run this function
    count = 1
    seed_taus = ""
    bad_chars = ['[', ']', '\n']
    for line in file:
        if 1 <= count <= 3:
            seed_taus += line
            #print("Taus " + line)
        count += 1
    for item in seed_taus:
        for char in bad_chars:
            if item == char:
                seed_taus = seed_taus.replace(item, '')
    for elem in seed_taus:
        ''.join(elem)
    # Converting strings to lists to further modify values
    # and make it easily iterable
    seed_taus = list(seed_taus)
    new_taus = []
    new_list_of_taus = []
    for val in seed_taus:
        if val != ' ':
            new_taus.append(val)
        else:
            new_list_of_taus.append(new_taus)
            new_taus = []
    new_list_of_taus.append(new_taus)
    # Removing empty list artifacts
    for x in new_list_of_taus[:]:
        if len(x) == 0:
            new_list_of_taus.remove(x)
    # Joining lists within bigger list
    for i in range(len(new_list_of_taus)):
        new_list_of_taus[i] = [''.join(new_list_of_taus[i])]
    for z in new_list_of_taus:
        #print(z)
        for q, g in enumerate(z):
            z[q] = float(g)
    # Final biases is now a list of floats of the appropriate values taken from the file
    final_taus = []
    for i in new_list_of_taus:
        for j in i:
            final_taus.append(j)
    #print("Final Biases:", final_biases)
    return final_taus

def get_biases_from_file(file):
    count = 1
    seed_biases = ""
    bad_chars = ['[', ']', '\n']
    for line in file:
        # If taus are not fixed at 1
        # if 5 <= count <= 7:
        # If taus are fixed at 1
        if 3 <= count <= 5:
            seed_biases += line
            #print("Biases " + line)
        count += 1
    for item in seed_biases:
        for char in bad_chars:
            if item == char:
                seed_biases = seed_biases.replace(item, '')
    for elem in seed_biases:
        ''.join(elem)
    # Converting strings to lists to further modify values
    # and make it easily iterable
    seed_biases = list(seed_biases)
    #print(seed_biases)
    new_biases = []
    new_list_of_biases = []
    for val in seed_biases:
        if val != ' ':
            new_biases.append(val)
        else:
            new_list_of_biases.append(new_biases)
            new_biases = []
    new_list_of_biases.append(new_biases)
    # Removing empty list artifacts
    for x in new_list_of_biases[:]:
        if len(x) == 0:
            new_list_of_biases.remove(x)
    #print("New list after removing empty lists:", new_list_of_biases, '\n')
    # Joining lists within bigger list
    for i in range(len(new_list_of_biases)):
        new_list_of_biases[i] = [''.join(new_list_of_biases[i])]
    #print("New list after joining lists within:", new_list_of_biases)
    for z in new_list_of_biases:
        #print(z)
        for q, g in enumerate(z):
            z[q] = float(g)
    # Final biases is now a list of floats of the appropriate values taken from the file
    final_biases = []
    for i in new_list_of_biases:
        for j in i:
            final_biases.append(j)
    #print("Final Biases:", final_biases)
    return final_biases

def get_weights_from_file(file):
    count = 1
    seed_weights = ""
    bad_chars = ['[', ']', '\n']
    for line in file:
        # If taus are not fixed at 1:
        #if 9 <= count <= 68:
        # If taus are fixed at 1:
        if 7 <= count <= 66:
            seed_weights += line
            #print("Line "+str(count)+" "+line)
        count += 1
    for item in seed_weights:
        for char in bad_chars:
            if item == char:
                seed_weights = seed_weights.replace(item, '')
    for elem in seed_weights:
        ''.join(elem)
    seed_weights = list(seed_weights)
    #print(seed_weights)
    new_weights = []
    new_list_of_weights = []
    for i in range(len(seed_weights)):
        if seed_weights[i] != ' ':
            new_weights.append(seed_weights[i])
            if i == len(seed_weights)-1:
                new_list_of_weights.append(new_weights)
        else:
            new_list_of_weights.append(new_weights)
            new_weights = []
    # Removing empty list artifacts
    for x in new_list_of_weights[:]:
        if len(x) == 0:
            new_list_of_weights.remove(x)
    # Joining lists within bigger list
    for i in range(len(new_list_of_weights)):
        new_list_of_weights[i] = [''.join(new_list_of_weights[i])]
    for z in new_list_of_weights:
        for q, g in enumerate(z):
            z[q] = float(g)
    almost_final_weights = []
    final_weights = []
    for i in new_list_of_weights:
        for j in i:
            almost_final_weights.append(j)
            if len(almost_final_weights) == 15:
                final_weights.append(almost_final_weights)
                almost_final_weights = []
    #print("Final weights:", final_weights)
    return final_weights

# file = open(r"C:\Users\JPS' Desktop\nasa-swarm-data\2020_08_06_20_13_03\Best_Agents\Best_Agent_of_Generation_294.txt")
# get_biases_from_file(file)

# # Redeclaring file variable because of an odd closing error
# # that occurs otherwise; probably a better fix;
# # just wasn't immediately obvious/necessary to solve
# file = open(r"C:\Users\JPS' Desktop\nasa-swarm-data\2020_08_06_20_13_03\Best_Agents\Best_Agent_of_Generation_294.txt")
# get_weights_from_file(file)

# #
# # Creating the actual test simulation
# #

# Since populate in the GA creates the agent population,
# I'm creating a function to do the same here
def replicate():
    for k in range(population_size):
        c = CTRNN.CTRNN(size=network_size, step_size=network_speed)
        # Assign initial weights
        weights = get_weights_from_file(file = open(r"C:\Users\JPS' Desktop\nasa-swarm-data\2021_04_07_10_57_42\Best_Agents\Best_Agent_of_Generation_2.txt"))
        #"C:\Users\JPS' Desktop\nasa-swarm-data\2020_08_06_20_13_03\Best_Agents\Best_Agent_of_Generation_294.txt"
        for i in range(network_size):
            for j in range(network_size):
                #print(weights[i][j])
                c.weights[i, j] = weights[i][j]
        # Assign Taus
        #taus = get_taus_from_file(file = open(r"C:\Users\JPS' Desktop\nasa-swarm-data\2021_03_26_09_07_05\Best_Agents\Best_Agent_of_Generation_4.txt"))
        for i in range(network_size):
            # If taus are not fixed at 1:
            # c.taus[i] = taus[i]
            # If taus are fixed at 1:
            c.taus[i] = 1.
        # Assign biases
        biases = get_biases_from_file(file = open(r"C:\Users\JPS' Desktop\nasa-swarm-data\2021_04_07_10_57_42\Best_Agents\Best_Agent_of_Generation_2.txt"))
        #"C:\Users\JPS' Desktop\nasa-swarm-data\2020_08_06_20_13_03\Best_Agents\Best_Agent_of_Generation_294.txt"
        for i in range(network_size):
            #print(biases[i])
            c.biases[i] = biases[i]
    return c

# List to track sensory input over time
sens_input_hist = []
# List to track angle differential over time
angle_differential_hist = []
# List to track sensory input over time
avg_sens_input_hist = []
# List to track angle differential over time
avg_angle_differential_hist = []
# List to track outputs
sens_activation_hist = []
# Initializaing relevant objects
individual = replicate()
stats = Stats.Stats()
current_run = 1
max_runs = 10

# Running the simulation and tracking stats
while current_run <= max_runs:
    env = Env.Environment(individual)
    print("Run #"+str(current_run))
    window = turtle.Screen()
    window.tracer(0,0)
    for i in range(duration):
        #print("I am stepping")
        env.step()
        for agent in env.agents:
            sens_input_hist.append((agent.rscs_detected[0], agent.rscs_detected[1]))
            angle_differential_hist.append(abs(agent.turtle.heading() - agent.turtle.towards(env.rscs_info[0][0])))
            sens_activation_hist.append(agent.brain.hist_outputs[:][:])
        avg_sens_input_hist.append(sens_input_hist)
        avg_angle_differential_hist.append(angle_differential_hist)
    # sens_input_hist = np.asarray(sens_input_hist)
    # angle_differential_hist = np.asarray(angle_differential_hist)
    sens_input_hist = []
    angle_differential_hist = []
    sens_activation_hist = []

    #print("Run" + str(current_run))
    current_run += 1
    window.update()
    window.clearscreen()

avg_sens_input_hist = np.asarray(avg_sens_input_hist)
avg_angle_differential_hist = np.asarray(avg_angle_differential_hist)

#print(avg_sens_activ_hist)

#print(np.shape(avg_sens_input_hist), "\n")
# In a 2D array, array[r,c] indexes row,column
# In a 3D array, which we have here, array[n][r, c]
# will pick out the nth array and then a row, column position in that array
# for i in range(len(avg_angle_differential_hist)):
#     #print("Index"+str(i)+":", avg_sens_input_hist[i][:,0], "\n")
#     #print("Index"+str(i)+":", avg_sens_input_hist[i][:,1], "\n")
#     plt.plot(avg_sens_input_hist[i][:,0])
#     plt.plot(avg_sens_input_hist[i][:,1])
# plt.show()

# plt.plot(np.arange(0,RUN_DURATION,STEP_SIZE), avg_sens_activ_hist)
# plt.show()

# Avg seq heading and sens input produces separate lines for angle differential
#stats.avg_seq_heading_and_sens_input(avg_sens_input_hist, avg_angle_differential_hist, max_runs)

# Overlaid heading and sens input just plots one line for each list w/in the larger array
#stats.avg_ovrlaid_heading_and_sens_input(avg_sens_input_hist, avg_angle_differential_hist, max_runs)