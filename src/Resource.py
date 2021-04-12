# Code that generates the resources
import turtle
import tkinter
import random

class Resource:

    def __init__(self, energy=100):
        # Initializing the resources as invisible squares
        # shapes are 21x21 (WxL) by default
        self.rsc = turtle.Turtle(shape="square", visible=False)
        # Resources can be red or blue; color will represent value
        #self.colors = ["red", "blue"]
        self.colors = ["red"]
        # Obtaining canvas width and height
        self.canvW = turtle.screensize()[0]
        self.canvH = turtle.screensize()[1]
        # Creating a list to track resource information
        self.resources_list = []
        self.rsc.getscreen().bgcolor("gray")
        self.rsc.color(random.choice(self.colors))
        self.color = self.rsc.color()[0]
        self.rsc.penup()
        # Moving the resources to random locations on the canvas
        #self.rsc.goto(random.randrange(0, 200), random.randrange(-200, 200))
        #self.rsc.goto(random.choice([(random.randrange(-200, 0), random.randrange(-200, 0)), (random.randrange(0, 200), random.randrange(0, 200))]))

        # Setting heading and forward movement so the resource spawns
        # randomly in a circle around the agent
        # self.rsc.setheading(random.randrange(0, 270))
        # #self.rsc.setheading(random.choice([random.randrange(0, 130), random.randrange(150, 270)]))
        # self.rsc.forward(random.randrange(100, 200))

        # self.rsc.goto(random.choice([(random.choice(range(0, self.canvW)), 
        #                 random.choice(range(-self.canvW, self.canvW))), 
        #                 (random.choice(range(-self.canvW, self.canvW)), 
        #                 random.choice(range(0, self.canvH)))]))
        
        self.loc = self.rsc.pos()
        self.rsc.showturtle()
        # Energy (value) of the the rsc
        self.energy = energy
        # Graspability of rsc by agent
        self.is_graspable = True