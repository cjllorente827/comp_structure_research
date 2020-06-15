import sys

argc = len(sys.argv)

if argc != 4:
    print("""
Usage: python extract_halo_data.py <enzo_output> <rockstar_catalog/halos_0.0.bin> <output_filename>
""")
    exit()


import yt

from tqdm import tqdm
from time import time
from collections import OrderedDict
from yt.extensions.astro_analysis.halo_analysis.api import HaloCatalog
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import pymp
NUM_THREADS = pymp.config.num_threads[0]
from HaloData import HaloData, Fields
import numpy as np

def stars(pfilter, data):
    filter = data[("all", "particle_type")] == 2 # DM = 1, Stars = 2
    return filter

yt.add_particle_filter("stars", function=stars, filtered_type='all', \
                       requires=["particle_type"])

def extract_data_to_dat_file(hc, ds, outfile):

    num_halos = len(hc.catalog)
    halos = pymp.shared.array( (num_halos,Fields.NUM_FIELDS) )
    print("Parsing halo catalogs.....")
    with pymp.Parallel(NUM_THREADS) as p:
        for i in p.xrange(num_halos-1,-1,-1):
            # print(f"Thread {p.thread_num} working on Halo {i}")
            halo = hc.catalog[i]
            halo_pos = (
                halo['particle_position_x'],
                halo['particle_position_y'],
                halo['particle_position_z']
            )

            radius = halo['virial_radius'].in_units('kpc')
            sphere = ds.sphere(halo_pos, radius)
            totals = sphere.quantities.total_mass().in_units('Msun').value
            stellar_mass = sphere[('stars', 'particle_mass')].sum().in_units('Msun').value
            num_star_particles = len(sphere[('stars', 'particle_mass')])

            omega_b = 0.0486
            omega_c = 0.2589
            omega_m = omega_b + omega_c
            baryonic_mass_fraction = omega_b / omega_m
    
            gas_mass = totals[0]
            total_mass = np.sum(totals)
            dm_mass = total_mass - gas_mass - stellar_mass
            baryon_mass = gas_mass + stellar_mass
            if total_mass == 0.:
                str_mass_fraction = 0.
            else:
                str_mass_fraction = stellar_mass / baryonic_mass_fraction / total_mass

            halos[i,Fields.HALO_ID] = halo['particle_identifier']
            halos[i,Fields.RADIUS] = radius.value
            halos[i,Fields.XPOS] = halo_pos[0].in_units('Mpc')
            halos[i,Fields.YPOS] = halo_pos[1].in_units('Mpc')
            halos[i,Fields.ZPOS] = halo_pos[2].in_units('Mpc')
            halos[i,Fields.STR_MASS] = stellar_mass
            halos[i,Fields.GAS_MASS] = gas_mass
            halos[i,Fields.BAR_MASS] = baryon_mass
            halos[i,Fields.DM_MASS] = dm_mass
            halos[i,Fields.STR_MASS_FRAC] = str_mass_fraction
            halos[i,Fields.TOT_MASS] = total_mass
            halos[i,Fields.NUM_STAR_PARTICLES] = num_star_particles
            # print(f"    Thread {p.thread_num} finished Halo {i}")
    print("All halos parsed.")
    return HaloData(num_halos, halos)


def main(enzo_in, rockstar_in, outfile):
        print(f"Reading from {enzo_in}")
        ds = yt.load(enzo_in)
        ds.add_particle_filter('stars')
        hds = yt.load(rockstar_in)

        hc = HaloCatalog(data_ds=ds, halos_ds=hds)
        hc.load()

        start_time = time()
        hd = extract_data_to_dat_file(hc, ds, outfile)
        elapsed = time() - start_time
        print(f"Halo data extraction took {elapsed} seconds on {NUM_THREADS} threads")
        hd.save_to_file(outfile)
        #annotate_halos(hc, ds)

if __name__ == "__main__":

    
    enzo_in     = sys.argv[1]
    rockstar_in = sys.argv[2]
    outfile     = sys.argv[3]

    main(enzo_in, rockstar_in, outfile)

    
