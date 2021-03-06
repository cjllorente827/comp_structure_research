import sys
import yt
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from HaloData import *
from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1 import AxesGrid
from tqdm import tqdm

from BehrooziFit import stellar_mass as SM_FIT_FUNC

matplotlib.rcParams.update({'font.size': 16})
matplotlib.rcParams.update({"figure.facecolor": 'FFFFFF'})
np.set_printoptions(threshold=sys.maxsize)
    

####################################################################################################
# Creates a scatter plot for doing inspection of halo data extracted from a halo catalog.
# Allows for multiple filters to be placed on the dataset.

# color_field - Colors halos according to one of the fields defined in HaloData.py
# filter_fields - This can be an integer or a list of integers representing
#                 fields to filter by. The list of integers that map to fields is defined
#                 in HaloData.py
# filter_funcs - A function or list of functions to apply. Applied in the same order as
#                filter_fields
# filter_values - A value or list of values to filter by
# 
####################################################################################################
def stellar_mass_fraction_scatter(hd, **kwargs):
    global PLOT_DIR

    # assign keyword arguments to variables
    color_field  = kwargs['color_field'] if 'color_field' in kwargs else Fields.NUM_STAR_PARTICLES

    # correcting for the way Behroozi calculates stellar mass fraction
    #smf_correction = 1.
    smf_correction = (0.0486)/(0.0486 + 0.2589)
    
    HEIGHT = 6
    WIDTH = HEIGHT*1.3
    fig, ax = plt.subplots(1,1,figsize=(WIDTH,HEIGHT))

    #keeps all the plots on the same color scale
    norm=matplotlib.colors.LogNorm()
    
    im = ax.scatter(hd.halos[:,Fields.TOT_MASS],\
                    hd.halos[:,Fields.STR_MASS_FRAC]*smf_correction,\
                    c=hd.halos[:,color_field],\
                    marker='.', cmap='viridis', norm=norm)
            
    ax.set_xlabel("$M_{tot}$  ($M_{\odot}$)")
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.tick_params(direction='in', which='both')
    
    ax.set_ylim(top=2., bottom=1e-6)
    ax.set_xlim(left=9e7, right=2e14)
    ax.set_ylabel("$M_{*}/M_{vir}$")

    fig.colorbar(im, ax=ax)
    fig.suptitle("Stellar Mass Fraction")
    plt.show()

def stellar_mass_fraction_reduced(hd_list, z_list):

    fig, ax = plt.subplots(1,2,figsize=(18,7))
    omega = (0.0486)/(0.0486 + 0.2589)

    colors    = ['r','g','b']

    fit_domain = np.logspace(10, 15)
    
    for hd, z, color in zip(hd_list, z_list, colors):
        reduced_data = apply_reduction(hd, Fields.TOT_MASS, Fields.STR_MASS, \
                                   [np.median,np.max,np.min], bin_scale='log')

        hm, median_sm, max_sm, min_sm = reduced_data

        median_sm_fit = SM_FIT_FUNC(fit_domain, z)

        median_fsm = median_sm/hm
        median_fsm_fit = median_sm_fit/fit_domain
    
        # stellar mass
        ax[0].plot(hm, median_sm, label=f'$z=${z}', c=color)
        ax[0].plot(fit_domain, median_sm_fit, linestyle='dashed', c=color)

        #ax[0].fill_between(hm, max_sm, min_sm, alpha=0.25)

        # stellar mass fraction
        ax[1].plot(hm, median_fsm, label=f'$z=${z}', c=color)
        ax[1].plot(fit_domain, median_fsm_fit, linestyle='dashed', c=color)

        #ax[1].fill_between(hm, max_sm/hm, min_sm/hm, alpha=0.25)

    ax[0].set_xscale('log')
    ax[0].set_yscale('log')
    ax[1].set_xscale('log')
    ax[1].set_yscale('log')

    ax[0].set_ylabel('$M_* (M_{\odot})$')
    ax[0].set_xlabel('$M_h (M_{\odot})$')
    ax[0].set_xlim(0.9*min(fit_domain), 1.1*max(fit_domain))

    ax[1].set_xlim(0.9*min(fit_domain), 1.1*max(fit_domain))
    ax[1].set_ylim(1e-4, 0.1)
    ax[1].set_ylabel('$f_{sm} = M_*/M_h$')
    ax[1].set_xlabel('$M_h (M_{\odot})$')
    ax[1].legend(loc=(1.1,0.5))

    plt.show()


def baryon_frac(hd, z):
    
    fig, ax = plt.subplots(1,1,figsize=(14,7))

    sm, hm = apply_reduction(hd, Fields.STR_MASS, Fields.TOT_MASS, \
                                   np.median, bin_scale='log')
    
    sm, median_bm = apply_reduction(hd, Fields.STR_MASS, Fields.BAR_MASS, \
                                 np.median, bin_scale='log')

    baryon_frac = (0.0486)/(0.0486 + 0.2589)

    gas_mass_peeples_2014 = lambda M: M * 10**(-0.48 * np.log10(M) + 4.39)

    hm_fit = np.logspace(9, 14)
    z = 0
    median_sm_fit = SM_FIT_FUNC(hm_fit, z)
    gm = gas_mass_peeples_2014(median_sm_fit)


    ax.plot(sm, sm/baryon_frac/hm, color='darkred', label="Stars")
    ax.plot(median_sm_fit, median_sm_fit/baryon_frac/hm_fit, color='darkred', label="Behroozi 2013",\
            linestyle='dashed')
    ax.plot(sm, median_bm/baryon_frac/hm, color='darkblue', label="Gas + Dust")
    ax.plot(median_sm_fit, (gm+median_sm_fit)/baryon_frac/hm_fit, color='darkblue',\
            label="Peeples 2014", linestyle='dashed')

    ax.set_xscale('log')
    ax.legend(loc=(1.05,0.5))

    ax.set_ylabel("Mass fraction $(M/(\Omega_b/\Omega_m)/M_h )$")
    ax.set_xlabel("$M_* (M_{\odot})$")
    plt.show()
    
def hist_2d(hd, z):
    greater_than = lambda val, cut: val > cut
    
    fig, ax = plt.subplots(1,1,figsize=(14,7))

    nbins = 0.5*int(np.sqrt(hd.num_halos))
    sm = np.log10(hd.halos[:,Fields.STR_MASS])
    hm = np.log10(hd.halos[:,Fields.TOT_MASS])

    hist, x, y = np.histogram2d(hm, sm, bins=nbins)

    X,Y = np.meshgrid(x[:-1],y[:-1])
    ax.contour(10**X,10**Y,hist.T)

    
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.show()
