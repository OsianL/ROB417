#ROB 417 - Osian Leahy
#This file should include
#Code is ported from threeD_robot_arm_links.m
from copy import deepcopy

import numpy as np

import Links
import Rotations as Ro
import VectorSets as Vs

#three_d_robot_arm_links
#Rotates and places link vectors in space prior to graphing. Uses the following inputs:
# link_vectors, a list of np.mat vectors representing each link in it's original reference frame
# joint_angles, a list of angles corresponding to each link's base joint
# joint_axes, a list of axes ('x', 'y', or 'z') about which each link's base joint rotates.
#Returns a list of np.mat (3x2), where each column is the start or endpoint of a link, along with some intermediary variables
def three_d_robot_arm_links(link_vectors,joint_angles,joint_axes):

    #Generate a set of rotation matrices corresponding to the joint angles and axes
    r_joints = Ro.three_d_rotation_set(joint_angles,joint_axes)

    #Get the cumulative multiple of these matrices for each link in the kinematic chain
    r_links = Ro.rotation_set_cumulative_product(r_joints)

    #Generate a local link set (not used except as a function check)
    link_set_local = Links.build_links(link_vectors)

    #Rotate each link endpoint into the world frame
    link_vectors_in_world = Vs.vector_set_rotate(link_vectors,r_links)

    #Generate the start/end matrices for each rotated link (added zero columns to make them atrices
    links_in_world = Links.build_links(link_vectors_in_world)

    #Find the endpoint of each link by adding the previous link's endpoint.
    link_end_set = Vs.vector_set_cumulative_sum(link_vectors_in_world)

    #Add a zero vector representing the base of the arm to the list of link end points
    #Use deepcopy to ensure that modifications don't affect link_end_set
    link_end_set_with_base = [np.zeros(np.shape(link_end_set[1]))] + deepcopy(link_end_set)

    #Place the links in space by adding the endpoint of the previous link to the start/end of the current link.
    link_set = Links.place_links(links_in_world,link_end_set_with_base)

    #Return link_set and all intermediary values
    return link_set, r_joints, r_links, link_set_local, link_vectors_in_world, links_in_world, link_end_set, link_end_set_with_base

