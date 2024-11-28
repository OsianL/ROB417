#ROB 417 - Osian Leahy
#This file should include all relevant functions for following paths/trajectories with a Multi-DOF arm
#Code ported form follow_trajectory.m,
import numpy as np
import numdifftools
from scipy.optimize import lsq_linear
from scipy.integrate import solve_ivp


#follow_trajectory_velocity
#Follow a path by feeding velocity commands to the robot arm servos
#Does not consider any robot velocity/acceleration capabilities.
#To allow for smooth accelerations, following of accel/velocity limits, etc a trajectory should be generated and then interpolated to create the path function.

#Inputs:
# t: (double) the current timestep to evaluate the path at
# alpha_state (n_joints x 1 np.array): the current position of the robot arm joints
# jacob (function): Takes the current joint angles as an input and returns the endpoint jacobian for the arm
# path (function): A (3x1 vector valued) function which returns the path position at a given time t.

#Outputs:
# alpha_dot (n_joints x 1 np.array): The commanded joint angle velocities
# v (3x1 vector): The calculated derivative of path at time t.

def follow_trajectory_velocity(t, alpha_state, jacob, path):

    #The Jacobian allows us to convert between constraint velocities and joint velocities given a current position state
    #Therefore we will start by differentiating our path to get it's desired velocity.
    #If we had generated this path via something like a trapezoidal trajectory generator, the accel & velo profiles would already be embedded in the path
    v_fun = numdifftools.Jacobian(path)

    # Note: numdifftools.Jacobian transforms this into a column vectors, but lsq_linear needs a row vector (weird)
    v = np.transpose(v_fun(t))[0]

    #Then just minimize the constraint to find the smallest required joint velocities:
    min_result = lsq_linear(jacob(alpha_state),v)

    alpha_dot = min_result.x

    #Finally return both alphadot and v:
    return alpha_dot,v

#generate_joint_pose_trajectory
#Returns a precalculated (offline) position trajectory to feed to a position controller.
#Integrates over a velocity trajectory to generate the required list of times,poses
#joint_velocity can be the first return of
def generate_joint_pose_trajectory(joint_velocity, t_span, a_initial):

    timespan = [min(t_span),(max(t_span))]

    #Integrate as an initial value problem
        #starts with an initial value for joint angles,
        #uses that to calculate the initial angle change
        #does a finite difference sum to get the next joint angle
    sol = solve_ivp(joint_velocity,timespan,a_initial,t_eval=t_span)

    #return just the timespan and joint angles
    return sol.t,sol.y