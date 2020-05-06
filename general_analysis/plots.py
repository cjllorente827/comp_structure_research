import sys
import yt
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from HaloData import *
from matplotlib.animation import FuncAnimation

matplotlib.rcParams.update({'font.size': 16})

PLOT_DIR = "plots"

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

def stellar_mass_fraction_scatter(halo_dat_fname, cutoff=1):
    global PLOT_DIR
    hd = HaloData.load_from_file(halo_dat_fname)
    
    #filter by number of star particles
    filter_func = lambda val, cut: val > cut
    filtered_halos = filter_by(hd, Fields.NUM_STAR_PARTICLES, filter_func, cutoff)

    # create a color axis for number of star particles
    # color_map   = plt.cm.viridis
    # color_range = np.log10(filtered_halos.halos[:,Fields.NUM_STAR_PARTICLES]/\
    #                        np.max(filtered_halos.halos[:,Fields.NUM_STAR_PARTICLES]))
    # colors      = color_map(color_range)

    print(f"Plotting {filtered_halos.num_halos} of {hd.num_halos} halos")
    
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
