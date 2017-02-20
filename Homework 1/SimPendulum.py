from scipy import *
from numpy import sin, cos
import matplotlib.pyplot as plt
import numpy as np
import pygame, sys

'''
Some parameter to initialize the simulation for Simple Pendulum
Simple pendulum follows the simple harmonic motion which is represnted by the folowing equation:

           theta.. = - (g/l) * sin(theta)
'''

ts = .02 		    # Time step size in seconds (delta t)
td = 3 * 60 		# Trial duration in minutes (How long should simulation run?)
te = int(td/ts) 	# No. of timesteps in trial duration (integer)

m = 1 			    # Mass of the bob
g = 9.81 		    # Gravitational acceleration

th = [pi/2]		    # Initial angle in radians
om = [0] 		    # Initial angular velocity i.e first derivative of theta (th)

l = 1               # String length


class SimplePendulum():
    '''
        Class SimplePendulum creates a blueprint of the simple pendulum simulator.

    '''
    # Initializing the properties of the simulator object
    def __init__(self, ts, td, te, m, g, l, th, om):
        self._ts = ts
        self._td = td
        self._te = te
        self._m = m
        self._g = g
        self._l = l
        self._th = th
        self._om = om
    
    
    def run(self):
        '''
        Runs the simulator.
        Calculates the angle (theta) and Angular Velocity (Omega) for each time step using:
    
                               theta = theta + omega * dt 
                               omega = omega - (g/l) * sin(theta) * dt
       
                               Where, 
                                       theta = Angle with rest position
                                       omega = Angular velocity
        '''
        for j in range(self._te):
            self._th.append(self._th[j] + self._om[j] * self._ts)
            self._om.append(self._om[j] - (self._g/self._l) * sin(np.radians(self._th[j+1]))* self._ts)
        self.draw([self._th, self._om])

    # Function to draw the motion of pendulum (plotting angle and angular velocity with respect to Time)
    def draw(self, values):
        plt.figure(1)
        plt.subplot(211)
        plt.plot(values[0], 'r-')
        plt.xlabel('Time')
        plt.ylabel('Angle (theta)')
        plt.subplot(212)
        plt.plot(values[1], 'g-')
        plt.xlabel('Time')
        plt.ylabel('Angular Velocity (omega)')
        plt.subplots_adjust(hspace=0.3)
        plt.show()

# Instantiate the SimplePendulum class to create an instance of Simulator
Simulation = SimplePendulum(ts, td, te, m, g, l, th, om)

if __name__ == '__main__':
    Simulation.run()
