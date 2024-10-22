#ROB 417 - Osian Leahy
#This file should include all relevant functions used in generating the Jacobian for a multi-DOF robot arm

import numpy as np

from ThreeDRobotArm import three_d_robot_arm_endpoints
import VectorSets as Vs
import Rotations as Ro

#arm_jacobian
#Construct the arm jacobian at the end of a particular arm link.
#Requires the desired link number as well as the list of links, joint angles, and joint axes
def arm_jacobian(link_vectors: list, joint_angles: list, joint_axes: list, link_number):

    three_d_arm_output = three_d_robot_arm_endpoints(link_vectors,joint_angles,joint_axes)

    link_ends = three_d_arm_output[0]
    r_links = three_d_arm_output[2]
    link_end_set = three_d_arm_output[4]
    link_end_set_with_base = three_d_arm_output[5]

    #We need to create the 'imaginary' links connecting between each axis of rotation and the desired link end
    #use vector set difference:
    v_diff = Vs.vector_set_difference(link_end_set[link_number],link_end_set_with_base)

    #Create the joint axis vectors, which will be crossed with v_diff to create the jacobian:
    joint_axes_vectors = Ro.three_d_joint_axes_set(joint_axes)

    #Rotate them into the world coordinate frame:
    joint_axes_vectors_rotated = Vs.vector_set_rotate(joint_axes_vectors,r_links)

    #Create an array of zeros to fill the jacobian into:
    #Should have 3 rows (which map to x, y, and z), and n_links columns (which match to alpha_dot, beta_dot, gamma_dot, etc)
    J = np.zeros((3,len(link_vectors)))

    #Original matlab code has a check here for symbolic expressions, forcing the jacobian to be symbolic if
    #v_diff or joint_axis_vectors are symbolic. May need to come back and add this is using sympy in the future...

    #Now just need to fill in the jacobian:
    for i in range(0,link_number+1):
        #The Jacobian is the result of the cross product between each 'imaginary' link and the joint axis (to get the angular to linear velocity conversion vector)
        # axis = 0 tells numpy that our vectors are defined vertically rather than horizontally
        # Have to transpose the result to play nice with np indexing anyways
        # probably not the cleanest method
        J[:,i] = np.cross(joint_axes_vectors_rotated[i],v_diff[i],axis = 0).T

    #Finally return the Jacobian J and all it's intermediary values:
    return J, link_ends, link_end_set, link_end_set_with_base, v_diff, joint_axes_vectors, joint_axes_vectors_rotated, r_links
