"""
    A Genetic algorithm for the neuroevolution of CTRNNs
"""
import random
import math
import numpy as np
import sys
import CTRNN
import matplotlib.pyplot as plt

class GeneticAlgorithm:
    def __init__(self, swarm_size, population_size, genotype_size, elitism_fraction,
                crossover_probability, mutation_probability, current_generation,
                max_generation, network_speed, duration, network_size, fitness_function):
        self.swarm_size = swarm_size
        self.population_size = population_size
        self.genotype_size = genotype_size
        self.elitism_fraction = elitism_fraction
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.current_generation = current_generation
        self.max_generation = max_generation
        self.fitness_function = fitness_function
        #self.parameter_min = -5.0
        #self.parameter_max = 5.0

        self.network_size = network_size
        self.network_speed = network_speed
        self.duration = duration

        self.population_outputs = {}
        self.generation_fitness = {}
        self.population_fitness = []
        self.mean_fitness_list = [0]
        self.best_fitness_list = [0]
        self.best_outputs = []
        self.mean_fitness = 0.0
        self.best_fitness = 0.0
        self.best_agent_all_gens = ""
        self.best_agent_this_gen = ""

    def get_taus_from_file(self, file):
        count = 1
        seed_taus = ""
        bad_chars = ['[', ']', '\n']
        for line in file:
            if 1 <= count <= 3:
                seed_taus += line
                #print("Biases " + line)
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

    def get_biases_from_file(self, file):
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

    def get_weights_from_file(self, file):
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

    def next_generation(self):
        self.current_generation += 1
        self.population_fitness = []

    def get_mean_fitness(self):
        if len(self.population_fitness) > 0:
            self.mean_fitness = sum(self.population_fitness)/len(self.population_fitness)
        else:
            print(self.population_fitness)
            self.mean_fitness = 0.0
        
        self.mean_fitness_list.append(self.mean_fitness)

        return self.mean_fitness

    def get_best_fitness(self):
        self.best_fitness = max(self.population_fitness)
        self.best_fitness_list.append(self.best_fitness)

    
    """
    Collect data into fixed-length chunks or blocks
    #grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    Taken from python recipes
    """
    def grouper(iterable, n, fillvalue=None):
        args = [iter(iterable)] * n
        return izip_longest(fillvalue=fillvalue, *args)

    def populate(self):
        # Generate initial population from random
        population = []
        for k in range(self.population_size):
            c = CTRNN.CTRNN(size=self.network_size, step_size=self.network_speed)
            # Assign initial weights
            # Need to clamp blue and green neurons and their 
            # connections since they are not currently being used
            for i in range(self.network_size):
                for j in range(self.network_size):
                    # Prevent input-to-output connections
                    if i < 6 and j > self.network_size-4:
                        c.weights[i, j] = 0.0001
                    # Prevent output-to-input and
                    # inter-to-input connections
                    elif i > 5 and j < 6:
                        c.weights[i, j] = 0.0001
                    else:
                        c.weights[i, j] = [val for val in [random.uniform(-10.0, 10.0) for i in range(1)] if val !=0][0]
                        #c.weights[i, j] = random.uniform(-2.5, 0.0)
            # Assign Taus
            for i in range(self.network_size):
                #c.taus[i] = random.uniform(0.1, 1.)
                c.taus[i] = 1.0

            # Assign biases
            for i in range(self.network_size):
                c.biases[i] = random.uniform(-5., 5.)
                #c.biases[i] = 1.0

            population.append(c)
        
        return population

    def populate_from_seed(self):
        #Generate initial population from seed
        population = []
        for k in range(self.population_size):
            c = CTRNN.CTRNN(size=self.network_size, step_size=self.network_speed)
            # Assign initial weights
            weights = self.get_weights_from_file(file = open(r"C:\Users\JPS' Desktop\nasa-swarm-data\2021_04_09_11_36_03\Best_Agents\Best_Agent_of_Generation_25.txt"))
            #"C:\Users\JPS' Desktop\nasa-swarm-data\2020_08_06_20_13_03\Best_Agents\Best_Agent_of_Generation_294.txt"
            for i in range(self.network_size):
                for j in range(self.network_size):
                    #print(weights[i][j])
                    c.weights[i, j] = weights[i][j]
            # Assign Taus
            # If Taus are not fixed
            # taus = self.get_taus_from_file(file = open(r"C:\Users\JPS' Desktop\nasa-swarm-data\2021_02_16_12_46_01\Best_Agents\Best_Agent_of_Generation_47.txt"))
            for i in range(self.network_size):
                #c.taus[i] = taus[i]
                # If taus are fixed
                c.taus[i] = 1.
            # Assign biases
            biases = self.get_biases_from_file(file = open(r"C:\Users\JPS' Desktop\nasa-swarm-data\2021_04_09_11_36_03\Best_Agents\Best_Agent_of_Generation_25.txt"))
            #"C:\Users\JPS' Desktop\nasa-swarm-data\2020_08_06_20_13_03\Best_Agents\Best_Agent_of_Generation_294.txt"
            for i in range(self.network_size):
                #print(biases[i])
                c.biases[i] = biases[i]
            population.append(c)        
        
        return population

    def evaluate(self, individual):
        # Evaluate
        fitness = self.fitness_function(individual)
        if self.best_fitness < fitness:
            self.best_fitness = fitness
        self.population_fitness.append(fitness)
        return fitness

    def mutate(self, individual):
        # Mutate the individual with some probability
        attrs = ["biases", "taus", "weights"]
        for attr in attrs:
            if attr == "biases":
                for bias in range(len(getattr(individual,attr))):
                    #print(str(attr), str(getattr(individual, attr)[bias]))
                    attr_value = getattr(individual, attr)
                    if random.uniform(0.01, 1.0) <= self.mutation_probability:
                        #print("Biases mutated")
                        mutation = random.uniform(-1., 1.)
                        #mutation = 0.0
                        # #print("Mutating " + attr + ": " + str(attr_value) + "->" + str(attr_value))
                        attr_value[bias] += mutation
                        setattr(individual, attr, attr_value)
            elif attr == "taus":
                for tau in range(len(getattr(individual,attr))):
                    #print(str(attr), str(getattr(individual, attr)[tau]))
                    attr_value = getattr(individual, attr)
                    if random.uniform(0.01, 1.0) <= self.mutation_probability:
                        #print("Taus mutated")
                        #mutation = random.uniform(0.1, 1.)
                        mutation = 0.0
                        # #print("Mutating " + attr + ": " + str(attr_value) + "->" + str(attr_value))
                        #attr_value[tau] = mutation
                        attr_value[tau] += mutation
                        setattr(individual, attr, attr_value)
            else:
                weightmatrix = getattr(individual, attr)
                #print("weightmatrix: "+str(weightmatrix))
                for weights in weightmatrix:
                    for i in range(weights.shape[0]):
                        attr_value = getattr(individual, attr)
                        if random.uniform(0.01, 1.0) <= self.mutation_probability:
                            #print("Weights mutated")
                            mutation = random.uniform(-0.5, 0.5)
                            #mutation = 0.0
                            #print("Mutating weights"+str(weights.indices)+": " + str(weights.data[i]) + "->" + str(weights.data[i]+mutation))
                            weights.data[i] += mutation
                setattr(individual, attr, weightmatrix)

        
        return individual

    def crossover(self, ind_a, ind_b):
        # Breed a new organism from two of the previous generation
        ##print("Crossover not setup yet.")
        if random.uniform(0.1,1.) <= self.crossover_probability:
            ind_b.taus = ind_a.taus
        if random.uniform(0.1,1.) <= self.crossover_probability:
            ind_b.weights = ind_a.weights
        if random.uniform(0.1,1.) <= self.crossover_probability:
            ind_b.biases = ind_a.biases
        # if random.uniform(0.,1.) <= self.crossover_probability:
        #     ind_b.states = ind_a.states

        return ind_b

    def fitness_proportionate_selection(self, population_with_fitness):
        #Sort by highest fitness
        ranked_population = sorted(population_with_fitness.items(), key=lambda items: items[1], reverse=True)#{k: v for k, v in }
        
        number_of_elites = int(math.ceil(self.elitism_fraction*self.population_size))
        #print("Num Elites:", number_of_elites)
        elites = []
        elites_values = []
        if number_of_elites == 1:
            elites.append(ranked_population[0][0])
            elites_values.append(ranked_population[0][1])
        else:
            for i in range(0, number_of_elites):
                #print("Ranked population", ranked_population)
                elites.append(ranked_population[i][0])
                elites_values.append(ranked_population[i][1])
        
        #print("Elites", elites)
        #print("Elite Values", elites_values)

        elite_sum = sum(elites_values)
        elite_probs = []

        for i in range(0, len(elites)):
            proportionate_fitness = (elites_values[i]/elite_sum)
            elite_probs.append(proportionate_fitness)
        #print("Elite Probabilities", elite_probs)

        for ind in population_with_fitness:
            rand_elite = np.random.choice(elites, 1, p=elite_probs)[0]
            if (not ind in elites):
                #and population_with_fitness[rand_elite] != population_with_fitness[ind]):
                if random.uniform(0.,1.) <= self.crossover_probability:
                    ind = self.crossover(rand_elite, ind)
                self.mutate(ind)
            else:
                self.mutate(rand_elite)

        return list(population_with_fitness)

    def tournament_selection(self, population_with_fitness):
        random.shuffle(population_with_fitness)
        for A, B in grouper(population_with_fitness, 2):
            if A > B:
                self.crossover(A, B)
                self.mutate(B)
            else:
                self.crossover(B, A)
                self.mutate(A)


