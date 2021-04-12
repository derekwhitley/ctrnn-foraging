import turtle
import tkinter
import random
from CTRNN import CTRNN
import numpy as np
import matplotlib.pyplot as plt
from decimal import *


# alfred = turtle.Turtle()
# res = turtle.Turtle()
# res.goto(.5, 0)
# print(alfred.distance(res.pos()))
# #los = turtle.Turtle()
# turtle.done()
# res.goto([-50,150])

# alfred.forward(100) #movement in pixels
# alfred.left(45) #takes in an angle in degrees
# alfred.forward(100)
# alfred.right(90)
# alfred.forward(100)

# alfred.color("black", "cyan") # takes standard, RGB, and Hex values
#                     # a0 = outline color
#                     # a1 = fill color

# alfred.begin_fill()
# alfred.forward(100)
# alfred.setheading(90)    # another way to orient movement; see documentation
#                          # doing it this way removes need for calculation (90 = north)
# alfred.forward(100)
# alfred.left(90)
# alfred.forward(100)
# alfred.left(90)
# alfred.forward(100)
# alfred.end_fill()

# alfred.penup()  # takes the "pen" and moves the turtle without drawing a line
# alfred.forward(10)
# alfred.pendown()    # sets the pen down to resume drawing lines

# alfred.begin_fill()
# alfred.forward(100)
# alfred.left(90)
# alfred.forward(100)
# alfred.left(90)
# alfred.forward(100)
# alfred.left(90)
# alfred.forward(100)
# alfred.end_fill()

# alfred.getscreen().bgcolor("black")
# alfred.color("red", "yellow")
# #alfred.speed(0)
# alfred.left(90)

# los.color("white")
# los.pendown()
# los.setheading(alfred.heading()-30)
# los.forward(200)
# los.penup()
# los.goto(alfred.pos())
# los.pendown()
# los.setheading(alfred.heading()+30)
# los.forward(200)
# los.penup()

# res.color("white")
# res.speed(0)
# print("field of view: " + str([alfred.heading()-30, alfred.heading()+30]))
# print("heading: " + str(alfred.heading()))

# if  (alfred.heading()-30 <= alfred.towards(res.pos()) <= alfred.heading()+30):
#     print("Alfred can SEE resources")

# print(alfred.towards(res.pos()))
# turtle.done()

# How to get resource location from list
# for i in detected_rscs:
#     print(i)
#     print(str(rscs[i].loc))

# How to get FoV, Agent Heading, and Agent Position as print statements
# print("Field of view: " + str([agent.agent.heading()-30, agent.agent.heading()+30]))
# print("Agent Heading: " + str(agent.agent.heading()))
# print("Agent Position:" + str(agent.agent.pos()))
# print("\n")

# alfred = turtle.Turtle()
# alfred.color("white")
# alfred.getscreen().bgcolor("black")

# for i in range(0, 360):
#     alfred.forward(10)
#     alfred.left(random.choice([-15, 15]))

# turtle.done()

# Draws pretty hexagons
# for i in range(0, 360):
#     alfred.forward(10)
#     alfred.left(random.choice([-45, 45]))

# Creating a list to track detected resources
# detected_rscs = agent.rscs_detected
# print(detected_rscs)
# for i in range(len(detected_rscs)):
#     print(detected_rscs[i][1])
        
# How to get resource location from list
# when agent.rscs_detected returns the iterable
# for i in detected_rscs:
#     print(i)
#     print(str(rscs[i].loc))

# # params
# run_duration = 250
# net_size = 2
# step_size = 0.01

# # set up network
# network = CTRNN(size=net_size,step_size=step_size)

# network.taus = [1.,1.]
# network.biases = [-2.75,-1.75]
# network.weights[0,0] = 4.5
# network.weights[0,1] = 1.00
# network.weights[1,0] = -1.00
# network.weights[1,1] = 4.5

# # network.taus = [1.15,1.15]
# # network.biases = [-3.00,-2.00]
# # network.weights[0,0] = 4.65
# # network.weights[0,1] = 1.15
# # network.weights[1,0] = -1.15
# # network.weights[1,1] = 4.65

# initialize network w/ initially random outputs
# network.randomize_outputs(0.1,0.2)

