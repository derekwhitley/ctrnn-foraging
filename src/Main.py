# Main file for Neuro-evolving CTRNNs
import time
import datetime
import subprocess
import math
import random as rand
import Env
import Resource
import turtle
import tkinter
import GA
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy
import os
from pathlib import Path, PureWindowsPath

import configparser
config = configparser.ConfigParser()
config.read("./config.ini")

SWARM_SIZE              =       int(config['DEFAULT']['SWARM_SIZE'])
POPULATION_SIZE         =       int(config['DEFAULT']['POPULATION_SIZE'])
GENERATIONS             =       int(config['DEFAULT']['GENERATIONS'])
MUTATION_PROBABILITY    =       float(config['DEFAULT']['MUTATION_PROBABILITY'])
CROSSOVER_PROBABILITY   =       float(config['DEFAULT']['CROSSOVER_PROBABILITY'])
ELITISM_FRACTION        =       float(config['DEFAULT']['ELITISM_FRACTION'])
SELECTION               =       str(config['DEFAULT']['SELECTION'])
INIT_MODE               =       str(config['DEFAULT']['INIT_MODE'])
LAUNCH_MONITOR          =       config['DEFAULT'].getboolean('LAUNCH_MONITOR')
RUN_DURATION            =       int(config['DEFAULT']['RUN_DURATION'])
NET_SIZE                =       int(config['DEFAULT']['NET_SIZE'])
STEP_SIZE               =       float(config['DEFAULT']['STEP_SIZE'])
DATA_DIR               =       str(config['DEFAULT']['DATA_DIR'])

# Colors for console
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

start = time.time()

duration = RUN_DURATION
network_size = NET_SIZE
network_speed = .01

# GA Parameters
swarm_size = SWARM_SIZE
pop_size = POPULATION_SIZE
genome_size = 15
elite_frac = ELITISM_FRACTION
crossover_prob = CROSSOVER_PROBABILITY
mut_prob = MUTATION_PROBABILITY
cur_gen = 1
max_gen = GENERATIONS

