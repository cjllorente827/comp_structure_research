###############################################################################
# The purpose of this object is to generate measurements of certain properties
# of halos at a set of given redshifts. It will then output the values it 
# gathers to a binary output file (using pickle) that can be then easily be
# read back in and used to make plots/generate derived quantities. 
###############################################################################

import sys

sys.path.append('/mnt/home/llorente/comp_structure_research')

import pymp
NUM_THREADS = pymp.config.num_threads[0]

import yt
yt.funcs.mylog.setLevel(50)

import pickle


def stars(pfilter, data):
    filter = data[("all", "particle_type")] == 2 # DM = 1, Stars = 2
    return filter

yt.add_particle_filter("stars", function=stars, filtered_type='all', \
                       requires=["particle_type"])

from time import time
import numpy as np
from HaloData import *

import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

# linear fit function
lin_func = lambda x, m,b: m*x + b
nparams = 2
nbins   = 1000

########################################################################
# Takes in a dataset and a halo and returns an array containing 
# specific star formation rate as well as a least squares fit 
# to a power law for the sSFR. Returns the time bins and cumulative 
# stellar mass function as well
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
    ssfr = np.array([sfr[i]/csm[i] if csm[i] > 0 else 0. for i in range(len(sfr))])
    
    # enforce a minimum ssfr
    # allows log plotting, ignored by fits
    ssfr_floor = 1e-13
    ssfr[ssfr < ssfr_floor] = ssfr_floor

    # do curve fits ignoring the time periods before there were any stars
    guess = np.array([1,-1])
    
    # cuts out the times before stars appear
    tbins_fit = tbins[csm>0]
    ssfr_fit = ssfr[csm>0]

    # ignores data points with the ssfr floor
    tbins_fit = tbins[ssfr > 1e-13]
    ssfr_fit = ssfr[ssfr > 1e-13]
    
    try : 
        p, popt = curve_fit(lin_func,
                            np.log10(tbins_fit),
                            np.log10(ssfr_fit),
                            p0=guess)
    except :
        rows = 1
        cols = 1
        fig, axes = plt.subplots(rows,cols,figsize=(18*cols,7*rows))

        print(f"Failed to fit halo {halo[Fields.HALO_ID]} with mass {halo[Fields.STR_MASS]:.1e}")
        p = np.array([np.nan]*nparams)

        # text_xoffset = 0.05
        # text_yoffset = np.nanmin(ssfr)
        # for z in range(5):
        #     t = float(ds.cosmology.t_from_z(z).in_units('Gyr').value)
        #     axes.axvline(t, linestyle='dashed', c='k')
        #     axes.text(t+text_xoffset,text_yoffset, f"z={z}" )

        # axes.loglog(time/1e9, ssfr, c='b', linewidth=0, marker='o')
        # axes.set_xlabel('Time (Gyr)')
        # axes.set_ylabel('sSFR  [yr$^{-1}$]')
        # axes.set_title(f'sSFR for halo with M={halo[Fields.STR_MASS]:.1e} $M_\odot$')
    
        # plt.show()

        
    return ssfr, p, tbins, csm

def calculate_ssfr_for_dataset(ds, hd, z_start, z_end):
    global nbins, nparams

    t_start = float(ds.cosmology.t_from_z(z_start).in_units('yr').value)
    t_end   = float(ds.cosmology.t_from_z(z_end).in_units('yr').value)

    print(f"Time range starting at {t_start:.1e} years.")
    print(f"Time range ending at {t_end:.1e} years.")

    #nhalos = 40 # for testing purposes
    nhalos = hd.num_halos # for actually running the code
    
    ssfr = pymp.shared.array((nhalos, nbins))
    ssfr_fit = pymp.shared.array((nhalos, nparams))
    csm = pymp.shared.array((nhalos, nbins))

    tbins = None

    ###########################################################
    # Run in serial (for debugging)
    ###########################################################
    # for i in range(nhalos):
    #     halo = hd.halos[i]
    #     ssfr[i], ssfr_fit[i], tbins, csm[i] = \
    #             determine_halo_ssfr(ds, halo, t_start, t_end, tbins)
    
    ###########################################################
    # Run in parallel (for go fast)
    ###########################################################
    with pymp.Parallel(NUM_THREADS) as p:
        for i in p.xrange(nhalos):
            halo = hd.halos[i]
            ssfr[i], ssfr_fit[i], tbins, csm[i] = \
                determine_halo_ssfr(ds, halo, t_start, t_end, tbins)
            # print(f"Thread {p.thread_num} processing halo {i}")
            # print(ssfr[i])
    # end parallel section

    # remove any halos that failed to achieve fits
    idx_removal = np.array([not x for x in np.isnan(ssfr_fit[:,0])])
    ssfr = ssfr[idx_removal]
    ssfr_fit = ssfr_fit[idx_removal]
    csm = csm[idx_removal]

    print(f"Calculated ssfr fits for {len(ssfr)} halos out of {nhalos}. \
    ({int(100*len(ssfr)/nhalos)}%)")

    return ssfr, ssfr_fit, tbins, csm

