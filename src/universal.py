####################################################################################
# This file contains import statements that should be relevant for basically
# any python script, or if not, are at least low impact enough that it doesn't
# affect the runtime too dramatically.
#
# yt is specifically excluded because it's extremely heavy and will slow
# down the runtime significantly.
####################################################################################

import sys
import numpy as np
import pickle
from time import time as get_time


####################################################
# Some basic filter functions
####################################################
greater_than = lambda x,y: x>y
less_than = lambda x,y: x<y
greater_than_or_equal_to = lambda x,y: x>=y
less_than_or_equal_to = lambda x,y: x<=y
equal_to = lambda x,y: x==y


####################################################
# yt filter functions for enzo datasets
#
# Ex.
# First call:
# add_particle_filter("stars", function=StarParticle, filtered_type='all', \
#                     requires=["particle_type"])
#
# Then you can add it to a dataset
#     ds.add_particle_filter('stars')
#
####################################################
def StarParticle(pfilter, data):
    filter = data[("all", "particle_type")] == 2 # DM = 1, Stars = 2
    return filter

def DarkMatter(pfilter, data):
    filter = data[("all", "particle_type")] == 1 # DM = 1, Stars = 2
    return filter
    
def MustRefineDarkMatter(pfilter, data):
    filter = data[("all", "particle_type")] == 4 # Must Refine Particle type
    return filter


####################################################################################
# Takes in a YT dataset object and a single halo and returns a YT Region object
####################################################################################
def to_YTRegion(ds, halo):
    radius = ds.quan(halo[Fields.RADIUS], 'Mpc')
    quans = [ds.quan(x, 'Mpc') for x in [\
                                         halo[Fields.XPOS],\
                                         halo[Fields.YPOS],\
                                         halo[Fields.ZPOS]]]
    
    halo_pos =  np.array(quans) / ds.domain_width.to('Mpc').value

    sphere = ds.sphere(halo_pos, radius)
    return sphere


##########################################################
# Conditional Print
# prints only if the condition is true
# saves a line of code when debugging
##########################################################
def ifprint(arg, c):
    if c:
        print(arg)

        
