#ROB 417 - Osian Leahy
#This file should include all relevant functions used in processing rotation math and matrices
#Code is ported from R_planar.m, rotation_set_cumulative_product.m, Rx.m, Ry.m, Rz.m, threeD_rotation_set.m,

import numpy as np
import math as m
from copy import deepcopy

#r_planar
#Creates a planar rotation matrix given
def r_planar(theta) -> np.array:
    r = np.array([[m.cos(theta),-m.sin(theta)],[m.sin(theta),m.cos(theta)]])
    return r

#rotation_set_cumulative_product
#Returns the cumulative product of each rotation matrix down the kinematic chain
def rotation_set_cumulative_product(r_set):

    #deepcopy so we don't have to worry about references
    r_set_c = deepcopy(r_set)

    #iterate starting from the second entry, each entry multiplied by the one previous
    for i in range(1,len(r_set)):
        r_set_c[i] = r_set_c[i-1]@r_set_c[i]

    return r_set_c

#r_x
#Returns the 3x3 3D Rotation matrix for a rotation about the X axis
def r_x(psi):
    return np.array([[1,0,0],
                      [0, m.cos(psi), -m.sin(psi)],
                      [0, m.sin(psi), m.cos(psi)]])

#r_y
#Returns the 3x3 3D Rotation matrix for a rotation about the Y axis
def r_y(phi):
    return np.array([[m.cos(phi), 0, m.sin(phi)],
                      [0, 1, 0],
                      [-m.sin(phi), 0, m.cos(phi)]])

#r_z
#Returns the 3x3 3D Rotation matrix for a rotation about the Z axis
def r_z(theta):
    return np.array([[m.cos(theta), -m.sin(theta), 0],
                      [m.sin(theta), m.cos(theta), 0],
                      [0,0,1]])

#three_d_rotation_set
#Takes in two lists, one containing joint angles and the other containing axes of rotation ('x', 'y', or 'z')
#Returns the corresponding list of 3D rotation matrices
def three_d_rotation_set(joint_angles, joint_axes):

    #Can be a shallow copy since we are just creating a list of equal length
    r_set = [None] * len(joint_angles)

    #iterate over the list and generate the relevant rotation matrices
    for i in range(0,len(joint_angles)):
        if joint_axes[i] == 'x':
            r_set[i] = r_x(joint_angles[i])
        elif joint_axes[i] == 'y':
            r_set[i] = r_y(joint_angles[i])
        elif joint_axes[i] == 'z':
            r_set[i] = r_z(joint_angles[i])
        else: raise ValueError('joint_axes has value != x, y, or z')

    return r_set

#three_d_joint_axes_set
#Returns a list of vectors corresponding to the joint axes of rotation
def three_d_joint_axes_set(joint_axes):

    #Can be a shallow copy since we are just creating a list of equal length
    joint_axes_vectors = joint_axes.copy()

    #Adds the corresponding vector to the list
    for i in range(0,len(joint_axes)):
        if joint_axes[i] == 'x':
            joint_axes_vectors[i] = np.array([[1],[0],[0]])
        elif joint_axes[i] == 'y':
            joint_axes_vectors[i] = np.array([[0],[1],[0]])
        elif joint_axes[i] == 'z':
            joint_axes_vectors[i] = np.array([[0],[0],[1]])
        else: raise ValueError('joint_axes has value != x, y, or z')

    return joint_axes_vectors

