# Creating a class for different statistics tracking and plotting
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import configparser
config = configparser.ConfigParser()
config.read("./config.ini")

RUN_DURATION            =       int(config['DEFAULT']['RUN_DURATION'])

class Stats:
    
    def __init__(self):
        self.self = 0

    def heading_and_sens_input_over_time(self, array1, array2, max_runs):
        sns.set_palette(sns.hls_palette(15, l=.6, s=1))
        fig, axs = plt.subplots(2)
        
        # Commands that affect the whole plot
        #fig.subplots_adjust(hspace=0.5)
        fig.suptitle("Test Agent's Red Sensory Inputs over Differential Heading")
        
        # Commands that affect subplot 0
        #axs[0].set_title("Best Agent's Red Sensory Inputs of Generation " +str(ga.current_generation))
        axs[0].get_xaxis().set_visible(False)
        axs[0].set(ylabel="Input Intensity")
        axs[0].legend(labels=['Left Eye', 'Right Eye'], loc='upper right', fontsize=4.75)
        
        # Commands that affect subplot 1
        #axs[1].set_title("Best Agent's Neural Outputs of Generation " +str(ga.current_generation))
        #axs[1].set(xlabel="Time Step", ylabel="Angle Differential")
        
        # Actual plotting commands
        for i in range(len(array1)):
            #j is each tuple in an input list
            for j in array1[i]:
                axs[0].plot((RUN_DURATION*max_runs), j[0])
                axs[0].plot((RUN_DURATION*max_runs), j[1])
        
        # axs[0].plot(np.arange(0, RUN_DURATION*max_runs), array1[:,0])
        # axs[0].plot(np.arange(0, RUN_DURATION*max_runs), array1[:,1])
        #axs[1].plot(np.arange(0, RUN_DURATION), array2)

        plt.show()
            

    def avg_seq_heading_and_sens_input(self, array1, array2, max_runs):
        sns.set_palette(sns.hls_palette(30, l=.5, s=.5))
        fig, axs = plt.subplots(2)
        
        # Commands that affect the whole plot
        #fig.subplots_adjust(hspace=0.5)
        fig.suptitle("Test Agent's Average Red Sensory Inputs over Differential Heading")
        
        # Commands that affect subplot 0
        #axs[0].set_title("Best Agent's Red Sensory Inputs of Generation " +str(ga.current_generation))
        axs[0].get_xaxis().set_visible(False)
        axs[0].set(ylabel="Input Intensity")
        
        # Commands that affect subplot 1
        #axs[1].set_title("Best Agent's Neural Outputs of Generation " +str(ga.current_generation))
        axs[1].set(xlabel="Time Step", ylabel="Angle Differential")
        
        # Actual plotting commands
        # axs[0].plot(np.arange(0, RUN_DURATION*max_runs), array1[:,0])
        # axs[0].plot(np.arange(0, RUN_DURATION*max_runs), array1[:,1])
        axs[0].plot(np.arange(0, RUN_DURATION*max_runs), array1)
        axs[1].plot(np.arange(0, RUN_DURATION*max_runs), array2[:])

        axs[0].legend(labels=['Left Eye', 'Right Eye'], loc='upper right', fontsize=8)
        
        plt.show()

    def avg_ovrlaid_heading_and_sens_input(self, array1, list2, max_runs):
        sns.set_palette(sns.hls_palette(100, l=.5, s=.5))
        fig, axs = plt.subplots(2)
        
        # Commands that affect the whole plot
        #fig.subplots_adjust(hspace=0.5)
        fig.suptitle("Test Agent's Average Red Sensory Inputs over Differential Heading")
        
        # Commands that affect subplot 0
        #axs[0].set_title("Best Agent's Red Sensory Inputs of Generation " +str(ga.current_generation))
        # axs[0].get_xaxis().set_visible(False)
        # axs[0].set(ylabel="Input Intensity")
        
        # Commands that affect subplot 1
        #axs[1].set_title("Best Agent's Neural Outputs of Generation " +str(ga.current_generation))
        axs[1].set(xlabel="Time Step", ylabel="Angle Differential")
        
        # Actual plotting commands

        axs[0].plot(np.arange(0, RUN_DURATION*max_runs), array1[:,0])
        axs[0].plot(np.arange(0, RUN_DURATION*max_runs), array1[:,1])
        axs[0].legend(labels=['Left Eye', 'Right Eye'], loc='upper right', fontsize=8)
        
        for i in range(0, max_runs):
            #print("List elements within lists", list2[i])
            #print(RUN_DURATION)
            axs[1].plot(range(0, RUN_DURATION), list2[i])
            plt.show()
        