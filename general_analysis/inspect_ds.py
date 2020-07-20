################################################################################
# This is an ad-hoc script to inspect whatever I might need to look at
# within a given dataset. 
################################################################################

import sys
import numpy as np
HOME='/mnt/home/llorente/'
sys.path.append(HOME+'comp_structure_research')
sys.path.append(HOME+'comp_structure_research/stellar_mass_fraction')

import yt
yt.enable_parallelism()

from HaloData import *

ts = yt.load(f'{HOME}/cosmo_bigbox/25Mpc_512/RD????/RD????')


def DarkMatter(pfilter, data):
    filter = data[("all", "particle_type")] == 1 # DM = 1, Stars = 2
    return filter
    
yt.add_particle_filter("dark_matter", function=DarkMatter, filtered_type='all', \
                    requires=["particle_type"])

def stars(pfilter, data):
    filter = data[("all", "particle_type")] == 2 # DM = 1, Stars = 2
    return filter

yt.add_particle_filter("stars", function=stars, filtered_type='all', \
                       requires=["particle_type"])



def inspect_fields(ds):
    if yt.is_root():
        for f in ds.field_list:
            print(f)

        print()

        for df in ds.derived_field_list:
            print(df)
# end inspect_fields

halo_dat_fname =\
    f"{HOME}/comp_structure_research/stellar_mass_fraction/bigbox_25Mpc/halodata_RD0111.dat"

hd = HaloData.load_from_file(halo_dat_fname)\
             .filter_by(Fields.TOT_MASS, greater_than, 1e10)\
             .filter_by(Fields.NUM_STAR_PARTICLES, greater_than, 10)


for ds in ts:
    ds.add_particle_filter('stars')

    domain = ds.domain_width.to('Mpc')
    halo_data = hd.halos[0]
    halo_pos = (halo_data[Fields.XPOS], halo_data[Fields.YPOS], halo_data[Fields.ZPOS])
    halo_rad = halo_data[Fields.RADIUS]
    halo = ds.sphere(halo_pos, halo_rad)


    print(ds.fields.stars.metallicity_fraction)
    break