def z_to_t(ds, z):
    return float(ds.cosmology.t_from_z(z).in_units('yr').value)

def sample_fit_at_z(ds, fits, redshifts):

    nhalos = len(fits)
    nz = len(redshifts)
    samples = np.zeros((nhalos, nz))
    for i,p in enumerate(fits):
        fit_func = lambda t: 10**lin_func(np.log10(t), p[0], p[1])
        for j,z in enumerate(redshifts):
            t = z_to_t(ds, z)
            samples[i,j] = fit_func(t)
    return samples

def sample_at_z(ds, values, times, redshifts):
    
    nhalos = len(values)
    nz = len(redshifts)
    nbins = len(times)
    samples = np.zeros((nhalos, nz))
    for i,val in enumerate(values):
        for j,z in enumerate(redshifts):
            t = z_to_t(ds, z)
            min_index = np.argmin( np.abs(times - t) )

            avg_val = 0.
            # average of the three points nearest the desired redshift
            if min_index > 0 and min_index < nbins-1:
                avg_val = np.mean(val[min_index-1:min_index+2])
            # handle edge cases (literally)
            # averages two points instead of three
            elif min_index == 0:
                avg_val = np.mean(val[0:2])
            elif min_index == nbins-1:
                avg_val = np.mean(val[nbins-2:nbins])
            else:
                print(f"Something went wrong: min_index = {min_index}")
                sys.exit()

            samples[i,j] = avg_val
    return samples


####################################################################
# Builds out a history of certain properties for halos defined
# at z = 0. Outputs itself to file as a binary pickle object that
# can easily be read back in and used to make plots.
####################################################################
class HaloHistory:

    nhalos = 0
    ds_fname = ''
    hd_fname = ''
    ssfr = None # specific star formation rates per halo per redshift
    ssfr_fit = None
    tbins = None
    csm = None # cumulative stellar mass per halo per redshift
    redshifts = None

    # properties sampled at specific redshifts for comparison to observation
    ssfr_fit_at_z = None
    csm_at_z = None

    ##############################################################
    # Takes in an enzo dataset filename, a halo dataset filename, and a list of 
    # redshifts to take datapoints for.
    ##############################################################
    def __init__(self, ds_fname, hd_fname, redshifts):

        all_start = time()
        self.ds_fname = ds_fname
        self.hd_fname = hd_fname

        print(f"Reading from {hd_fname}")
        start = time()
        # TODO: consider implementing a more generic way to filter this
        hd = HaloData.load_from_file(hd_fname)\
                          .filter_by(Fields.STR_MASS, greater_than, 1e9)
        hd_load_time = time() - start


        self.redshifts = redshifts
        print(f"Reading from {ds_fname}")

        start = time()     
        ds = yt.load(ds_fname)
        ds.add_particle_filter('stars')
        ds_load_time = time() - start

        start = time()     
        self.ssfr, self.ssfr_fit, self.tbins, self.csm = \
            calculate_ssfr_for_dataset(ds, hd, \
                                       np.max(self.redshifts),\
                                       np.min(self.redshifts))
        self.nhalos = np.shape(self.ssfr)[0]
        ssfr_fit_time = time() - start

        start = time()
        self.ssfr_at_z = sample_fit_at_z(ds, self.ssfr_fit, self.redshifts)
        self.csm_at_z = sample_at_z(ds, self.csm, self.tbins, self.redshifts)
        sample_time = time() - start

        total_time = time() - all_start
        print(f"Total time to run: {total_time:.1f} s")
        print(f"HaloData load: {ds_load_time:.1f} s ({100*hd_load_time/total_time:.1f}% of total)")
        print(f"Enzo dataset load: {ds_load_time:.1f} s ({100*ds_load_time/total_time:.1f}% of total)")
        print(f"Calculation of ssfr: {ssfr_fit_time} s ({100*ssfr_fit_time/total_time:.1f}% of total)")
        print(f"Redshift sampling: {sample_time} s ({100*sample_time/total_time:.1f}% of total)")

    def dump(self, fname):
        with open(fname, 'wb') as f:
            pickle.dump(self, f)


def load_history(fname):
    with open(fname, 'rb') as f:
        hist = pickle.load(f)
    return hist



