#ROB 417 - Osian Leahy
#This file should include all relevant functions used in drawing the current arm state
#Code is ported from create_axes.m, threeD_draw_links.m

import numpy as np
import matplotlib.pyplot as plt


#create_3d_axes
#Creates a figure with a single 3d axes that we can graph the arm state on and update
#Replaces both #create_axes.m and #create_subaxes.m
def create_3d_axes(fig_num,limits, num_rows=1, num_cols = 1, num_ax = 1):

    #Create and clear the figure to ensure no overplotting
    f = plt.figure(fig_num)
    f.clear()

    #since we're using subplot here anyways, this function can do double duty
    ax = [''] * num_ax

    for i in range(0,num_ax):

        ax[i] = f.add_subplot(num_rows, num_cols, i+1, projection = '3d')
        plt.axis(limits)

    return f,ax

#three_d_draw_links
#Plots each link on a given set of axes, inputs are:
# link_set: a list of 3x2 matrices with columns containing the start & endpoints of a link
# link_colors: a list of matplotlib color codes corresponding to each link
# ax: the axes to draw on
#Returns a list of objects corresponding to each link
def three_d_draw_links(link_set, link_colors, ax:plt.Axes, marker = 'o', linestyle = '-'):
    #Shallow copy since we will replace each entry
    l = link_set.copy()

    #Draw a line for each link, and save the handles to list 'l'
    for i in range(0,len(l)):
        #x values are top row
        #y values are middle row
        #z values are bottom row
        l[i] = ax.plot(link_set[i][0], link_set[i][1], link_set[i][2], color = link_colors[i], marker = marker, linestyle = linestyle)

    return l

#Draw each vector (column) in the array V on an axes at point p using plt.quiver()
def draw_vectors_at_point(p,v,ax,q_colors):

    #list to store our returned object references in:
    cols = np.size(v,1)
    q = [''] * cols

    #plot the arrows:
    for i in range(0,cols):
        q[i] = ax.quiver(p[0][0],p[1][0],p[2][0],v[0][i],v[1][i],v[2][i], color = q_colors[i])

    return q
