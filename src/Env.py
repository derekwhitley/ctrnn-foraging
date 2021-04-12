# Code that generates the environment
import turtle
import time
import tkinter
import random
import Resource
import Agent
import Nest
from operator import attrgetter
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

class Environment:
    def __init__(self, individual_swarm, num_agents = SWARM_SIZE, num_resources=5):
        self.canvW = turtle.screensize()[0]
        self.canvH = turtle.screensize()[1]
        self.num_agents = num_agents
        self.num_resources = num_resources
        # self.canvas = canvas
        self.nest = Nest.Nest()
        self.agents = []
        # Swarm list is ordered by generation
        self.swarms = []
        # Dictionary to track resources and relevant properties
        self.rscs = {}
        # List of tuples of (resource position[i][0] and color[i][1]) to send to agent.detect_fov()
        self.rscs_info = []
        # List to capture agents that achieve perfect orientation
        self.intelligent_agents = []
        # Loop that creates n agents
        for i in range (0, self.num_agents):
            agent = Agent.Agent(individual_swarm, nest=self.nest)
            self.agents.append(agent)
        self.swarms.append(self.agents)
        # Loop that creates n resources
        for i in range (0, self.num_resources):
            rsc = Resource.Resource()
            # Moving the 5 resources (2 patches) to selected locations
            # rsc.rsc.goto(100, 0)
            if i == 0:
                rsc.rsc.goto(-50, 170)
            elif i == 1:
                rsc.rsc.goto(-90, 170)
            elif i == 2:
                rsc.rsc.goto(-50, -20)
            elif i == 3:
                rsc.rsc.goto(-90, -20)
            elif i == 4:
                rsc.rsc.goto(-70, 10)
            # elif i == 5:
            #     rsc.rsc.goto(150, 200)
            # elif i == 6:
            #     rsc.rsc.goto(180, 200)
            # elif i == 7:
            #     rsc.rsc.goto(150, 0)
            # elif i == 8:
            #     rsc.rsc.goto(170, 30)
            # elif i == 9:
            #     rsc.rsc.goto(170, 30)
            
            # Making sure the resources are not too close to each other or to the agent
            # rsc.rsc.penup()
            # if (rsc.rsc.distance(self.nest.nest) < 300):
            #     #print("Distance to Nest Conditions Not Met, Moving")
            #     rsc.rsc.goto(random.choice([(random.choice(range(0, self.canvW)), 
            #     random.choice(range(-self.canvW, self.canvW))), 
            #     (random.choice(range(-self.canvW, self.canvW)), 
            #     random.choice(range(0, self.canvH)))]))
            # for j in self.agents:
            #     while 20 > (rsc.rsc.distance(j.turtle) > 100):
            #         #print("Distance to Agent Conditions Not Met, Moving")
            #         rsc.rsc.goto(random.choice([(random.randrange(-40, 0), random.randrange(-40, 0)), (random.randrange(0, 50), random.randrange(0, 50))]))
            
            rsc.loc = rsc.rsc.pos()
            self.rscs[i] = rsc
            # Creating a list of tuples where index 0 is the resource's x,y location
            # and index 1 is the resource's color
            self.rscs_info.append((rsc.loc, rsc.color))
        # for i in range(len(rscs)):
        #     print("Resource:", i, "\nTurtle tag:", rscs[i], "\nLocation", rscs[i].loc, "\nGraspable:", rscs[i].is_graspable, "\n")

    # Finds the closest rsc to the agent to pass to step function
    def find_closest_rsc(self):
        for agent in self.agents:
            closest_rsc = agent.closest_rsc
            for i in range(len(self.rscs)):
                if agent.turtle.distance(self.rscs[i].loc) < closest_rsc:
                    closest_rsc = agent.turtle.distance(self.rscs[i].loc)
            # print("closest_rscs:", closest_rsc)
            agent.closest_rsc = closest_rsc

    # Identifies the closest resources in the agent's FoV
    # since this is normally handled by the agent
    def grasp_detection(self):
        for agent in self.agents:
            closest_blue_rsc = False
            closest_red_rsc = False
            closest_rsc = False

            if agent.closest_red_rsc_pos:
                closest_red_rsc_dist = agent.turtle.distance(agent.closest_red_rsc_pos)
                # Identify position of rsc based on agent attribute
                # and environment dictionary and record rsc object
                for i in range(len(self.rscs)):
                    if self.rscs[i].loc == agent.closest_red_rsc_pos:
                        closest_red_rsc = self.rscs[i]
            else:
                closest_red_rsc_dist = 101

            if agent.closest_blue_rsc_pos:
                closest_blue_rsc_dist = agent.turtle.distance(agent.closest_blue_rsc_pos)
                # Identify position of rsc based on agent attribute
                # and environment dictionary and record rsc object
                for i in range(len(self.rscs)):
                    if self.rscs[i].loc == agent.closest_blue_rsc_pos:
                        closest_blue_rsc = self.rscs[i]
            else:
                closest_blue_rsc_dist = 101

            # print("Closest Blue:", closest_blue_rsc_dist, "Closest Red", closest_red_rsc_dist)

            if closest_red_rsc and closest_red_rsc_dist < closest_blue_rsc_dist:
                closest_rsc = closest_red_rsc
                # Else assign blue as closest
            elif closest_blue_rsc and closest_blue_rsc_dist < closest_red_rsc_dist:
                closest_rsc = closest_blue_rsc
            else:
                closest_rsc = False
            
            # If agent is carrying rsc, update position
            if agent.is_carrying_rsc and closest_rsc:
                self.move_rsc_with_agent(agent, closest_rsc)
            
            # If agent is not carrying rsc, pick up and move rsc
            if closest_rsc:
                # print("Agent position:", agent.turtle.pos())
                # print("Closest rsc dist:", agent.turtle.distance(closest_rsc.rsc.pos()), "Color:", closest_rsc.color, "\n")

                if agent.turtle.distance(closest_rsc.rsc.pos()) <= 10 and agent.grasping == True and agent.is_carrying_rsc == False:
                    self.move_rsc_with_agent(agent, closest_rsc)
                    agent.is_carrying_rsc = True
                    agent.rsc_being_carried = closest_rsc

    def move_rsc_with_agent(self, agent, closest_rsc):
        # Updates carried resources location w/ agents' locations
        closest_rsc.rsc.setpos(agent.turtle.pos())
        # print("A resource is being carried")

    def step(self):
        # Need to add nest decay somewhere around these parts
        # Decay can be done in several ways:
        # Stochastic decay w/ stochastic decay rates
        # Stochastic decay w/ fixed decay rates
        # Constant, fixed decay, w/ stochastic decay rates
        # Constant, fixed decay, w/ constant decay rate

        # How does the agent become aware of nest decay?
        # i.e., how does the agent learn to fix the nest?
        # Basis of fitness function?

        # maybe rsc decay as well
        for agent in self.agents:
            agent.step(self.rscs_info)
            self.grasp_detection()
        
        self.find_closest_rsc()

        # Need to add nest repair
        # Based on resource transport