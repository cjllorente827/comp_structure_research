import sys
import yt
yt.funcs.mylog.setLevel(50)

from universal import *

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from HaloData import Fields, HaloData, to_YTRegion, apply_reduction
from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1 import AxesGrid, make_axes_locatable
from tqdm import tqdm
from matplotlib.colors import LogNorm
from scipy.optimize import curve_fit

matplotlib.rcParams.update({'font.size': 16})
matplotlib.rcParams.update({"figure.facecolor": 'FFFFFF'})
np.set_printoptions(threshold=sys.maxsize)
    
def inspect_halo(ds, halo, zoom=2):
    
    sphere = to_YTRegion(ds, halo)

    HEIGHT = 16

    axes = [None]*4
    fig, ((axes[0], axes[1]),(axes[2], axes[3])) = plt.subplots(2,2,figsize=(HEIGHT, HEIGHT))
    plt.subplots_adjust(left=0.1, \
                        bottom=0.1,\
                        right=0.9,\
                        top=0.9,\
                        wspace=0.3,\
                        hspace=0.2)

    fields = ['density', 'metallicity','temperature', ('deposit', 'stars_density')]
    cmaps = ['viridis', 'dusk', 'plasma', 'Purples_r']
    titles = ['Density','Metallicity', 'Temperature', 'Stellar Density']

    p = yt.ProjectionPlot(ds, 'x', fields, sphere.center, \
                          weight_field='density', data_source=sphere)

    frb = p.data_source.to_frb(2*sphere.radius/zoom, 1000)
    data = [None]*4
    data[0] = np.array(frb['density'])
    data[1] = np.array(frb['metallicity'])
    data[2] = np.array(frb['temperature'])

    star_density = np.array(frb[('deposit','stars_density')])
    star_density[star_density == 0.] = 1e-33
    
    data[3] = star_density[:]

    for i,ax in enumerate(axes):
        im = ax.imshow(data[i], origin='lower', norm=LogNorm(), cmap=cmaps[i])
        ax.set_title(titles[i])

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(im, cax=cax)
        
    plt.show()



##################################################################
# Empirical fit function for the Stellar Mass Metallicty relation
# over cosmic time in units of solar masses and solar metallicities
#
# Adapted from Behroozi 2019
# originally developed in Maiolino 2008
# Behroozi mentions setting a lower metallicity floor at
# log Z = -1.5 to avoid unphysical metallicities
# This might need to be implemented here as well
##################################################################
def Behroozi_metallicity(M_star, z):
    M0 = 10**(11.22 + 0.47*z)
    K0 = 9.07 - 0.07 * z
    log_OH_12 = K0 - 0.086 * ( np.log10(M_star/M0)**2 ) # log(O/H) + 12

    # convert to solar metallicity (I hope)
    Z = log_OH_12 - 8.66
    Z[Z < 10**(-1.5)] = 10**(-1.5)
    return Z

def Voit_metallicity(M_star):
    return (M_star * 1e-11)**(0.4)
    

def metallicity_vs_stellar_mass(hd_list, z_list):

    fig, ax = plt.subplots(1,1,figsize=(8,7))

    colors = plt.cm.viridis(np.linspace(0, 1,len(hd_list)+1 ))
    

    for hd, z, color in zip(hd_list, z_list, colors):
    
        reduced_data = apply_reduction(hd, Fields.STR_MASS, Fields.STR_METAL_FRAC, \
                                   np.median, bin_scale='log')

        sm, median_Z = reduced_data
        fit = Behroozi_metallicity(sm, z)

        if z == 0.:
            ax.loglog(sm, Voit_metallicity(sm), c='k', label='Voit 2015', linestyle=':')

        ax.loglog(sm, median_Z, label=f'$z = {z}$', c=color)
        ax.loglog(sm, fit, linestyle='--', c=color)
        ax.set(
            ylabel=r'$Z (Z_\odot$)',
            xlabel=r'$M_* (M_\odot)$'
#            ylim=(1e-3, 3)
        )
    # end for hd, z

    ax.legend(loc='best')
    
    plt.title(f'Stellar Metallicity vs. Stellar Mass for massive halos')
    plt.show()

