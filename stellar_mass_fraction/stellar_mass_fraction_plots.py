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


def stellar_mass_fraction_scatter(hd, cutoff=1):
    global PLOT_DIR
    
    #filter by number of star particles
    filter_func = lambda val, cut: val > cut
    filtered_halos = filter_by(hd, Fields.NUM_STAR_PARTICLES, filter_func, cutoff)
    
    fig, ax = plt.subplots(1,1,figsize=(7,7))

    # correcting for the way Behroozi calculates stellar mass fraction
    #smf_correction = 1.
    smf_correction = (0.0486)/(0.0486 + 0.2589)

    im = ax.scatter(filtered_halos.halos[:,Fields.TOT_MASS],\
              filtered_halos.halos[:,Fields.STR_MASS_FRAC]*smf_correction,\
              c=filtered_halos.halos[:,Fields.NUM_STAR_PARTICLES],\
                    marker='.', cmap='viridis', norm=matplotlib.colors.LogNorm())
    ax.set_title("Stellar Mass Fraction")
    ax.set_xlabel("$M_{tot}$  ($M_{\odot}$)")
    ax.set_ylim(top=2., bottom=1e-6)
    ax.set_yscale('log')
    ax.set_xscale('log')
    
    ax.set_ylabel("$M_{*}/M_{vir}$")

    fig.colorbar(im, ax=ax)
    plt.show()
    #plt.savefig("stellar_mass_fraction_bigbox.png")

def stellar_mass_fraction_scatter_multi(hd, halo_mass_filter=None):
    global PLOT_DIR

    HEIGHT = 6
    
    cutoffs = [0,1,10,100]
    N = len(cutoffs)

    # correcting for the way Behroozi calculates stellar mass fraction
    #smf_correction = 1.
    smf_correction = (0.0486)/(0.0486 + 0.2589)
    
    fig, axes = plt.subplots(1,N,figsize=(N*HEIGHT,HEIGHT), sharey='row',\
                             gridspec_kw={'hspace':0, 'wspace':0})

    #keeps all the plots on the same color scale
    norm=matplotlib.colors.LogNorm()

    for i in range(0, N):

        ax = axes[i]
        cutoff = cutoffs[i]
        
        #filter by number of star particles
        filter_func = lambda val, cut: val > cut
        filtered_halos = filter_by(hd, Fields.NUM_STAR_PARTICLES, filter_func, cutoff)

        #filter by halo mass
        if halo_mass_filter is not None:
            filtered_halos = filter_by(filtered_halos, Fields.TOT_MASS, filter_func,\
                                       halo_mass_filter)
    
        im = ax.scatter(filtered_halos.halos[:,Fields.TOT_MASS],\
              filtered_halos.halos[:,Fields.STR_MASS_FRAC]*smf_correction,\
              c=filtered_halos.halos[:,Fields.NUM_STAR_PARTICLES],\
                        marker='.', cmap='viridis', norm=norm)

        if cutoff == 0:
            ax.set_title("No cutoff")
        else:
            ax.set_title(f"Cutoff at > {cutoff} star particles")
            
        ax.set_xlabel("$M_{tot}$  ($M_{\odot}$)")
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.tick_params(direction='in', which='both')
    
    axes[0].set_ylim(top=2., bottom=1e-6)
    axes[0].set_ylabel("$M_{*}/M_{vir}$")

    fig.colorbar(im, ax=axes[-1])
    fig.suptitle("Stellar Mass Fraction with different cutoffs")
    plt.show()

def stellar_mass_fraction_reduced(hd, z, min_nstar=None, min_halo_mass=None):

    greater_than = lambda val, cut: val > cut

    if min_nstar is not None:
        hd = filter_by(hd, Fields.NUM_STAR_PARTICLES, greater_than, 10)

    if min_halo_mass is not None:
        hd = filter_by(hd, Fields.TOT_MASS, greater_than, 1e10)

    reduced_data = apply_reduction(hd, Fields.TOT_MASS, Fields.STR_MASS, \
                                   [np.median,np.max,np.min], bin_scale='log')

    hm, median_sm, max_sm, min_sm = reduced_data

    z = 0
    median_sm_fit = SM_FIT_FUNC(hm, z)
    omega = (0.0486)/(0.0486 + 0.2589)

    median_fsm = median_sm/hm
    median_fsm_fit = median_sm_fit/hm
    
    fig, ax = plt.subplots(1,2,figsize=(18,7))

    # stellar mass
    ax[0].plot(hm, median_sm, label='Median $M_*$')
    ax[0].plot(hm, median_sm_fit, label='Behroozi fit')

    #ax[0].fill_between(hm, max_sm, min_sm, alpha=0.25)

    # stellar mass fraction
    ax[1].plot(hm, median_fsm, label='Median $f_{sm}$')
    ax[1].plot(hm, median_fsm_fit, label='Behroozi fit')

    #ax[1].fill_between(hm, max_sm/hm, min_sm/hm, alpha=0.25)

    ax[0].set_xscale('log')
    ax[0].set_yscale('log')
    ax[1].set_xscale('log')
    ax[1].set_yscale('log')

    ax[0].set_ylabel('$M_* (M_{\odot})$')
    ax[0].set_xlabel('$M_h (M_{\odot})$')
    
    ax[1].set_ylim(1e-5, 2)
    ax[1].set_ylabel('$f_{sm} = M_*/M_h$')
    ax[1].set_xlabel('$M_h (M_{\odot})$')
    ax[1].legend(loc=(1.1,0.5))

    # add the 2d histograms
    nbins = 0.5*int(np.sqrt(hd.num_halos))
    sm = np.log10(hd.halos[:,Fields.STR_MASS])
    hm = np.log10(hd.halos[:,Fields.TOT_MASS])

    hist2d, x, y = np.histogram2d(hm, sm, bins=nbins)

    X,Y = np.meshgrid(x[:-1],y[:-1])
    ax[0].contour(10**X,10**Y,hist2d.T, colors='steelblue', alpha=0.5)
    ax[1].contour(10**X,10**Y/10**X,hist2d.T, colors='steelblue', alpha=0.5)


    plt.show()


def baryon_frac(hd, z, min_nstar=None, min_halo_mass=None):
    
    greater_than = lambda val, cut: val > cut

    if min_nstar is not None:
        hd = filter_by(hd, Fields.NUM_STAR_PARTICLES, greater_than, 10)

    if min_halo_mass is not None:
        hd = filter_by(hd, Fields.TOT_MASS, greater_than, 1e10)
    
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


def hist_2d(hd, z, min_nstar=None, min_halo_mass=None):
    greater_than = lambda val, cut: val > cut

    if min_nstar is not None:
        hd = filter_by(hd, Fields.NUM_STAR_PARTICLES, greater_than, 10)

    if min_halo_mass is not None:
        hd = filter_by(hd, Fields.TOT_MASS, greater_than, 1e10)
    
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
