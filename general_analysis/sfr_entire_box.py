
import sys
from time import time
import numpy as np
import matplotlib.pyplot as plt
import yt
import pickle
import pdb

from yt.utilities.parallel_tools.parallel_analysis_interface import parallel_objects
yt.funcs.mylog.setLevel(50)
yt.enable_parallelism()

ZSTART = 8.
ZEND = 0.
NBINS   = 500

@yt.particle_filter(name="stars", filtered_type='all',requires=["particle_type"])
def stars(pfilter, data):
    return data[(pfilter.filtered_type, "particle_type")] == 2 # DM = 1, Stars = 2


def starFormationRate(field, data):
    masses = data[('stars', 'particle_mass')]
    formation_time = data[('stars', 'creation_time')]

    t_start = float(data.ds.cosmology.t_from_z(8.).in_units('yr').value)
    t_end   = float(data.ds.cosmology.t_from_z(0.).in_units('yr').value)

    time_range = [t_start, t_end]
    
    hist, bins = np.histogram(formation_time, bins=NBINS, range=time_range)
    inds = np.digitize(formation_time, bins=bins)
    tbins = (bins[:-1] + bins[1:])/2
    
    # star formation rate
    sfr = np.array([masses[inds == j+1].sum()/(bins[j+1]-bins[j]) for j in range(len(tbins))])

    return sfr, tbins



def plot_result(sfr, tbins):

    row, col = 1,1
    fig, ax = plt.subplots(row,col, figsize=(8*col,7*row))  
    ax.plot(tbins,sfr)
    ax.set(
        title='Star formation rate for entire 25 Mpc box',
        xlabel=r"$t$ (yr)",
        ylabel=r"SFR $(M_{\odot})$/yr")

    plt.show()
    #fig.savefig('SFR_25Mpc.png')
    plt.close()

ds_fname = sys.argv[1]

    
print(f"Calculating SFR for {ds_fname}")
start = time()     
ds = yt.load(ds_fname)
ds.add_particle_filter('stars')
ds.add_field(("stars", "sfr"), function=starFormationRate, units='Msun/yr', sampling_type='cell', particle_type=True)
for fd in ds.derived_field_list:
    print(fd)
#ad = ds.all_data()
ad = ds.r[1e-4,1e-4,1e-4]
ds_load_time = time() - start

print(f"Dataset loaded after {ds_load_time} seconds")

start = time()
smass = ad[("stars", "particle_mass")]
print(smass)
sfr, tbins = ad[("stars", "sfr")]
sfr_time = time() - start

print(f"Calculation of SFR completed in {sfr_time} seconds")

    
plot_result(sfr, tbins)
#np.savetxt("SFR_25Mpc.dat")    

    