# simulate network
# outputs = []
# for _ in range(int(run_duration/step_size)):
#     #print("I am the outputs:", outputs)   
#     # input neurons
#     # input_neurons = agent.detected_rscs() #[redvalue, greenvalue, bluevalue]
#     # for j in range(3, net_size):
#     #     input_neurons.append(0)
#     network.euler_step([0]*net_size) # zero external_inputs
#     outputs.append([network.outputs[i] for i in range(net_size)])

#print("I am outputs:", outputs[0][0])
#print("I am maybe different outputs:", outputs[0][:])
# outputs = np.asarray(outputs)
# print("I am the len of outputs:", len(outputs))
# print("I am something else:", len(outputs[:,0]))
# print("I am something else else:", len(outputs[:,1]))
#print("I am the current outputs:", outputs[:,0])

# plot oscillator output
# plt.plot(np.arange(0,run_duration,step_size),outputs[:,0])
# plt.plot(np.arange(0,run_duration,step_size),outputs[:,1])
# plt.xlabel('Time')
# plt.ylabel('Neuron outputs')
# plt.show()

# alfred = turtle.Turtle()
# print("Distance 1:", alfred.distance(225.00,-49.00))
# print("Distance 2:", alfred.distance(186.00,-160.00))
# turtle.done()

# Original fix for bottom-right quadrant FoV problem; keeping in case other solution breaks
# if self.agent.heading() == 0.0:
#     if self.agent.towards(rscs_info[i][0]) <= self.agent.heading()+self.left_eye:
#         print("Resource " + str(i) + " detected at:", self.agent.towards(rscs_info[i][0]), "\nColor:", rscs_info[i][1])
#         all_rscs_detected.append((rscs_info[i][0], rscs_info[i][1]))

#     # This loop has to be updated based on whatever angle the 
#     # eyes allow for in FoV. May be a better way to address this. 
#     # Need to think on it. 
#     elif self.agent.heading()+300 <= self.agent.towards(rscs_info[i][0]) <= self.agent.heading()+360:
#         print("Resource " + str(i) + " detected at:", self.agent.towards(rscs_info[i][0]), "\nColor:", rscs_info[i][1])
#         all_rscs_detected.append((rscs_info[i][0], rscs_info[i][1]))

#     else:
#         print("Resource " + str(i) + " Outside FoV")
#         rscs_undetected.append(i)

# def cleanuppool(self):
#     global __evolsearch_process_pool
#     print(__evolsearch_process_pool)

#     print("I'm being called")
#     if __evolsearch_process_pool != None:
#         print("I'm trying to terminate")
#         __evolsearch_process_pool.terminate()

# Alternative move function w/o neural input
# def move(self, steps, rscs_info):
#     count = 1
#     for i in range(steps):
#         print("Step:", count)
#         self.detect_fov(rscs_info)
#         self.turtle.forward(self.max_forward_travel)
#         self.turtle.left(random.choice([self.max_turning_radius, 0, -self.max_turning_radius]))
#         count+=1

#print("I'm a random value:", [val for val in [random.uniform(-5.0, 5.0) for i in range(1)] if val !=0][0])

# Prints neural outputs
# plt.plot(np.arange(0,env.agents[0].brain.run_duration,env.agents[0].brain.step_size), hist_outputs[:,:])

# root=tkinter.Tk()
# root.withdraw()
# c=tkinter.Canvas(master=root)
# t=turtle.RawTurtle(c)
# t.fd(5)
# print(t.xcor()) # outputs 5.0

# alfred = turtle.Turtle()
# print(alfred.pos())
# turtle.tracer(0,0)
# alfred.forward(100)
# #turtle.bye()
# print(alfred.pos())
# #turtle.update()

# window = turtle.Screen()

# file2 = open(r"C:\Users\JPS' Desktop\nasa-swarm-data\2020_07_26_11_25_23 (Highest Fitness to Date)\Best_Agents\Best_Agent_of_Generation_19.txt")
# count = 1

# seed_biases = ""
# seed_weights = ""

# for line in file2:
#     if 3 <= count < 6:
#         seed_biases += line
#         #print("Biases " + line)
#     # Weights
#     if 7 <= count < 67:
#         seed_weights += line
#         #print("Line "+str(count)+" "+line)
#     count += 1
# #print("Seed Biases:", np.asarray(seed_biases))
# #print("Seed Weights:", np.asarray(seed_weights))
# bad_chars = ['[', ']']
# for item in seed_biases:
#     for char in bad_chars:
#         if item == char:
#             seed_biases = seed_biases.replace(item, '')

