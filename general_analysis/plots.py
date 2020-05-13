import sys
import yt
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from HaloData import *
from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1 import AxesGrid
from tqdm import tqdm

matplotlib.rcParams.update({'font.size': 16})

PLOT_DIR = "plots"

def projection_w_halos(ds, hd, field):

    proj = yt.ProjectionPlot(ds, 'x', field)

    # for coordinate system offsets
    ad = ds.all_data()
    dims = (ad.right_edge-ad.left_edge).to('Mpc')
    yoff = (dims[1]/2).value
    zoff = (dims[2]/2).value

    print("Annotating halos...")
    for i in tqdm(range(0,hd.num_halos)):
        halo = hd.halos[i]
        halo_pos = np.array([halo[Fields.YPOS],halo[Fields.ZPOS]]) # in kpc

        # TODO: Figure out a better way of handling this.
        # Probably best to just save the data in code units during data extraction
        
        # convert to Mpc
        halo_pos *= 1e-3

        # offset center of coordinate system
        halo_pos[0] -= yoff
        halo_pos[1] -= zoff
        
        rad = halo[Fields.RADIUS] # in kpc
        proj.annotate_sphere(halo_pos, radius=(1000,'kpc'), coord_system='plot')

    return proj

def density_projection(ds):
    global PLOT_DIR
    
    plot = yt.ProjectionPlot(ds, 'x', "density")
    plot.display(f"{PLOT_DIR}/{ds.basename}_density.png")
    return plot

def weighted_projection(ds, field_name):
    global PLOT_DIR
    
    plot = yt.ProjectionPlot(ds, 'x', "density", weight_field=field_name)
    plot.display(f"{PLOT_DIR}/{ds.basename}_weighted_{field_name}.png")
    return plot
