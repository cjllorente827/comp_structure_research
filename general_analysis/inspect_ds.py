################################################################################
# This is an ad-hoc script to inspect whatever I might need to look at
# within a given dataset. 
################################################################################

import sys
import numpy as np
import pdb
HOME='/mnt/home/llorente/'
sys.path.append(HOME+'comp_structure_research/src')
sys.path.append(HOME+'comp_structure_research/stellar_mass_fraction')

import yt
yt.enable_parallelism()

from HaloData import *

ds = yt.load(f'{HOME}/cosmo_bigbox/25Mpc_512/RD0265/RD0265')

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


halo_dat_fname =\
    f"{HOME}/comp_structure_research/bigbox_25Mpc/halodata_RD0265.dat"

hd = HaloData.load_from_file(halo_dat_fname)\
             .filter_by(Fields.STR_MASS, greater_than, 1e11)


ds.add_particle_filter('stars')

domain = ds.domain_width.to('Mpc')
halo_data = hd.halos[0]
domain = ds.domain_width.to('Mpc').value
halo_data = hd.halos[0]
halo_pos = (halo_data[Fields.XPOS], halo_data[Fields.YPOS], halo_data[Fields.ZPOS])/domain
halo_rad = halo_data[Fields.RADIUS]/domain[0]
halo_sm = halo_data[Fields.STR_MASS]
halo_tm = halo_data[Fields.TOT_MASS]
halo = ds.sphere(halo_pos, halo_rad)

fields_to_save = [
    ("gas", "density"),
    ("stars", "particle_mass"),
    ("stars", "creation_time")
]

halo.save_as_dataset(filename="Single_halo_z0", fields=fields_to_save)

p = yt.ProjectionPlot(ds, "z", ("enzo", "Density"), data_source=halo)
p.set_center(halo_pos)
p.set_width(2*halo_rad)
p.save()

print(f"""
Halo position: {halo_pos} 
Halo rad: {halo_rad:2e}
Halo stellar mass: {halo_sm:2e}
Halo total mass: {halo_tm:2e}
""")





