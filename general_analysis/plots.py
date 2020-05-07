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


#################################################################################
# Plots that show a general picture of what is occurring within a simulation
# 1st row:
# - Density
# - Temperature
# - Metallicity
# 2nd row:
# - Density with halos annotated
# - All particles
# - Star particles only 
#################################################################################
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

def stellar_mass_fraction_reduced(hd, cutoff=1):

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
            smf_max[i] = np.max(smf_data_bins[i,:count])
            smf_min[i] = np.min(smf_data_bins[i,:count])
            smf_count[i] = count
    #end for i

    # some data cleanup, replaces zero values with nan so they are not plotted
    smf_median[ smf_median==0. ] = np.nan
    smf_max[ smf_max==0. ] = np.nan
    smf_min[ smf_min==0. ] = np.nan

    fig, ax = plt.subplots(3,1,figsize=(7,17.5), sharex='col',\
                           gridspec_kw={'hspace':0, 'wspace':0, 'height_ratios':[1,2,2]})
    ax[0].hist(data, logbins)
    
    ax[1].set_ylim(top=10., bottom=1e-3)
    ax[1].set_yscale('log')
    ax[1].set_xscale('log')

    ax[1].loglog(logbins[:nbins], smf_median)
    ax[1].fill_between(logbins[:nbins], smf_max, smf_min, alpha=0.15)
    
    ax[1].set_ylabel("$M_{*}/(\Omega_b/\Omega_m)/M_{vir}$")

    im = ax[2].scatter(filtered_halos.halos[:,Fields.TOT_MASS],\
                       filtered_halos.halos[:,Fields.STR_MASS_FRAC],\
                       marker='.', alpha=0.15, c='steelblue')
    
    ax[2].set_xlabel("$M_{tot}$  ($M_{\odot}$)")
    ax[2].loglog(logbins[:nbins], smf_median)
    ax[2].fill_between(logbins[:nbins], smf_max, smf_min, alpha=0.15)
    #ax[2].set_ylim(top=10., bottom=1e-5)
    ax[2].set_ylabel("$M_{*}/(\Omega_b/\Omega_m)/M_{vir}$")

    #plt.subplots_adjust(left=0.1, bottom=0.1, right=0.99, top=0.9)
    
    plt.show()
    
    
def main(dataset, halo_dat_fname):
    stellar_mass_fraction_scatter(halo_dat_fname)
    density_projection(dataset)
    weighted_projection(dataset, 'density')
    weighted_projection(dataset, 'temperature')
    


if __name__ == "__main__":

    usage_str =\
    """
Usage: 
    python plots.py <dataset_file_name> <halo_dat_file>
    """

    argc = len(sys.argv)
    if argc != 2 and argc != 1:
        print(usage_str)
        sys.exit()

    if argc == 1:
        print("Running in test mode")
        dataset_fname  = "test_data/RD0009/RD0009"
        halo_dat_fname = "test_data/halo_test.dat"
        PLOT_DIR       = "test_plots"
    else:
        dataset_fname  = sys.argv[1]
        halo_dat_fname = sys.argv[2]

    dataset = yt.load(dataset_fname)
        
    main(dataset, halo_dat_fname)
