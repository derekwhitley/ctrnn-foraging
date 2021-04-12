# Generates the code for the turtle body
# Need to create sensors and effectors

# Code that generates the environment
import turtle
import random
import Nest
import math
import Brain
import configparser
import random
config = configparser.ConfigParser()
config.read("./config.ini")

RUN_DURATION              =       int(config['DEFAULT']['RUN_DURATION'])

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

class Agent:    
    def __init__(self, individual_swarm, nest, run_duration=RUN_DURATION):
        # Creates a turtle to serve as the main agent(s)
        self.turtle = turtle.Turtle(shape="turtle", visible=False)
        self.turtle.penup()
        self.turtle.hideturtle()
        self.turtle.goto(0, 75)
        #self.turtle.setheading(random.choice([random.randrange(0, 30), random.randrange(330, 360)]))
        #self.turtle.setheading(random.randrange(165, 195))
        self.turtle.setheading(180)
        self.turtle.showturtle()
        self.turtle.pendown()
        # Calls the agent's location
        self.loc = self.turtle.pos()
        # Sets a maximum distance for the turtle's FoV
        self.fov_distance = 100.0
        # Left eye for FoV; value affects heading
        # Cannot hardcode with setheading() bc 
        # it doesn't update properly
        self.left_eye = 30.0
        # Right eye for FoV; value affects heading
        self.right_eye = -30.0
        # An attribute to track if the turtle is "grasping" a resource
        self.grasping = False
        # Agent's energy; will vary during conditions
        self.energy = 100
        # Agent's lifespan; may vary during conditions
        self.life_span = 1000
        # List to track detected resources; 0.0001 is the default value
        # since 0's can be problematic for the network and for turtle
        self.rscs_detected = [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001]
        # List of times resources detected
        self.rscs_detected_hist = [[],[],[],[],[],[]]
        # Sets the maximum distance at which agent can grab rsc
        self.max_grab_dist = 10.
        # Sets the precision value for calculation rounding
        self.precision = 5
        # Creates a brain for the agent
        self.brain = Brain.Brain(individual_swarm)
        # Sets maximum forward travel distance
        self.max_forward_travel = 5.0
        # Sets maximum turning radius for agent
        self.max_turning_radius = 5.0
        # Tracks which rscs are closest
        self.closest_red_rsc_pos = False
        self.closest_blue_rsc_pos = False
        # Checks if a rsc is being carried
        self.is_carrying_rsc = False
        # Tracks which rsc is currently being carried by agent
        self.rsc_being_carried = 0.0
        # Attaches nest object to agent
        self.nest = nest
        # Tracks the closest rsc as given by the environment
        self.closest_rsc = 2000.0
        #self.count = 0
        # self.turtle.setheading(random.randint(0,360))

    # A function to detect objects within the turtle's FoV
    # and store them within rscs_detected
    # Detects a color gradient along three dimensions (r, g, b) w/ two eyes (L, R)
    def detect_fov(self, rscs_info):
        left_rscs_detected = []
        right_rscs_detected = []

        # Nest graded value
        # if int(self.turtle.distance(self.nest.loc)) > 0.0:
        if self.turtle.distance(self.nest.loc) and self.max_grab_dist:
            nest_dist = (self.fov_distance/self.turtle.distance(self.nest.loc)) / self.max_grab_dist
        else:
            print("nest.loc:",self.nest.loc,"max_grab_dist:",self.max_grab_dist)
        #     nest_dist = 0.0001

        # Nest degree offset
        nest_degree_offset = abs(self.turtle.towards(self.nest.loc) - self.turtle.heading())
        if nest_degree_offset > 60.0:
            nest_degree_offset -= 360.00

        # Checks if nest is within left eye's FoV
        if self.turtle.heading() <= self.turtle.towards(self.nest.loc) <= self.turtle.heading()+self.left_eye and self.turtle.distance(self.nest.loc) <= self.fov_distance:
            # print("Nest detected at:", self.turtle.towards(nest.loc), "\nColor:", nest.color, "\nDistance away:", self.turtle.distance(rscs_info[i][0]))
            self.rscs_detected[2] = round(nest_dist, self.precision)
            self.rscs_detected[3] = round(nest_dist - (nest_dist * ((abs(nest_degree_offset) / (self.left_eye*2)))), self.precision)
        # Checks if nest is within right eye's FoV
        elif self.turtle.heading()+self.right_eye <= self.turtle.towards(self.nest.loc) <= self.turtle.heading() and self.turtle.distance(self.nest.loc) <= self.fov_distance:
            self.rscs_detected[3] = round(nest_dist, self.precision)
            self.rscs_detected[2] = round(nest_dist - (nest_dist * ((abs(nest_degree_offset) / (self.left_eye*2)))), self.precision)
        else:
            self.rscs_detected[2] = 0.0001
            self.rscs_detected[3] = 0.0001

        # Looping through the locations and colors of the rscs
        # provided by the environment as a list to check if they
        # are within the left or right FoV
        for i in range(0, len(rscs_info)):
            #print("Checking resource number:", i, "\nRelative heading:", self.turtle.towards(rscs_info[i][0]), "\nColor:", rscs_info[i][1], "\n")
            corrected_left_fov = self.turtle.heading() + self.left_eye # 105
            corrected_right_fov = self.turtle.heading() + self.right_eye # -15 = 345

            # Checks if rsc is within regular left eye's FoV
            if self.turtle.heading() <= self.turtle.towards(rscs_info[i][0]) <= self.turtle.heading()+self.left_eye and self.turtle.distance(rscs_info[i][0]) <= self.fov_distance:
                left_rscs_detected.append((rscs_info[i][0], rscs_info[i][1]))
            # Checks if rsc is within regular right eye's FoV
            elif self.turtle.heading()+self.right_eye <= self.turtle.towards(rscs_info[i][0]) <= self.turtle.heading() and self.turtle.distance(rscs_info[i][0]) <= self.fov_distance:
                right_rscs_detected.append((rscs_info[i][0], rscs_info[i][1]))         
            elif corrected_right_fov < 0.0:    
                corrected_right_fov += 360.00

                if corrected_right_fov <= self.turtle.towards(rscs_info[i][0]) <= 360.00 or 0.0 <= self.turtle.towards(rscs_info[i][0]) <= self.turtle.heading():
                    if self.turtle.distance(rscs_info[i][0]) <= self.fov_distance:
                        right_rscs_detected.append((rscs_info[i][0], rscs_info[i][1]))
                    else:
                        # print("Resource " + str(i) + " Outside FoV\n", "Resource at:", self.turtle.towards(rscs_info[i][0]), "\nDistance away:", self.turtle.distance(rscs_info[i][0]), "\n")
                        self.rscs_detected[0] = 0.0001
                        self.rscs_detected[1] = 0.0001
                        self.rscs_detected[4] = 0.0001
                        self.rscs_detected[5] = 0.0001
                else:
                        self.rscs_detected[0] = 0.0001
                        self.rscs_detected[1] = 0.0001
                        self.rscs_detected[4] = 0.0001
                        self.rscs_detected[5] = 0.0001

            elif corrected_left_fov > 360.00:
                corrected_left_fov -= 360.00

                if self.turtle.heading() <= self.turtle.towards(rscs_info[i][0]) <= 360.00 or 0.0 <= self.turtle.towards(rscs_info[i][0]) <= corrected_left_fov:
                    if self.turtle.distance(rscs_info[i][0]) <= self.fov_distance:
                        left_rscs_detected.append((rscs_info[i][0], rscs_info[i][1]))
                    else:        
                        self.rscs_detected[0] = 0.0001
                        self.rscs_detected[1] = 0.0001
                        self.rscs_detected[4] = 0.0001
                        self.rscs_detected[5] = 0.0001
                else:
                        self.rscs_detected[0] = 0.0001
                        self.rscs_detected[1] = 0.0001
                        self.rscs_detected[4] = 0.0001
                        self.rscs_detected[5] = 0.0001
            
            else:        
                self.rscs_detected[0] = 0.0001
                self.rscs_detected[1] = 0.0001
                self.rscs_detected[4] = 0.0001
                self.rscs_detected[5] = 0.0001

        # Series of conditionals to determine which rsc is closest
        # to agent and closer to which eye via sensory signal
        if len(left_rscs_detected) >= 1:
            closest_blue_rsc = ''
            closest_red_rsc = ''

            for i in range(0, len(left_rscs_detected)):
                # [i][0] = loc
                # [i][1] = color

                left_degree_offset = abs(self.turtle.towards(left_rscs_detected[i][0]) - self.turtle.heading())
                if left_degree_offset > 60.0:
                    left_degree_offset -= 360.00
                
                # Calculates a linearized value for rsc distance
                # as a function of the max FoV distance divided by the actual
                # distance of the rsc, and scaled down 1 OoM by max grab dist
                # Max adjusted dist = 10.0
                # Min adjusted dist = 0.10

                if left_rscs_detected[i][1] == 'blue' and closest_blue_rsc == '':
                    # If the rsc is right in the same location as the agent, i.e., dist = 0.0
                    # we want this value to be the highest, e.g., 10
                        
                    # Condition for if dist to rsc 0.0 <= 1.0
                    # Making these equivalent because 0 and 1 in turtle
                    # are extremely close together
                    if 0. <= self.turtle.distance(left_rscs_detected[i][0]) <= 1.:
                    # Adjusting the value here based on how the math would work out;
                    # if the dist is 0, i.e., the agent and rsc occupy the same space
                    # or if the dist is 1, the agent gets the highest signal possible, viz., 10
                    # Adjusted (self.fov_distance/1) to just self.fov_distance
                    # since the math is the same and can remove superfluous computations
                        closest_blue_rsc = (self.fov_distance / self.max_grab_dist)
                        self.rscs_detected[4] = round(closest_blue_rsc, self.precision)
                        self.rscs_detected_hist[4].append(self.rscs_detected[4])
                        self.rscs_detected[5] = round(closest_blue_rsc - (closest_blue_rsc * ((abs(left_degree_offset) / (self.left_eye*2)))), self.precision)
                        self.rscs_detected_hist[5].append(self.rscs_detected[5])
                        self.closest_blue_rsc_pos = left_rscs_detected[i][0]
                    
                    # If the value is between 1 and 100, the math works out cleaner
                    # Highest possible signal here is closest to max
                    # Lowest possible signal is ~.1
                    elif 1. < self.turtle.distance(left_rscs_detected[i][0]) <= self.fov_distance:
                        closest_blue_rsc = (self.fov_distance/self.turtle.distance(left_rscs_detected[i][0])) / self.max_grab_dist
                        self.rscs_detected[4] = round(closest_blue_rsc, self.precision)
                        self.rscs_detected_hist[4].append(self.rscs_detected[4])
                        self.rscs_detected[5] = round(closest_blue_rsc - (closest_blue_rsc * ((abs(left_degree_offset) / (self.left_eye*2)))), self.precision)
                        self.rscs_detected_hist[5].append(self.rscs_detected[5])
                        self.closest_blue_rsc_pos = left_rscs_detected[i][0]

                elif left_rscs_detected[i][1] == 'red' and closest_red_rsc == '':                   
                    if 0. <= self.turtle.distance(left_rscs_detected[i][0]) <= 1.:
                        closest_red_rsc = (self.fov_distance / self.max_grab_dist)
                        self.rscs_detected[0] = round(closest_red_rsc, self.precision)
                        self.rscs_detected_hist[0].append(self.rscs_detected[0])
                        self.rscs_detected[1] = round(closest_red_rsc - (closest_red_rsc * ((abs(left_degree_offset) / (self.left_eye*2)))), self.precision)
                        self.rscs_detected_hist[1].append(self.rscs_detected[1])
                        self.closest_red_rsc_pos = left_rscs_detected[i][0]

                    elif 1. < self.turtle.distance(left_rscs_detected[i][0]) <= self.fov_distance:
                        #print("Check 2")
                        closest_red_rsc = (self.fov_distance/self.turtle.distance(left_rscs_detected[i][0])) / self.max_grab_dist
                        #print(closest_red_rsc)
                        self.rscs_detected[0] = round(closest_red_rsc, self.precision)
                        self.rscs_detected_hist[0].append(self.rscs_detected[0])
                        self.rscs_detected[1] = round(closest_red_rsc - (closest_red_rsc * ((abs(left_degree_offset) / (self.left_eye*2)))), self.precision)
                        self.rscs_detected_hist[1].append(self.rscs_detected[1])
                        self.closest_red_rsc_pos = left_rscs_detected[i][0]
        
        # Same code as above but for right eye
        if len(right_rscs_detected) >= 1:
            closest_blue_rsc = ''
            closest_red_rsc = ''
            
            for i in range(0, len(right_rscs_detected)):
                # [i][0] = loc
                # [i][1] = color

                right_degree_offset = abs(self.turtle.towards(right_rscs_detected[i][0]) - self.turtle.heading())
                if right_degree_offset > 60.0:
                    right_degree_offset -= 360.00
                
                if right_rscs_detected[i][1] == 'blue' and closest_blue_rsc == '':

                    if 0. <= self.turtle.distance(right_rscs_detected[i][0]) <= 1.:
                        closest_blue_rsc = (self.fov_distance / self.max_grab_dist)
                        self.rscs_detected[5] = round(closest_blue_rsc, self.precision)
                        self.rscs_detected_hist[5].append(self.rscs_detected[5])
                        self.rscs_detected[4] = round(closest_blue_rsc - (closest_blue_rsc * ((abs(right_degree_offset) / (self.right_eye*2)))), self.precision)
                        self.rscs_detected_hist[4].append(self.rscs_detected[4])
                        self.closest_blue_rsc_pos = right_rscs_detected[i][0]
                    
                    elif 1. < self.turtle.distance(right_rscs_detected[i][0]) <= self.fov_distance:
                        closest_blue_rsc = (self.fov_distance/self.turtle.distance(right_rscs_detected[i][0])) / self.max_grab_dist
                        self.rscs_detected[5] = round(closest_blue_rsc, self.precision)
                        self.rscs_detected_hist[5].append(self.rscs_detected[5])
                        self.rscs_detected[4] = round(closest_blue_rsc - (closest_blue_rsc * ((abs(right_degree_offset) / (self.right_eye*2)))), self.precision)
                        self.rscs_detected_hist[4].append(self.rscs_detected[4])
                        self.closest_blue_rsc_pos = right_rscs_detected[i][0]

                elif right_rscs_detected[i][1] == 'red' and closest_red_rsc == '':
                    
                    if 0. <= self.turtle.distance(right_rscs_detected[i][0]) <= 1.:
                        closest_red_rsc = (self.fov_distance/ self.max_grab_dist)
                        self.rscs_detected[1] = round(closest_red_rsc, self.precision)
                        self.rscs_detected_hist[1].append(self.rscs_detected[1])
                        self.rscs_detected[0] = round(closest_red_rsc - (closest_red_rsc * ((abs(right_degree_offset) / (self.right_eye*2)))), self.precision)
                        self.rscs_detected_hist[0].append(self.rscs_detected[0])
                        self.closest_red_rsc_pos = right_rscs_detected[i][0]

                    elif 1. < self.turtle.distance(right_rscs_detected[i][0]) <= self.fov_distance:
                        closest_red_rsc = (self.fov_distance/self.turtle.distance(right_rscs_detected[i][0])) / self.max_grab_dist
                        self.rscs_detected[1] = round(closest_red_rsc, self.precision)
                        self.rscs_detected_hist[1].append(self.rscs_detected[1])
                        self.rscs_detected[0] = round(closest_red_rsc - (closest_red_rsc * ((abs(right_degree_offset) / (self.right_eye*2)))), self.precision)
                        self.rscs_detected_hist[0].append(self.rscs_detected[0])
                        self.closest_red_rsc_pos = right_rscs_detected[i][0]
                
        return self.rscs_detected

    # Calls the outputs of the brain
    # self.brain.current_outputs[-4] # forward neuron
    # self.brain.current_outputs[-3] # left motor neuron
    # self.brain.current_outputs[-2] # right motor neuron
    # self.brain.current_outputs[-1] # grasping neuron

    # A function to move the agent based on neuronal input
    def move(self):
        # Moves the turtle forward based on output from forward motor neuron

        # if self.max_turning_radius > self.brain.current_outputs[-3] or self.brain.current_outputs[-2]:
        #     self.turtle.left(self.max_turning_radius)
        if self.brain.current_outputs[-3] > self.brain.current_outputs[-2]:
            #self.turtle.left((self.max_turning_radius*self.brain.current_outputs[-3]) - (self.max_turning_radius*self.brain.current_outputs[-2]))
            #self.turtle.left(self.brain.current_outputs[-3] - self.brain.current_outputs[-2])
            self.turtle.left(self.brain.current_outputs[-3])
            #self.turtle.forward(self.brain.current_outputs[-4])
        elif self.brain.current_outputs[-2] > self.brain.current_outputs[-3]:
            #self.turtle.right((self.max_turning_radius*self.brain.current_outputs[-2]) - (self.max_turning_radius*self.brain.current_outputs[-3]))
            #self.turtle.right(self.brain.current_outputs[-2] - self.brain.current_outputs[-3])
            self.turtle.right(self.brain.current_outputs[-2])
            #self.turtle.forward(self.brain.current_outputs[-4])

    # A function to track grabbing based on neuronal input
    # Reach is ~10 pixels
    def grab(self):
        if self.brain.current_outputs[-1] >= 0.5:
            self.grasping = True
        else:
            self.grasping = False
    
    def step(self, rscs_info):
        # Produce sensory inputs for network
        self.detect_fov(rscs_info)
        # Feed sensory inputs into network
        self.brain.step(rscs_detected=self.rscs_detected)
        # Implement motor inputs from network
        self.move()
        # Check if rsc is graspable and grasp if activation >= 0.5
        #self.grab()
