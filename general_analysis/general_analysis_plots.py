import sys
import yt
yt.funcs.mylog.setLevel(50)

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from HaloData import *
from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1 import AxesGrid, make_axes_locatable
from tqdm import tqdm
from matplotlib.colors import LogNorm

matplotlib.rcParams.update({'font.size': 16})
matplotlib.rcParams.update({"figure.facecolor": 'FFFFFF'})
np.set_printoptions(threshold=sys.maxsize)

def to_YTRegion(ds, halo):
    radius = ds.quan(halo[Fields.RADIUS], 'Mpc')
    quans = [ds.quan(x, 'Mpc') for x in [\
                                         halo[Fields.XPOS],\
                                         halo[Fields.YPOS],\
                                         halo[Fields.ZPOS]]]
    
    halo_pos =  np.array(quans) / ds.domain_width.to('Mpc').value

    sphere = ds.sphere(halo_pos, radius)
    return sphere

    
def inspect_halo(ds, halo, zoom=2):
    
    sphere = to_YTRegion(ds, halo)

    HEIGHT = 16
    axes = [None]*4

    axes = [None]*4
    fig, ((axes[0], axes[1]),(axes[2], axes[3])) = plt.subplots(2,2,figsize=(HEIGHT, HEIGHT))
    plt.subplots_adjust(left=0.1, \
                        bottom=0.1,\
                        right=0.9,\
                        top=0.9,\
                        wspace=0.3,\
                        hspace=0.2)

    fields = ['density', 'metallicity','temperature', ('deposit', 'stars_density')]
    cmaps = ['viridis', 'dusk', 'plasma', 'viridis']
    titles = ['Density','Metallicity', 'Temperature', 'Stellar Density']

    p = yt.ProjectionPlot(ds, 'x', fields, sphere.center, \
                          weight_field='density', data_source=sphere)

    frb = p.data_source.to_frb(2*sphere.radius/zoom, 1000)
    data = [None]*4
    data[0] = np.array(frb['density'])
    data[1] = np.array(frb['metallicity'])
    data[2] = np.array(frb['temperature'])
    data[3] = np.array(frb[('deposit','stars_density')])

    for i,ax in enumerate(axes):
        im = ax.imshow(data[i], origin='lower', norm=LogNorm(), cmap=cmaps[i])
        ax.set_title(titles[i])

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(im, cax=cax)
        
    plt.show()

def metallicity_vs_stellar_mass(hd, z):

    hd = hd.filter_by(Fields.NUM_STAR_PARTICLES, greater_than, 10)\
           .filter_by(Fields.TOT_MASS, greater_than, 1e9)
    
    reduced_data = apply_reduction(hd, Fields.STR_MASS, Fields.STR_METAL_FRAC, \
                                   np.median, bin_scale='log')

    sm, median_mf = reduced_data

    Z_approx = lambda M : (M/1e11)**(0.4)
    
    fig, ax = plt.subplots(1,1,figsize=(7,7))

    # stellar mass
    ax.plot(sm, median_mf, label='Z')
    ax.plot(sm, Z_approx(sm), label='Voit 2015 approximation')

    ax.set_xscale('log')
    ax.set_yscale('log')

    #ax.set_ylim(1e-3, 3e1)

    ax.set_ylabel('Z ($Z_\odot$)')
    ax.set_xlabel('$M_* (M_\odot)$')
    ax.legend(loc='best')
    
    plt.title(f'Stellar Metallicity vs. Stellar Mass for massive halos at $z={z}$')
    plt.show()

def star_formation(ds, halo):

    fig, axes = plt.subplots(1,1,figsize=(18,7))

    z_start = 4
    z_end   = 0

    t_start = ds.cosmology.t_from_z(z_start).in_units('Gyr').value
    t_end   = ds.cosmology.t_from_z(z_end).in_units('Gyr').value

    #ad = ds.all_data()
    ad = to_YTRegion(ds, halo)
    masses = ad[('stars', 'particle_mass')].in_units('Msun')
    formation_time = ad[('stars', 'creation_time')].in_units('Gyr') 

    time_range = [t_start, t_end]
    n_bins = 1000
    hist, bins = np.histogram(formation_time, bins=n_bins, range=time_range)
    inds = np.digitize(formation_time, bins=bins)
    time = (bins[:-1] + bins[1:])/2

    redshift = ds.cosmology.z_from_t(time*ds.quan(1,'Gyr'))

    sfr = np.array([masses[inds == j+1].sum()/(bins[j+1]-bins[j]) for j in range(len(time))])
    sfr[sfr == 0] = np.nan

    ssfr = sfr/halo[Fields.STR_MASS]
    
    axes.plot(redshift, ssfr, c='b')
    axes.set_xlim(z_start,z_end)
    axes.set_xlabel('redshift')
    axes.set_ylabel('sSFR  [yr$^{-1}$]')
    
    plt.show()

