#ROB 417 - Osian Leahy
#This file should include all relevant functions used in drawing the current arm state
#Code is ported from create_axes.m, threeD_draw_links.m

import numpy as np
import matplotlib.pyplot as plt
from jmespath.ast import projection

#create_3d_axes
#Creates a figure with a single 3d axes that we can graph the arm state on and update
def create_3d_axes(fig_num,limits):

    f = plt.figure(fig_num)

    f.clear()

    ax = f.add_subplot(111 ,projection = '3d')

    plt.axis(limits)

    return f,ax

#three_d_draw_links
#Plots each link on a given set of axes, inputs are:
# link_set: a list of 3x2 matrices with columns containing the start & endpoints of a link
# link_colors: a list of matplotlib color codes corresponding to each link
# ax: the axes to draw on
#Returns a list of objects corresponding to each link
def three_d_draw_links(link_set, link_colors, ax:plt.Axes, linestyle):
    #Shallow copy since we will replace each entry
    l = link_set.copy()

    #Draw a line for each link, and save the handles to list 'l'
    for i in range(0,len(l)):
        #x values are top row
        #y values are middle row
        #z values are bottom row
        l[i] = ax.plot(link_set[i][0], link_set[i][1], link_set[i][2], color = link_colors[i], marker = 'o', linestyle = linestyle)

    #plt.axis('equal')

    return l
