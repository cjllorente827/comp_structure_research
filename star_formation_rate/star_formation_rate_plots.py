############################################################################
# This code uses the extracted halo data along with the original
# Enzo dataset in order to create star formation histories of each halo
#
# The file it creates has the following format
# Halo ID | Stellar Mass (Msun) | SFR at z=start .............. SFR at z=end (Msun/yr) |
#
# This allows for a single dataset from which the SFR and sSFR can be derived
#
# The code relies on these settings for the starting redshift and ending
# redshift, as well as the amount of bins to create.
# These will be used to create a series of bins equally spaced in redshift-space
# for stars to be sorted into

z_start = 8
z_end   = 0
nbins   = 10
############################################################################


import sys

if len(sys.argv) != 3:
    print("""
Usage: python star_formation_rate_plots.py <enzo_dataset> <halo_dataset>
    """)
    exit()
sys.path.append('/mnt/home/llorente/comp_structure_research')

import yt
yt.funcs.mylog.setLevel(50)
yt.enable_parallelism()

def stars(pfilter, data):
    filter = data[("all", "particle_type")] == 2 # DM = 1, Stars = 2
    return filter

yt.add_particle_filter("stars", function=stars, filtered_type='all', \
                       requires=["particle_type"])

from time import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from HaloData import *
from tqdm import tqdm
from matplotlib.colors import LogNorm

matplotlib.rcParams.update({'font.size': 16})
matplotlib.rcParams.update({"figure.facecolor": 'FFFFFF'})
np.set_printoptions(threshold=sys.maxsize)

########################################################################
# Takes in a dataset and a halo and returns an array containing 
# specific star formation rate during the specified time
########################################################################
def determine_halo_ssfr(ds, halo, t_start, t_end, tbins):
    global nbins

    ad = to_YTRegion(ds, halo)
    masses = ad[('stars', 'particle_mass')].in_units('Msun')
    formation_time = ad[('stars', 'creation_time')].in_units('yr')

    # Using equally spaced time bins
    time_range = [t_start, t_end]

    hist, bins = np.histogram(formation_time, bins=nbins, range=time_range)
    inds = np.digitize(formation_time, bins=bins)

    tbins = (bins[:-1] + bins[1:])/2 if tbins is None else tbins

    # cumulative stellar mass
    csm = np.array([masses[inds <= j+1].sum() for j in range(len(tbins))])

    # star formation rate
    sfr = np.array([masses[inds == j+1].sum()/(bins[j+1]-bins[j]) for j in range(len(tbins))])

    # specific star formation rate
    ssfr = sfr/csm

    #replace all NaN values with zeros
    ssfr[np.isnan(ssfr) == True] = 0.0

    return ssfr, tbins


def calculate_ssfr_for_dataset(ds, hd):
    global z_start, z_end, nbins

    t_start = float(ds.cosmology.t_from_z(z_start).in_units('yr').value)
    t_end   = float(ds.cosmology.t_from_z(z_end).in_units('yr').value)


    ssfr = np.zeros((hd.num_halos, nbins))
    tbins = None

    start = time()    
    for i, halo in enumerate(hd.halos):
        ssfr[i], tbins = determine_halo_ssfr(ds, halo, t_start, t_end, tbins)
        
    
        if i > 20:
            elapsed = time() - start

            if yt.is_root(): 
                print(f"Calculation of star formation rates took {elapsed} seconds.")

            return ssfr[:20]
    # power law fit function with unit adjusting constant, k
    # horizontal offset, o
    # and power law slope, a
    # fit_func = lambda t, k1,a1,o1:  k1*(t-o1)**(-a1)
    # p, popt = curve_fit(fit_func, tbins[np.isnan(ssfr) == False], ssfr[np.isnan(ssfr) == False], p0=[1e-3,1,1e9])
    # ssfr_fit = lambda t: fit_func(t, p[0], p[1], p[2])


def main(ds_fname, hd_fname):
    if yt.is_root(): 
        print(f"Reading from {ds_fname}")
    ds = yt.load(ds_fname)
    ds.add_particle_filter('stars')

    hd = HaloData.load_from_file(hd_fname)
    hd = hd.filter_by(Fields.STR_MASS, greater_than, 1e9)

    if yt.is_root(): 
        print(f"Calculating ssfr for {hd.num_halos} halos")
    result = calculate_ssfr_for_dataset(ds, hd)
    if yt.is_root():
        print(result)

if __name__ == "__main__":
    ds_fname = sys.argv[1]
    hd_fname = sys.argv[2]


    main(ds_fname, hd_fname)
