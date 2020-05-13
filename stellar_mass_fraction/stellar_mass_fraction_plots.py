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

def halo_mass_histogram(hd, cutoff=0):
    #filter by number of star particles
    filter_func = lambda val, cut: val > cut
    filtered_halos = filter_by(hd, Fields.NUM_STAR_PARTICLES, filter_func, cutoff)

    data = filtered_halos.halos[:,Fields.TOT_MASS]
    hist, bins = np.histogram(data, bins=50)
    logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
    
    plt.hist(data, logbins)
    plt.xscale('log')
    #plt.plot(filtered_halos.halos[:,Fields.STR_MASS_FRAC])


def stellar_mass_fraction_scatter(hd, cutoff=1):
    global PLOT_DIR
    
    #filter by number of star particles
    filter_func = lambda val, cut: val > cut
    filtered_halos = filter_by(hd, Fields.NUM_STAR_PARTICLES, filter_func, cutoff)
    
    fig, ax = plt.subplots(1,1,figsize=(7,7))

    im = ax.scatter(filtered_halos.halos[:,Fields.TOT_MASS],\
              filtered_halos.halos[:,Fields.STR_MASS_FRAC],\
              c=filtered_halos.halos[:,Fields.NUM_STAR_PARTICLES],\
                    marker='o', cmap='viridis', norm=matplotlib.colors.LogNorm())
    ax.set_title("Stellar Mass Fraction")
    ax.set_xlabel("$M_{tot}$  ($M_{\odot}$)")
    ax.set_ylim(top=10., bottom=1e-5)
    ax.set_yscale('log')
    ax.set_xscale('log')
    
    ax.set_ylabel("$M_{*}/(\Omega_b/\Omega_m)/M_{vir}$")

    fig.colorbar(im, ax=ax)
    plt.show()
    #plt.savefig("stellar_mass_fraction_bigbox.png")

def stellar_mass_fraction_scatter_multi(hd):
    global PLOT_DIR

    HEIGHT = 6
    
    cutoffs = [0,1,10,100]
    N = len(cutoffs)
    
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
    
        im = ax.scatter(filtered_halos.halos[:,Fields.TOT_MASS],\
              filtered_halos.halos[:,Fields.STR_MASS_FRAC],\
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
    
    axes[0].set_ylim(top=10., bottom=1e-5)
    axes[0].set_ylabel("$M_{*}/(\Omega_b/\Omega_m)/M_{vir}$")

    fig.colorbar(im, ax=axes[-1])
    fig.suptitle("Stellar Mass Fraction with different cutoffs")
    plt.show()

def stellar_mass_fraction_reduced(hd, behroozi_data, cutoff=1):

    filter_func = lambda val, cut: val > cut
    filtered_halos = filter_by(hd, Fields.NUM_STAR_PARTICLES, filter_func, cutoff)

    nbins = int(np.sqrt(filtered_halos.num_halos))
    
    data = filtered_halos.halos[:,Fields.TOT_MASS]
    hist, bins = np.histogram(data, bins=nbins)
    logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
    hist, null = np.histogram(data, bins=logbins)
    
    #nbins = len(logbins)-1
    maxlen = np.max(hist)+1 # have an extra slot at the end for safety
    smf_data_bins = np.zeros((nbins, maxlen))
    smf_median    = np.zeros(nbins)
    smf_mean    = np.zeros(nbins)
    smf_max       = np.zeros(nbins)
    smf_min       = np.zeros(nbins)
    smf_count     = np.zeros(nbins)

    for i in range(0, nbins):
        left_edge = logbins[i]
        right_edge = logbins[i+1]
        count = 0
        for j in range(0, filtered_halos.num_halos):
            halo = filtered_halos.halos[j]
            if halo[Fields.TOT_MASS] >= left_edge and halo[Fields.TOT_MASS] < right_edge:
                smf_data_bins[i, count] = halo[Fields.STR_MASS_FRAC]
                count += 1
        # end for j

        if count > 0:
            smf_median[i] = np.median(smf_data_bins[i,:count])        
            smf_mean[i] = np.mean(smf_data_bins[i,:count])        
            smf_max[i] = np.max(smf_data_bins[i,:count])
            smf_min[i] = np.min(smf_data_bins[i,:count])
            smf_count[i] = count
    #end for i

    # some data cleanup, replaces zero values with nan so they are not plotted
    smf_median[ smf_median==0. ] = np.nan
    smf_mean[ smf_mean==0. ] = np.nan
    smf_max[ smf_max==0. ] = np.nan
    smf_min[ smf_min==0. ] = np.nan

    fig, ax = plt.subplots(3,1,figsize=(7,17.5), sharex='col',\
                           gridspec_kw={'hspace':0, 'wspace':0, 'height_ratios':[1,2,2]})
    ax[0].hist(data, logbins)
    
    ax[1].set_ylim(top=10., bottom=1e-3)
    ax[1].set_yscale('log')
    ax[1].set_xscale('log')

    # correcting for the way Behroozi calculates stellar mass fraction
    #smf_correction = 1.
    smf_correction = (0.0486)/(0.0486 + 0.2589)

    ax[1].loglog(logbins[:nbins], smf_median*smf_correction)
    ax[1].loglog(logbins[:nbins], smf_mean*smf_correction)
    ax[1].fill_between(logbins[:nbins], smf_max*smf_correction, smf_min*smf_correction,\
                       alpha=0.15)
    
    im = ax[2].scatter(filtered_halos.halos[:,Fields.TOT_MASS],\
                       filtered_halos.halos[:,Fields.STR_MASS_FRAC]*smf_correction,\
                       marker='.', alpha=0.15, c='steelblue')
    
    ax[2].loglog(logbins[:nbins], smf_median*smf_correction, label='Median')
    ax[2].loglog(logbins[:nbins], smf_mean*smf_correction, label='Mean')
    ax[2].fill_between(logbins[:nbins], smf_max*smf_correction, smf_min*smf_correction,\
                       alpha=0.15)

    ax[1].set_ylabel("$M_{*}/M_h$")
    ax[2].set_xlabel("$M_{tot}$  ($M_{\odot}$)")
    ax[2].set_ylabel("$M_{*}/M_h$")

    #plt.subplots_adjust(left=0.1, bottom=0.1, right=0.99, top=0.9)

    halo_mass, smf, err_up, err_dn = np.loadtxt(behroozi_data, unpack=True)
    smf = 10**(smf)
    halo_mass = 10**(halo_mass)
    ax[1].loglog(halo_mass, smf, c='green')
    ax[2].loglog(halo_mass, smf, c='green', label='Behroozi 2013')

    ax[1].set_xlim((1e9, 2e13))
    ax[1].set_ylim((1e-4, 2))
    ax[2].set_xlim((1e9, 2e13))
    ax[2].set_ylim((1e-4, 2))
    ax[2].legend()
    
    plt.show()
