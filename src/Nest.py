# Code that generates the nest
import random
import turtle
import tkinter

class Nest:

    def __init__(self):
        # Initializing the nest as an invisible square
        self.nest = turtle.Turtle(shape="square", visible=False)
        self.nest.color("green")
        self.color = self.nest.color()[0]
        # Obtaining canvas width and height
        # self.canvW = turtle.screensize()[0]                          
        # self.canvH = turtle.screensize()[1]
        self.nest.penup()
        # Moving the nest to the lower left quadrant
        self.nest.goto((-300, -225))
        self.nest.pendown()
        self.loc = self.nest.pos()
        # Setting the nest's size (Width, Height, Thickness of border)                                 
        self.nest.shapesize(8, 8, 8)                                
        self.nest.showturtle()
        # Setting arbitrary decay rates for testing
        self.decay_rates = [0.05, 0.10, 0.15, 0.25, 0.5]
        self.decay_rate = random.choice(self.decay_rates)
        # Setting a repair rate (likely to be changed)
        self.repair_rate = self.decay_rate

    # A function to initiate nest decay
    def decay(self):
        # Looping through the list and multiplying each argument in shapesize()
        # by the decay parameter
        decay = tuple([-self.decay_rate + num for num in self.nest.shapesize()])
        self.nest.shapesize(*decay)

    # def repair(self):
    #     # Looping through the list and multiplying each argument in shapesize()
    #     # by the repair parameter
    #     self.nest.shapesize(8, 8, 8)
    #     # repair = tuple([self.repair_rate + num for num in self.nest.shapesize()])
    #     # self.nest.shapesize(*repair)

# Testing integrity of Nest initialization and methods
# nest = Nest()
# nest.nest.getscreen().bgcolor("gray")
# print("Orginal Size:", nest.nest.shapesize())

# nest.decay()
# print("Decayed Size:", nest.nest.shapesize())

# nest.repair()
# print("Repaired Size:", nest.nest.shapesize())

# turtle.done()
