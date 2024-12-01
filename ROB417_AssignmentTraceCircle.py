#ROB 417 - Osian Leahy
#This file is equivalent to ME317_assignment_trace_circle.m

import numpy as np
import math as m
import matplotlib.pyplot as plt

import TrajectoryFollowing as TrajF
import Drawing as Dw
import ThreeDRobotArm as Td
from PathGeneration import circle_x
from ArmJacobian import arm_jacobian


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

#Split this up into the solved times and poses
traj_times = joint_pose_traj[0]
traj_poses = joint_pose_traj[1]

#Create the axes to draw the arm on
axis_limits = [-2,2,-2,2,-2,2]
f,ax = Dw.create_3d_axes(417,axis_limits)

#Get the initial state of the arm and plot it
arm_initial = Td.three_d_robot_arm_links(link_vectors,alpha_start,joint_axes)
l_set_initial = arm_initial[0]
links_drawn = Dw.three_d_draw_links(l_set_initial,link_colors,ax[0])

#Rather than drawing the ideal path, get the endpoint of the arm at each point in time,
#the actual/linearized path, and plot them
endpoint_set = np.zeros(np.shape(traj_poses))

for i in range(0,np.size(endpoint_set,1)):

    #Get the arm link positions at the calculated joint angles
    arm_current = Td.three_d_robot_arm_links(link_vectors,traj_poses[:,i],joint_axes)
    links_current = arm_current[0]

    #Save just the endpoint (column [:,1]) of the last link [2] to the column of endpoint set [:,i]
    endpoint_set[:,i] = links_current[2][:,1]

#And plot the result:
ax[0].plot(endpoint_set[0],endpoint_set[1],endpoint_set[2])

#Turn on interactive mode to prevent matplotlob from blocking exectution
plt.ion()
plt.show()

#Finally animate the arm, saving link set in history
link_set_history = [None] * np.size(traj_poses,1)

#Iterate over the calculated joint angles:
for i in range(0,np.size(traj_poses,1)):

    #First calculate the link set data for a given timestep
    #Kinda redundant to earlier but /shrug
    #Ideally should probably precompute these in the earlier for loop and run it at a defined frame rate or smth?
    arm_current = Td.three_d_robot_arm_links(link_vectors,traj_poses[:,i],joint_axes)
    links_current = arm_current[0]

    #Then update the initial links_drawn objects
    #Doing it this way should be more efficient than redrawing it every time.
    Dw.three_d_update_links(links_drawn,links_current)

    #And finally redraw the graph
    plt.draw()
    #Adjust the pause time to adjust the effective framerate
    plt.pause(0.1)

    #and add the links to history:
    link_set_history[i] = links_current

#Done!