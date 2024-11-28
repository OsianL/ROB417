#ROB 417 - Osian Leahy
#This file is equivalent to ME317_assignment_trace_circle.m

import numpy as np
import math as m

from PathGeneration import circle_x
from ArmJacobian import arm_jacobian
import TrajectoryFollowing as TrajF

#Objective: Make an animated plot showing the robot following a circular path

#Start By defining our robot geometry:
link_vectors = [np.array([[1], [0], [0]]), np.array([[1], [0], [0]]), np.array([[0.75], [0], [0]])]
joint_axes = ['z', 'y', 'y']
link_colors = ['m', 'c', 'y']

#And define the joint starting angles:
alpha_start = [0, m.pi / 4, -m.pi / 2]

#Create an anonymous function for our path
#TODO: Try something other than a boring circle
path_to_follow = lambda t: 0.5*circle_x(t)

#And create a basic timespan array describing the trajectory along that path
start_time = 0
end_time = 1
num_points = 101
t_span = np.linspace(start_time, end_time, num_points)

#Turn the arm endpoint jacobian into an anonymous function
#arm_jacobian returns many additional items by default, we only care about the actual jacobian
jacob = lambda alpha: arm_jacobian(link_vectors, alpha, joint_axes, len(link_vectors) - 1)[0]

#Using the arm jacobian and path, generate a function for the velocity trajectory
#also returns multiple outputs but unsure if we need to restrict it to just one
#If our servos had velocity controllers, we would be able to feed t_span into this directly
joint_velocity = lambda t, alpha: TrajF.follow_trajectory_velocity(t, alpha, jacob, path_to_follow)[0]

#Using the velocity trajectory function and our timespan, we can get a proper position trajectory:
joint_pose_traj = TrajF.generate_joint_pose_trajectory(joint_velocity, t_span, alpha_start)

input('check')
