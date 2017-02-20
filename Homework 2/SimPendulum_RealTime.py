from scipy import *
from numpy import sin, cos
import matplotlib.pyplot as plt
import numpy as np

'''
Some parameter to initialize the simulation for Simple Pendulum
Simple pendulum follows the simple harmonic motion which is represnted by the folowing equation:

           theta.. = - (g/l) * sin(theta)
'''
ts = .02 		    # Time step size in seconds (delta t)
td = 3 * 60 		# Trial duration in minutes (How long should simulation run?)
te = int(td/ts) 	# No. of timesteps in trial duration (integer)

mu = 0.1 		    # Friction factor
m = 1 			    # Mass of the bob
g = 9.81 		    # Gravitational acceleration


th = [pi/4]		    # Initial angle in radians
om = [0] 		    # Initial angular velocity i.e first derivative of theta (th)



l = 1               # String length

class RealTime():

    def __init__(self, ts, td, te, mu, m, g, l, th, om):
        self._ts = ts
        self._td = td
        self._te = te
        self._mu = mu
        self._m = m
        self._g = g
        self._l = l
        self._th = th
        self._om = om

    # Fourth order Runge Kutta (RK4) to differentiate the simple pendulum equation motion
    def run(self):
    
        for j in range(self._te):
            # Euler approximation
            self._th.append(self._th[j] + self._ts * self._om[j])
            f1 = (-self._mu * self._om[j] + self._m * self._g * self._l * sin(np.radians(self._th[j])))/(self._m * (self._l^2))
            self._om.append(self._om[j] + self._ts * f1)
            
            # Approximation 1 at mid-interval
            th2 = self._th[j+1] + (self._ts/2) * self._om[j+1]
            f2 = (-self._mu * self._om[j+1] + self._m * self._g * self._l * sin(np.radians(self._th[j+1])))/(self._m * (self._l^2))
            om2 = self._om[j+1] + (self._ts/2) * f2
            
            # Approximation 2 at mid-interval
            th3 = th2 + (self._ts/2) * om2
            f3 = (-self._mu * om2 + self._m * self._g * self._l * sin(th2))/(self._m * (self._l^2))
            om3 = om2 + (self._ts/2) * f3
            
            # Approximation at next time step
            th4 = th3 + (self._ts) * om3
            f4 = (-self._mu * om3 + self._m * self._g * self._l * sin(th3))/(self._m * (self._l^2))
            om4 = om3 + (self._ts) * f4
            
            dth = (self._om[j] + 2 * self._om[j+1] + 2 * om2 + om3)/6
            dom = (f1 + 2 * f2 + 2 * f3 + f4)/6
            self._th[j+1] = self._th[j] + self._ts * dth
            self._om[j+1] = self._om[j] + self._ts * dom
        
        self.draw([self._th, self._om])

    # Function to animate the motion of pendulum (visualization)
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

# Instantiate the simGen class to create an instance of simulation
RealTime = RealTime(ts, td, te, mu, m, g, l, th, om)


if __name__ == '__main__':
    RealTime.run()
