####################################################################################
# This file contains import statements that should be relevant for basically
# any python script, or if not, are at least low impact enough that it doesn't
# affect the runtime too dramatically.
#
# yt is specifically excluded because it's extremely heavy and will slow
# down the runtime significantly.
####################################################################################

from HaloData import Fields, HaloData

import sys
import numpy as np

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

####################################################
# Some basic filter functions
####################################################
greater_than = lambda x,y: x>y
less_than = lambda x,y: x<y
greater_than_or_equal_to = lambda x,y: x>=y
less_than_or_equal_to = lambda x,y: x<=y
equal_to = lambda x,y: x==y
