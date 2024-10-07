#ROB 417 - Osian Leahy
#This file should include all relevant functions used in processing sets of vectors.
#Code is ported from vector_set_rotate.m, vector_set_cumulative_sum.m, vector_set_extend.m, vector_set_difference.m
from copy import deepcopy
import numpy as np

#Rotates a list of vectors using a corresponding list of rotation matrices
def vector_set_rotate(v_set, r_set):

    v_set_r = v_set.copy()

    for i in range(0,len(v_set_r)):
        v_set_r[i] = np.dot(r_set[i],v_set[i])

    return v_set_r

#Returns the cumulative sum, where each vector in the new list was the sum of the corresponding input and all vectors before it
def vector_set_cumulative_sum(v_set):

    v_set_s = deepcopy(v_set)

    for i in range(1,len(v_set_s)):
        v_set_s[i] = v_set_s[i] + v_set_s[i-1]

    return v_set_s

#Returns a set of vectors extended by a list of corresponding lengths
def vector_set_extend(v_set,v_extensions):

    v_set_extended = v_set.copy()

    for i in range(0,v_set):
        v_set_extended[i] = v_set[i] * (1 + v_extensions[i]/np.linalg.norm(v_set[i]))

    return v_set_extended

#Returns a set of vectors which are the difference between some vector v and each vector in the set
def vector_set_difference(v,v_set):

    v_diff = v_set.copy()

    for i in range(0,len(v_diff)):
        v_diff[i] = v - v_diff[i]

    return v_diff

