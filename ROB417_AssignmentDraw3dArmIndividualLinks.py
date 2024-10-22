#ROB 417 - Osian Leahy
#This file is equivalent to ME317_Assignment_draw_3D_arm_individual_links.m

from math import pi
import numpy as np
import matplotlib.pyplot as plt

import Links
import Rotations as Ro
import Drawing as Dw
import VectorSets as Vs
from ThreeDRobotArm import three_d_robot_arm_links

#Objective: Draw a 3 Axis arm in 3D given the link_vectors, joint angles, and joint axes of rotation

#Set up our inputs:
#link vectors in their local coordinate frames
link_vectors = [np.array([[4],[0],[0]]),np.array([[4],[0],[0]]),np.array([[0],[0],[2]])]
#static joint angles
joint_angles = [2*pi/5,-pi/4,pi/4]
#corresponding joint axes of rotation
joint_axes = ['z','y','x']
#color to draw each link in
link_colors = ['r','b','g']

#First, get the rotated, placed links and corresponding rotation matrices.
three_d_arm_output = three_d_robot_arm_links(link_vectors,joint_angles,joint_axes)

#unpack the outputs we care about from the tuple
link_set = three_d_arm_output[0]
r_links = three_d_arm_output[2]
link_end_set_with_base = three_d_arm_output[7]

#Create a list of vectors to represent the axis of rotation
joint_axes_vectors = Ro.three_d_joint_axes_set(joint_axes)

#Rotate them into the world coordinate frame:
joint_axes_vectors_rotated = Vs.vector_set_rotate(joint_axes_vectors,r_links)

#Augment them with start points:
joint_axes_set_rotated = Links.build_links(joint_axes_vectors_rotated)

#place them in the world coordinate frame:
joint_axes_set = Links.place_links(joint_axes_set_rotated,link_end_set_with_base)

#Create a Figure and 3D Axes to draw our arm on:
limits = [-2,8,-2,8,-2,8]
f,ax = Dw.create_3d_axes(417,limits)

#plot each link:
l = Dw.three_d_draw_links(link_set,link_colors,ax[0],linestyle = '-')

#plot the joint axis
l2 = Dw.three_d_draw_links(joint_axes_set,link_colors,ax[0],linestyle = '--')

#actually show the graph
plt.show()
