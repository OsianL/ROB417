#ROB 417 - Osian Leahy
#This file is equivalent to ME317_draw_3d_arm_with_jacobian.m

from math import pi
import numpy as np
import matplotlib.pyplot as plt

import Drawing as Dw
from ArmJacobian import arm_jacobian


#Objective: Draw a 3 Axis arm in 3D given the link_vectors, joint angles, and joint axes of rotation

#Set up our inputs:
#link vectors in their local coordinate frames
link_vectors = [np.array([[1],[0],[0]]),np.array([[1],[0],[0]]),np.array([[0],[0],[.5]])]
#static joint angles
joint_angles = [2*pi/5,-pi/4,pi/4]
#corresponding joint axes of rotation
joint_axes = ['z','y','x']
#colors to draw the jacobian arrows in:
q_colors = ['c','m','y']

#Create an empty list to hold the jacobian for each link end:
J = [''] * len(link_vectors)

#Generate the jacobian for each entry in the jacobian list
for i in range(0,len(J)):
    #use arm_jacobian()
    arm_jacobian_output = arm_jacobian(link_vectors,joint_angles,joint_axes,i)

    #Unpack the outputs
    #We need to store all iterations of this
    J[i] = arm_jacobian_output[0]
    #these are the same for each loop
    link_ends = arm_jacobian_output[1]
    link_end_set = arm_jacobian_output[2]
    joint_axes_vectors_rotated = arm_jacobian_output[6]

#now we need to draw 3 versions of the arm with each containing:
# - A visual representation of the arm
# - joint axes vectors
# - The 'imaginary' links pointing to the jacobian link endpoint
# - Tangent vectors showing the linear velocity direction

#Create a Figure and 3D Axes to draw our arm on:
limits = [-.5,3,-.5,3,-.5,3]
f,ax = Dw.create_3d_axes(417,limits,2,2,3)

#Create some empty lists of the correct length to hold the handles of each arm's links, jacobian psuedo-links, and joint axes:
l1 = [''] * len(J)
l2 = [''] * len(J)
l3 = [''] * len(J)
#And also to hold the arrows plotted on each axis:
q = [''] * len(J)

#Loop over each of the subaxes and plot the arm links
for i in range(0,len(l1)):
    l1[i] = ax[i].plot(link_ends[0,:],link_ends[1,:],link_ends[2,:], marker = 'o')

#Loop over each of the subaxes and plot the jacobian lines
for i in range(0, len(ax)):

    q[i] = Dw.draw_vectors_at_point(link_end_set[i],J[i],ax[i],q_colors)

#Loop over each of the subaxes and:
# - Create lists within l2,l3
# - Draw dashed lines up to the jacobian endpoint in this graph
# - Draw joint axes up to the last relevant joint for this jacobian

for i in range(0, len(ax)):

    #create empty lists to fill
    l2[i] = [''] * np.size(J,1)
    l3[i] = [''] * np.size(J, 1)

    for j in range(0,i+1):
        #Draw the jacobian pseudo-link lines
        #Drawing from the current starting link (j) to the current jacobian point (i+1)
        x_data = [link_ends[0][j],link_ends[0][i+1]]
        y_data = [link_ends[1][j],link_ends[1][i+1]]
        z_data = [link_ends[2][j],link_ends[2][i+1]]

        #get and use the color from the corresponding quiver object:
        q_color = q[i][j].get_color()

        #plot the lines
        l2[i][j] = ax[i].plot(x_data,y_data,z_data, color = q_color, linestyle = ':')

    for j in range(0,i+1):
        #Draw the joint axes lines

        #first place the rotated joint axis vector in the world:
        joint_axis_vector_in_world = np.concatenate([link_ends[:,j:j+1],link_ends[:,j:j+1] + joint_axes_vectors_rotated[j]], axis = 1)

        #get the color:
        q_color = q[i][j].get_color()

        #plot the lines:
        l3[i][j] = ax[i].plot(joint_axis_vector_in_world[0],joint_axis_vector_in_world[1],joint_axis_vector_in_world[2], color = q_color, linestyle = '--')

#Actually Show the plots
plt.show()