# for item in seed_biases:
#     ' '.join([])

#print(seed_biases)

# alfred = turtle.Turtle()

# turtle.done()

#print([i for i in range(1, 5)][0])
# a = np.random.rand(2, 2)
# [a, b] = plt.plot(a)
# plt.legend([a, b], ('1', '2'))
# plt.show()

# Cleaning up Fitness Function in Main
        # Should we make an attribute that adds to fitness based on the amount
        # of time an agent spends looking at a resource?
        # This method indicates fitness based on just the ability to fire the motors and detect something,
        # not to fire the motors for the purpose of detecting a resource or staying oriented
        # toward a resource once one has been seen.
        # relative_angle = 0.
        #if abs(agent.rscs_detected[0]-agent.rscs_detected[1]) > 0:
            # fitness_score += 1/abs(agent.rscs_detected[0]-agent.rscs_detected[1])-
        
        # if abs(agent.turtle.heading() - agent.turtle.towards(env.rscs_info[0][0])) > 180:
        #     relative_angle = abs((agent.turtale.heading() - agent.turtle.towards(env.rscs_info[0][0])) - 360)    
        #     fitness_score = 1/relative_angle
        #     #print("Relative Angle:", relative_angle)
        # else:
        #     if (agent.turtle.heading() - agent.turtle.towards(env.rscs_info[0][0])) != 0.:
        #         fitness_score = 1/(agent.turtle.heading() - agent.turtle.towards(env.rscs_info[0][0]))
        #         relative_angle = abs((agent.turtle.heading() - agent.turtle.towards(env.rscs_info[0][0])))
        #         #print("Relative Angle:", relative_angle)
        #     else:
        #         fitness_score = 1/((agent.turtle.heading() - agent.turtle.towards(env.rscs_info[0][0])) + 0.000000001)
        #         env.intelligent_agents.append(agent)
        #         print("Perfect Orientation Achieved")
        #         relative_angle = abs((agent.turtle.heading() - agent.turtle.towards(env.rscs_info[0][0])))
        # if relative_angle <= 60.0 and agent.rscs_detected[0] != 0.0001 and agent.rscs_detected[1] != 0.0001:
        
        # Try imposing a penalty when agents turn away from resources, so fitness
        # increases when they've attended but decreases if they turn away

                    # if agent.rscs_detected[0] or agent.rscs_detected[1] <= 0.0001:
                    #     fitness_score -= .25*(math.log(1/abs(agent.rscs_detected_hist[0][i]-agent.rscs_detected_hist[1][i])))
                # else:
                #     fitness_score += math.log(1/(abs((agent.rscs_detected[0]-agent.rscs_detected[1])+.000001)))
            
        #print("Heading - Towards: ", agent.turtle.heading() - agent.turtle.towards(env.rscs_info[0][0]))
        #print("Towards: ", agent.turtle.towards(env.rscs_info[0][0]))
        #print("Agent Heading: ", agent.turtle.heading())
        #print("Agent's Current Fitness:", fitness_score)
        #print("Current Neural Outputs:", agent.brain.current_outputs)
        #print("Historical Neural Outputs:", agent.brain.hist_outputs)

        #print("Sensory Inputs:", agent.rscs_detected[0], agent.rscs_detected[1])
        # Is the cause for the difference of 0.0 an artifact of rounding???
        # If round flattens the value to 0.0 instead of something like 0.000001, then
        # it'll result in a /0 error
        #if abs(agent.rscs_detected_hist[0][i]-agent.rscs_detected_hist[1][i]) != 0.:

# Cleaning up motor function in Agent
        # Check that NaNs aren't being inserted into the move action
        #if not math.isnan(round((self.brain.current_outputs[-4]*self.max_forward_travel), self.precision)):
        #     self.turtle.forward(round(self.brain.current_outputs[-4]*self.max_forward_travel, 2))
            
            # Sets turtle heading based on output from heading motor neurons
            # adjusted_left_heading = self.brain.current_outputs[-3]*self.max_turning_radius
            # adjusted_right_heading = self.brain.current_outputs[-2]*-self.max_turning_radius
            # self.turtle.left(adjusted_left_heading+adjusted_right_heading)
        # Adjusting to left/right differential wheel drive
        #if (self.brain.current_outputs[-3] - self.brain.current_outputs[-2]) >= self.max_turning_radius:
            #self.turtle.right(self.max_turning_radius)
        # elif (self.brain.current_outputs[-3] - self.brain.current_outputs[-2]) <= -self.max_turning_radius:
        #     self.turtle.right(-self.max_turning_radius)

