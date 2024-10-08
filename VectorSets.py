#ROB 417 - Osian Leahy
#This file should include all relevant functions used in processing sets of vectors.
#Code is ported from vector_set_rotate.m, vector_set_cumulative_sum.m, vector_set_extend.m, vector_set_difference.m
from copy import deepcopy
import numpy as np

#vector_set_rotate
#Rotates a list of vectors using a corresponding list of rotation matrices
def vector_set_rotate(v_set: list, r_set: list):

    #Can be a shallow copy since we will replace all entries.
    v_set_r = v_set.copy()

    #Stores the product of each rotation matrix and vector in a list
    for i in range(0,len(v_set_r)):
        v_set_r[i] = np.dot(r_set[i],v_set[i])

    return v_set_r

#vector_set_cumulative_sum
#Returns the cumulative sum, where each vector in the new list was the sum of the corresponding input and all vectors before it
def vector_set_cumulative_sum(v_set):

    #Should be a deep copy since we will use the entries.
    v_set_s = deepcopy(v_set)

    #Iterate from the second entry. Each list entry is the original vector plus the previous vectors.
    for i in range(1,len(v_set_s)):
        v_set_s[i] = v_set_s[i] + v_set_s[i-1]

    return v_set_s

#vector_set_extend
#Returns a set of vectors extended by a list of corresponding lengths
def vector_set_extend(v_set,v_extensions):

    #Can be a shallow copy since we will replace all the entries.
    v_set_extended = v_set.copy()

    #Each entry is a vector in the same direction as before, but extended by length k = v_extensions[i]
    for i in range(0,v_set):
        v_set_extended[i] = v_set[i] * (1 + v_extensions[i]/np.linalg.norm(v_set[i]))

    return v_set_extended

#vector_set_difference
#Returns a set of vectors which are the difference between some vector v and each vector in the set
def vector_set_difference(v,v_set):

    #Should probably be a deep copy since we use the values later.
    v_diff = deepcopy(v_set)

    #Each entry in the list is the difference between vector v the original list entry
    for i in range(0,len(v_diff)):
        v_diff[i] = v - v_diff[i]

    return v_diff

