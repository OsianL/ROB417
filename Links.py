#ROB 417 - Osian Leahy
#This file should include all relevant functions used in processing sets of links
#Code is ported from build_links.m, place_links.m,
from copy import deepcopy

import numpy as np

#build_links
#Takes a list of link vectors (2x1 or  3x1), and turns it into a list of link start and end points (list of 2x2 matrices)
#this is done in the link local coordinate frame, so the first column is always zeros.
def build_links(link_vectors):

    #Shallow copy since we will overwrite each element in the list later.
    link_set = link_vectors.copy()

    #iterate through and concatenate the
    for i in range(0,len(link_vectors)):
        #Concatentation is in axis 1 for along the x-axis
        link_set[i] = np.concatenate([np.zeros(np.shape(link_vectors[i])),link_vectors[i]],1)

    return link_set

#place_links
#Places arm links in the world coordinate frame given the following:
# links_in_world: n length list containing matrices with link start and end points as the columns (output of build_links)
# link_end_set_with_base: n+1 length list containing vectors pointing to the end location of each link
def place_links(links_in_world, link_end_set_with_base):

    link_set = deepcopy(links_in_world)

    #iterate for each link
    for i in range(1,len(link_set)):
        #elementwise addition of 2x2 and 2x1 matrices. The single column of link_end_set_with_base gets added to both columns of link_set
        #first entry of link_end_set_with_base will be the base of the arm, last entry will be ignored as it is the end of the last link
        link_set[i] = link_set[i] + link_end_set_with_base[i]

    return link_set