def plot_halo_ssfr(ds, halo, guess=[1,-1]):

    z_start = 8
    z_end   = 0

    t_start = float(ds.cosmology.t_from_z(z_start).in_units('yr').value)
    t_end   = float(ds.cosmology.t_from_z(z_end).in_units('yr').value)

    ad = to_YTRegion(ds, halo)
    masses = ad[('stars', 'particle_mass')].in_units('Msun')
    formation_time = ad[('stars', 'creation_time')].in_units('yr')

    # Using equally spaced time bins
    time_range = [t_start, t_end]
    n_bins = 100
    hist, bins = np.histogram(formation_time, bins=n_bins, range=time_range)
    inds = np.digitize(formation_time, bins=bins)
    time = (bins[:-1] + bins[1:])/2

    # cumulative stellar mass
    csm = np.array([masses[inds <= j+1].sum() for j in range(len(time))])

    # star formation rate
    sfr = np.array([masses[inds == j+1].sum()/(bins[j+1]-bins[j]) for j in range(len(time))])
    
    # sfr[sfr == 0] = np.nan

    # cut out the time before stars appear
    # otherwise the fit gets messed up
    sfr   = sfr[csm > 0]
    time  = time[csm > 0]
    csm   = csm[csm > 0.]

    # specific star formation rate
    ssfr = sfr/csm

    # enforce a minimum ssfr, these points will be ignored by the fit function
    ssfr[ssfr < 1e-13] = 1e-13

    # power law fit function, assumes initial guess is negative
    fit_func = lambda t, k,a:  k*(t)**(a)

    # linear fit function
    lin_func = lambda x, m,b: m*x + b

    try : 
        p, popt = curve_fit(lin_func,
                            np.log10(time[ssfr > 1e-13]),
                            np.log10(ssfr[ssfr > 1e-13]),
                            p0=guess)
        ssfr_fit = lambda t: 10**lin_func(np.log10(t), p[0], p[1])
    except RuntimeError:                
        print("Couldn't create fit. Plotting data and guess")
        ssfr_fit = lambda t: fit_func(t, guess[0], guess[1])  


    #Using equally spaced redshift bins

    ########################################################
    # This method is kinda misleading given the wide variance
    # in the amount of time between redshifts.
    # Keeping it around in case I ever need it, but not
    # gonna bother with it right now.
    ########################################################
    
    # z_range = [z_end, z_start]
    # hist, bins = np.histogram(formation_z, bins=n_bins, range=z_range)
    # inds = np.digitize(formation_z, bins=bins)
    # redshift = (bins[:-1] + bins[1:])/2

    # dt = [ abs(ds.cosmology.t_from_z(bins[j+1]) - ds.cosmology.t_from_z(bins[j]))/(3600*24*365.25)\
    #        for j in range(len(redshift)) ]
    # sfr = np.array([masses[inds == j+1].sum()/dt[j] for j in range(len(redshift))])
    # sfr[sfr == 0] = np.nan

    # ssfr = sfr/halo[Fields.STR_MASS]

    # axes[1].semilogy(redshift, ssfr, c='b')
    # axes[1].invert_xaxis()
    # axes[1].set_xlabel('Redshift')
    # axes[1].set_ylabel('sSFR  [yr$^{-1}$]')
    rows = 1
    cols = 1
    fig, axes = plt.subplots(rows,cols,figsize=(18*cols,7*rows))

    fit = ssfr_fit(time)

    text_xoffset = 0.05
    text_yoffset = np.nanmin(fit)
    for z in range(5):
        t = float(ds.cosmology.t_from_z(z).in_units('Gyr').value)
        axes.axvline(t, linestyle='dashed', c='k')
        axes.text(t+text_xoffset,text_yoffset, f"z={z}" )

    axes.loglog(time/1e9, fit, c='b', linestyle='dashed')
    axes.loglog(time/1e9, ssfr, c='b', linewidth=0, marker='o')
    axes.set_xlabel('Time (Gyr)')
    axes.set_ylabel('sSFR  [yr$^{-1}$]')
    axes.set_title(f'sSFR for halo with M={halo[Fields.STR_MASS]:.1e} $M_\odot$')
    
    plt.show()
