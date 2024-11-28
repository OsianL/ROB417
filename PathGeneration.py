#ROB 417 - Osian Leahy
#This file should include all relevant functions for generating paths to follow/turn into trajectories
#Code ported form circle_x.m,

import numpy as np
import math as m

#circle_x
#Vectored Valued Function for a circular path about the x-axis, starting at (0,1,0) and moving ccw
#Should work for a single t value or list of t
def circle_x(t):
    return np.array([0,m.sin(2*m.pi*t),m.cos(2*m.pi*t)])