# Cleaning up Main
    # Plots neural outputs of best agent in a generation
    # plt.plot(np.arange(0,RUN_DURATION,STEP_SIZE), ga.best_agent_this_gen.brain.hist_outputs[:][:])
    # plt.savefig(best_agents+"/Best_Agent_Neural_Output_of_Generation_"+str(ga.current_generation)+".svg")
    # plt.clf()

    #print("List/Value", len(ga.best_agent_this_gen.brain.hist_outputs[:][:]))
    # output_neurons_left = []
    # output_neurons_right = []
    # for i in range(0, len(ga.best_agent_this_gen.brain.hist_outputs)):
    #     output_neurons_left.append(ga.best_agent_this_gen.brain.hist_outputs[i][0])
    #     output_neurons_right.append(ga.best_agent_this_gen.brain.hist_outputs[i][1])
    
    #print("Length:", len(input_neurons_left))

    # Prints neural outputs

    # for i in range(0, len(env.agents)):
    #     plt.plot(np.arange(0,env.agents[i].brain.run_duration,env.agents[i].brain.step_size), generational_total_output[i][:])
    #     plt.title("Agent:"+str(i))
    #     plt.xlabel('Time (Brain_Time = 100x)')
    #     plt.ylabel('Neuron outputs')
    #     plt.show()

    # best_fit = []
    # mean_fit = []
    # num_gen = 1
    # max_num_gens = GENERATIONS
    # desired_fitness = 0.98
    # #while es.get_best_individual_fitness() < desired_fitness and num_gen < max_num_gens:
    # while num_gen <= max_num_gens:

    #     es.step_generation()

    #     print('Gen #'+str(num_gen)+' Best Fitness = '+str(es.get_best_individual_fitness()))

    #     best_fit.append(es.get_best_individual_fitness())
    #     mean_fit.append(es.get_mean_fitness())

    #     num_gen += 1
            # May want to create env archive file later

        # print results
        # print('Max fitness of population = ',es.get_best_individual_fitness())
        # print('Best individual in population = ',es.get_best_individual())

        # plot results
        # plt.figure()
        # plt.plot(best_fit)
        # plt.plot(mean_fit)
        # plt.xlabel('Generations')
        # plt.ylabel('Fitness')
        # plt.legend(['best fitness', 'avg. fitness'])
        # plt.show()