experiment_path = os.path.join(r"C:\\", "Users", "JPS' Desktop", "nasa-swarm-data", str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")))
best_agents = os.path.join(experiment_path, "Best_Agents")

plt.rcParams.update({'figure.max_open_warning':0})

# Series of commands to prompt user about storing data upon prgoram execution
store_experiment = input("Do you want to record this experiment? Y/N\n")
if store_experiment == "Y":
    explanation = input("Type in an explanation for this experiment, then press enter.\n")
    # Make a directory and store GA params
    os.mkdir(str(experiment_path))
    read_me_file = open(experiment_path+"/README.txt", "w")
    read_me_file.write("Experiment Description: "+str(explanation)+"\n")
    read_me_file.write("Swarm Size: "+str(SWARM_SIZE)+"\n")
    read_me_file.write("Population Size: "+str(POPULATION_SIZE)+"\n")
    read_me_file.write("Genome Size: "+str(genome_size)+"\n")
    read_me_file.write("Elitism Fraction: "+str(ELITISM_FRACTION)+"\n")
    read_me_file.write("Crossover Probability: "+str(CROSSOVER_PROBABILITY)+"\n")
    read_me_file.write("Mutation Probability: "+str(MUTATION_PROBABILITY)+"\n")
    read_me_file.write("Max Generations: "+str(GENERATIONS)+"\n")
    os.mkdir(str(best_agents))
    read_me_file.close()

# def convert_screenshot(image):
#     cmd = "convert -density 300"+image+".eps -resize 1024x1024"+image+".png"
#     subprocess.run(cmd)

# Main fitness function, gets used by GA
def fitness_function(individual_swarm):
    # Initializes the environment, which in turn creates everything else (agent, brain, nest, rscs)
    env = Env.Environment(individual_swarm)
    best_agents_inputs = []

    for i in range(RUN_DURATION):
        env.step()
    # total_population_output[num_gen] = generational_total_output
    
    # Setting a default fitness value so the requisite
    # data structures get created 
    fitness_score = 0.0001

    # Main loop for assigning fitness
    for agent in env.agents:
        for i in range(0, len(agent.rscs_detected_hist[0])):
            # Zero behavior: activate sensory neurons upon seeing red rsc
            if agent.rscs_detected_hist[0][i] != 0.0001 and agent.rscs_detected_hist[1][i] != 0.0001:
                # With the revisions to rscs detected, the lowest possible value is 0.0,
                # which indicates a rsc being right on top of an agent
                # Thus, fitness should reward lower scores and penalize higher ones,
                # and a log scale is not likely to be as useful
                if 0. <= abs(agent.brain.current_outputs[-3] - agent.brain.current_outputs[-2]) <= 0.3:
                    fitness_score += abs(math.log(abs(agent.rscs_detected_hist[0][i]+agent.rscs_detected_hist[1][i])))
                
                # First behavior: track a red resource
                # Conditional that checks the difference bt motor neuron outputs and
                # assigns higher fitness based on slower turning           
                    #fitness_score += abs(math.log(abs(agent.rscs_detected_hist[0][i]+agent.rscs_detected_hist[1][i])))

                    # Second behavior: locomote toward a resource
                    #if 0.5 <= agent.brain.current_outputs[-4] <= 1.0:
                    # if 0.1 <= abs(agent.rscs_detected_hist[0][i]+agent.rscs_detected_hist[1][i]) <= 100:
                    #     fitness_score += abs(math.log(1/abs(agent.rscs_detected_hist[0][i]+agent.rscs_detected_hist[1][i])))
        
        # Setting the best fitness and appropriate data for plotting/tracking
        if fitness_score > ga.best_fitness:
            ga.best_outputs = agent.brain.hist_outputs
            ga.best_agent_all_gens = agent
        if ga.population_fitness:
            if len(ga.population_fitness) > 1:
                if fitness_score >= max(ga.population_fitness):
                    ga.best_agent_this_gen = agent
            else:
                ga.best_agent_this_gen = agent
    
    window.update()
    #window.clearscreen()
    return fitness_score

# Initializing the GA
ga = GA.GeneticAlgorithm(swarm_size, pop_size,genome_size,elite_frac,crossover_prob,mut_prob,
                        cur_gen,max_gen,network_speed,duration, network_size, fitness_function)
# Either populating randomly or from seed
#population = ga.populate()
population = ga.populate_from_seed()
population_with_fitness = {}

# Main GA loop
while ga.current_generation <= ga.max_generation:
    gen_time = time.time()
    window = turtle.Screen()
    # window.setup(width=1,height=1)
    window.tracer(0,0)

    # Evaluate the population
    for swarm in range(len(population)):
        swarm_fitness = ga.evaluate(population[swarm])
        population_with_fitness[population[swarm]] = swarm_fitness
    population = ga.fitness_proportionate_selection(population_with_fitness) #mutation is handled inside of this function

    #Update mean and best fitness, print results to terminal
    ga.get_mean_fitness()
    ga.get_best_fitness()
    print("Best Fitness:", str(ga.current_generation)+"/"+str(ga.max_generation), round(max(ga.best_fitness_list), 5))
    print("Best Fitness this Generation:", str(max(ga.population_fitness)))
    print("Mean Fitness this Generation:", str((ga.mean_fitness))+"\n")
    
    # Setting weights to dense so they print fully in files
    dense = ga.best_agent_this_gen.brain.network.weights.todense()
    
    # Write best agent parameters to data directory
    if store_experiment == "Y":
        agent_file = open(best_agents+"/Best_Agent_of_Generation_"+str(ga.current_generation)+".txt", "w")
        agent_file.write(str(ga.best_agent_this_gen.brain.network.taus)+"\n\n")
        agent_file.write(str(ga.best_agent_this_gen.brain.network.biases)+"\n\n")
        agent_file.write(str(dense)+"\n\n")
        agent_file.write(str(max(ga.population_fitness))+"\n\n")
        agent_file.write(str(ga.best_agent_this_gen.brain.network.states)+"\n\n")
        agent_file.close()
        
        sns.set_palette(sns.hls_palette(15, l=.6, s=1))
        # Number of subplots directly relates to what's being tested
        fig, axs = plt.subplots(2)
        #fig.subplots_adjust(hspace=0.5)
        fig.suptitle("Best Agent's Red Sensory Inputs over Neural Outputs of Generation "+str(ga.current_generation))
        #axs[0].set_title("Best Agent's Red Sensory Inputs of Generation " +str(ga.current_generation))
        axs[0].plot(np.arange(0,RUN_DURATION,STEP_SIZE), ga.best_agent_this_gen.brain.neuron_input_left)
        axs[0].plot(np.arange(0,RUN_DURATION,STEP_SIZE), ga.best_agent_this_gen.brain.neuron_input_right)
        axs[0].get_xaxis().set_visible(False)
        axs[0].set(ylabel="Input Intensity")
        axs[0].legend(bbox_to_anchor=(1.13, .98), labels=['Left Eye', 'Right Eye'], loc='upper right', fontsize=4.75)
        
        #axs[1].set_title("Best Agent's Neural Outputs of Generation " +str(ga.current_generation))
        axs[1].plot(np.arange(0,RUN_DURATION,STEP_SIZE), ga.best_agent_this_gen.brain.hist_outputs[:][:])
        axs[1].set(xlabel="Time Step", ylabel="Activation")
        neuron_list = ['Neuron 1 (Input)', 'Neuron 2 (Input)', 'Neuron 3 (Input)', 'Neuron 4 (Input)', 'Neuron 5 (Input)', 'Neuron 6 (Input)',
         'Neuron 7 (Inter)', 'Neuron 8 (Inter)', 'Neuron 9 (Inter)', 'Neuron 10 (Inter)', 'Neuron 11 (Inter)',
          'Neuron 12 (Output)', 'Neuron 13 (Output)', 'Neuron 14 (Output)', 'Neuron 15 (Output)']
        axs[1].legend(bbox_to_anchor=(1.13, .92), labels=neuron_list, loc='upper right', fontsize=4.25)
        
        plt.savefig(best_agents+"/Best_Agent_Neural_Inputs_and_Outputs_of_Generation_"+str(ga.current_generation)+".svg")
        plt.cla()
        plt.clf()
        plt.close(fig)

    # save_screenshot = window.getcanvas()
    # save_screenshot.postscript(file=best_agents+"/Screenshot_of_Best_Agent_of_Generation"+str(ga.current_generation)+".eps")
    # convert_screenshot(best_agents+"/Screenshot_of_Best_Agent_of_Generation"+str(ga.current_generation)+".eps")

    # Keep the last image in the turtle screen
    if ga.current_generation < ga.max_generation:
        time.sleep(10)
        window.clearscreen()

    #print("Duration to Evaluate this Generation: ", str(time.time()-gen_time)+"\n")
    ga.next_generation()

# plot results and store in directory
if store_experiment == "Y":
    plt.figure()
    plt.plot(ga.best_fitness_list)
    plt.plot(ga.mean_fitness_list)
    plt.title('Fitness for Population of '+str(POPULATION_SIZE)+' Agents')
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.legend(['best fitness', 'avg. fitness'])
    # plt.show()
    plt.savefig(experiment_path+"/Fitness_over_Time_Plot.svg")

print("Simulation Duration: ", time.time()-start)