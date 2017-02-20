from scipy import *
from numpy import sin, cos
import matplotlib.pyplot as plt
import numpy as np

'''
Some parameter to initialize the simulation for Simple Pendulum
Simple pendulum follows the simple harmonic motion which is represnted by the folowing equation:

           theta.. = - (g/l) * sin(theta)
'''
ts = .02 		        # Time step size in seconds (delta t)
td = 2 * 60 		    # Trial duration in minutes (How long should simulation run?)
te = int(td/ts) 	    # No. of timesteps in trial duration (integer)

m = 1 			        # Mass of the bob
g = 9.81 		        # Gravitational acceleration

sample_size = 1000      # Sample size of the distribution

# Class simGen creates an object of the pendulum simulator
class MonteCarlo():

    # Initializing the properties of the simulator object
    def __init__(self, ts, td, te, m, g, sample_size):
        self._ts = ts
        self._td = td
        self._te = te
        self._m = m
        self._g = g
        self._size = sample_size
        self.thetas = []
        self.omegas = []
        self.length = []
        self.period = []
    '''
    Calculates the angle (theta) and Angular Velocity (Omega) for each time step using:
    
                               theta = theta + omega * dt 
                               omega = omega - (g/l) * sin(theta) * dt
       
                               Where, 
                                       theta = Angle with rest position
                                       omega = Angular velocity
    '''
    def TimePeriod(self, l, th, om):
        theta = th
        omega = -1 * om
        period = 0
        for j in range(self._te):
            theta = theta + omega * self._ts
            omega = omega - (g/l) * (np.sin(np.radians(theta)) * self._ts)
            period = period + self._ts

            if theta >= th:
                print('Length: ' + str(l) + ' Initial Angle: ' + str(th) + ' Initial Velocity: ' + str(om) + ' Period: ' + str(period))
                break
        return period
        
    def run(self):
        '''
            Run function generates a uniform disribution for length, theta and Omegae between the given ranges.
            For each set of random vaues it calls the method TimePeriod() which return the TimePeriod for that run. 

            After all the runs, it calls draw() to draw all the randomly generated values against calculated time period. 
        '''
        for i in range(self._size):
            rand_l = float(np.random.uniform(9.5, 10.5))
            rand_th = float(np.random.uniform(55, 65))
            rand_om = float(np.random.uniform(0.25, 0.35))
            
            period = self.TimePeriod(rand_l, rand_th, rand_om)
            self.length.append(rand_l)
            self.thetas.append(rand_th)
            self.omegas.append(rand_om)
            self.period.append(period)

        self.draw([self.length, self.thetas, self.omegas, self.period])

    # Function to draw the motion of pendulum (plotting angle and angular velocity)
    def draw(self, values):
        plt.figure(1)
        plt.subplot(311)
        plt.scatter(values[0], values[3])
        plt.xlabel('Length')
        plt.ylabel('Period (T)')

        plt.subplot(312)
        plt.scatter(values[1], values[3])
        plt.xlabel('Angle (theta)')
        plt.ylabel('Period (T)')

        plt.subplot(313)
        plt.scatter(values[2], values[3])
        plt.xlabel('Angular Velocity (omega)')
        plt.ylabel('Period (T)')

        plt.subplots_adjust(hspace=0.5)
        plt.show()


# Instantiate the simGen class to create an instance of simulation
MonteCarlo = MonteCarlo(ts, td, te, m, g, sample_size)

if __name__ == '__main__':
    MonteCarlo.run()