# Cleaning up old left / right FoV commands in Agent
            #print(left_rscs_detected)
            #closest_blue_rsc = 0.0
            #closest_red_rsc = 0.0
                                # if self.turtle.distance(left_rscs_detected[i][0]) == 0.:
                    #     closest_blue_rsc = 0.0
                    #     self.rscs_detected[4] = round(closest_blue_rsc, self.precision)
                    #     self.rscs_detected_hist[4].append(self.rscs_detected[4])
                    #     self.rscs_detected[5] = round(closest_blue_rsc - (closest_blue_rsc * ((abs(left_degree_offset) / (self.left_eye*2)))), self.precision)
                    #     self.rscs_detected_hist[5].append(self.rscs_detected[5])
                    #     self.closest_blue_rsc_pos = left_rscs_detected[i][0]

                    #if int(self.turtle.distance(left_rscs_detected[i][0])) != 0:
                    #closest_blue_rsc = (int(self.fov_distance)/int(self.turtle.distance(left_rscs_detected[i][0]))) / self.max_grab_dist

                    #closest_blue_rsc = (int(self.fov_distance)/int(self.turtle.distance(left_rscs_detected[i][0]))) / self.max_grab_dist

                                    # elif left_rscs_detected[i][1] == 'blue' and closest_blue_rsc != '':
                #     if int(self.turtle.distance(left_rscs_detected[i][0])) != 0:
                #         next_blue_rsc = (int(self.fov_distance)/int(self.turtle.distance(left_rscs_detected[i][0]))) / self.max_grab_dist
                #         if next_blue_rsc > closest_blue_rsc:
                #             closest_blue_rsc = next_blue_rsc
                #             self.rscs_detected[4] = round(closest_blue_rsc, self.precision)
                #             self.rscs_detected[5] = round(closest_blue_rsc - (closest_blue_rsc * ((abs(left_degree_offset) / (self.left_eye*2)))), self.precision)
                #             self.closest_blue_rsc_pos = left_rscs_detected[i][0]

                                    #print("Check 0")
                    # if self.turtle.distance(left_rscs_detected[i][0]) == 0.:
                    #     closest_red_rsc = 0.0
                    #     self.rscs_detected[0] = round(closest_red_rsc, self.precision)
                    #     self.rscs_detected_hist[0].append(self.rscs_detected[0])
                    #     self.rscs_detected[1] = round(closest_red_rsc - (closest_red_rsc * ((abs(left_degree_offset) / (self.left_eye*2)))), self.precision)
                    #     self.rscs_detected_hist[1].append(self.rscs_detected[1])
                    #     self.closest_red_rsc_pos = left_rscs_detected[i][0]
                    #     #(print("Check 1"))

                                            #print("Check 1")
                        #print(self.turtle.distance(left_rscs_detected[i][0]))
                        #print(left_rscs_detected[i][1])

                                # elif left_rscs_detected[i][1] == 'red' and closest_red_rsc != 0.0:
                #     if int(self.turtle.distance(left_rscs_detected[i][0])) != 0:
                #         next_red_rsc = (int(self.fov_distance)/int(self.turtle.distance(left_rscs_detected[i][0]))) / self.max_grab_dist
                #         if next_red_rsc > closest_red_rsc:
                #             closest_red_rsc = next_red_rsc
                #             self.rscs_detected[0] = round(closest_red_rsc, self.precision)
                #             self.rscs_detected_hist[0].append(self.rscs_detected[0])
                #             self.rscs_detected[1] = round(closest_red_rsc - (closest_red_rsc * ((abs(left_degree_offset) / (self.left_eye*2)))), self.precision)
                #             self.rscs_detected_hist[1].append(self.rscs_detected[1])
                #             self.closest_red_rsc_pos = left_rscs_detected[i][0]
                            # self.red_left_inputs.append(round(closest_red_rsc, self.precision))
                            # self.red_right_inputs.append(round(closest_red_rsc - (closest_red_rsc * ((abs(left_degree_offset) / (self.left_eye*2)))), self.precision))

                                        #print(right_rscs_detected)
            # closest_blue_rsc = 0.0
            # closest_red_rsc = 0.0

                                # If the rsc is right in the same location as the agent, i.e., dist = 0.0
                    # if self.turtle.distance(right_rscs_detected[i][0]) == 0.:
                    #     closest_blue_rsc = 0.0
                    #     self.rscs_detected[5] = round(closest_blue_rsc, self.precision)
                    #     self.rscs_detected_hist[5].append(self.rscs_detected[5])
                    #     self.rscs_detected[4] = round(closest_blue_rsc - (closest_blue_rsc * ((abs(right_degree_offset) / (self.right_eye*2)))), self.precision)
                    #     self.rscs_detected_hist[4].append(self.rscs_detected[4])
                    #     self.closest_blue_rsc_pos = right_rscs_detected[i][0]

                    
                # elif left_rscs_detected[i][1] == 'blue' and closest_blue_rsc != '':
                #     if int(self.turtle.distance(left_rscs_detected[i][0])) != 0:
                #         next_blue_rsc = (int(self.fov_distance)/int(self.turtle.distance(left_rscs_detected[i][0]))) / self.max_grab_dist
                #         if next_blue_rsc > closest_blue_rsc:
                #             closest_blue_rsc = next_blue_rsc
                #             self.rscs_detected[4] = round(closest_blue_rsc, self.precision)
                #             self.rscs_detected[5] = round(closest_blue_rsc - (closest_blue_rsc * ((abs(left_degree_offset) / (self.left_eye*2)))), self.precision)
                #             self.closest_blue_rsc_pos = left_rscs_detected[i][0]

                                    # At the origin, or more specifically, when the agent's heading is 0 at the origin,
                    # the right eye can only receive input from the offset of the left eye's input
                    # because of the FoV corrections needed for navigating the unit circle.
                    # The right eye is technically looking at 360-330, so it is 'blind' 
                    # to resources at 0, where the left eye is looking 0-30
                    # if self.turtle.distance(right_rscs_detected[i][0]) == 0.:
                    #     closest_red_rsc = 0.0
                    #     self.rscs_detected[1] = round(closest_red_rsc, self.precision)
                    #     self.rscs_detected_hist[1].append(self.rscs_detected[1])
                    #     self.rscs_detected[0] = round(closest_red_rsc - (closest_red_rsc * ((abs(right_degree_offset) / (self.right_eye*2)))), self.precision)
                    #     self.rscs_detected_hist[0].append(self.rscs_detected[0])
                    #     self.closest_red_rsc_pos = right_rscs_detected[i][0]

                                    # if right_rscs_detected[i][1] == 'blue' and closest_blue_rsc == 0.0:
                #     if int(self.turtle.distance(right_rscs_detected[i][0])) != 0:
                #         closest_blue_rsc = (int(self.fov_distance)/int(self.turtle.distance(right_rscs_detected[i][0]))) / self.max_grab_dist
                #         self.rscs_detected[5] = round(closest_blue_rsc, self.precision)
                #         self.rscs_detected[4] = round(closest_blue_rsc - (closest_blue_rsc * ((abs(right_degree_offset) / (self.left_eye*2)))), self.precision)
                #         self.closest_blue_rsc_pos = right_rscs_detected[i][0]

                # elif right_rscs_detected[i][1] == 'blue' and closest_blue_rsc != 0.0:
                #     if int(self.turtle.distance(right_rscs_detected[i][0])) != 0:
                #         next_blue_rsc = (int(self.fov_distance)/int(self.turtle.distance(right_rscs_detected[i][0]))) / self.max_grab_dist
                #         if next_blue_rsc > closest_blue_rsc:
                #             closest_blue_rsc = next_blue_rsc
                #             self.rscs_detected[5] = round(closest_blue_rsc, self.precision)
                #             self.rscs_detected[4] = round(closest_blue_rsc - (closest_blue_rsc * ((abs(right_degree_offset) / (self.left_eye*2)))), self.precision)
                #             self.closest_blue_rsc_pos = right_rscs_detected[i][0]

                # elif right_rscs_detected[i][1] == 'red' and closest_red_rsc == 0.0:
                #     if int(self.turtle.distance(right_rscs_detected[i][0])) != 0:
                #         closest_red_rsc = (int(self.fov_distance)/int(self.turtle.distance(right_rscs_detected[i][0]))) / self.max_grab_dist
                #         self.rscs_detected[1] = round(closest_red_rsc, self.precision)
                #         self.rscs_detected_hist[1].append(self.rscs_detected[1])
                #         self.rscs_detected[0] = round(closest_red_rsc - (closest_red_rsc * ((abs(right_degree_offset) / (self.left_eye*2)))), self.precision)
                #         self.rscs_detected_hist[0].append(self.rscs_detected[0])
                #         self.closest_red_rsc_pos = right_rscs_detected[i][0]
                #         # self.red_right_inputs.append(round(closest_red_rsc, self.precision))
                #         # self.red_left_inputs.append(round(closest_red_rsc - (closest_red_rsc * ((abs(right_degree_offset) / (self.left_eye*2)))), self.precision))

                # elif right_rscs_detected[i][1] == 'red' and closest_red_rsc != 0.0:
                #     if int(self.turtle.distance(right_rscs_detected[i][0])) != 0:
                #         next_red_rsc = (int(self.fov_distance)/int(self.turtle.distance(right_rscs_detected[i][0]))) / self.max_grab_dist
                #         if next_red_rsc > closest_red_rsc:
                #             closest_red_rsc = next_red_rsc
                #             self.rscs_detected[1] = round(closest_red_rsc, self.precision)
                #             self.rscs_detected_hist[1].append(self.rscs_detected[1])
                #             self.rscs_detected[0] = round(closest_red_rsc - (closest_red_rsc * ((abs(right_degree_offset) / (self.left_eye*2)))), self.precision)
                #             self.rscs_detected_hist[0].append(self.rscs_detected[0])
                #             self.closest_red_rsc_pos = right_rscs_detected[i][0]
                            # self.red_right_inputs.append(round(closest_red_rsc, self.precision))
                            # self.red_left_inputs.append(round(closest_red_rsc - (closest_red_rsc * ((abs(right_degree_offset) / (self.left_eye*2)))), self.precision))
        # print("Closest Resources Detected:", self.rscs_detected, "\n")
        # print(self.rscs_detected)

        # Cleaning up Agent.move
                    
            #print("I am turned "+str(self.turtle.heading())+" degrees:")
        # else:
        #     print(bcolors.FAIL + "NaN detected in Agent.move()!" + bcolors.ENDC)