import sys
HOME='/mnt/home/llorente'
#HOME='/home/cj/'
sys.path.append(f'{HOME}/comp_structure_research')
sys.path.append(f'{HOME}/comp_structure_research/stellar_mass_fraction')


RD_out = sys.argv[1]

import numpy as np
import yt
yt.enable_parallelism()

from HaloData import *

dataset_fname  = f"{HOME}/cosmo_bigbox/25Mpc_512/{RD_out}/{RD_out}"
halo_dat_fname = f"halodata_{RD_out}.dat"
hd = HaloData.load_from_file(halo_dat_fname)

hd = hd.filter_by(Fields.NUM_STAR_PARTICLES, greater_than, 10).filter_by(Fields.TOT_MASS, greater_than, 1e10)

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

ds = yt.load(dataset_fname)
ds.add_particle_filter('stars')
ds.add_particle_filter('dark_matter')
ad = ds.all_data()
(ad.right_edge-ad.left_edge).to('Mpc')

domain = ds.domain_width.to('Mpc').value[0]
large_box = 0.50*domain
mid_box = 0.20*domain
small_box = 0.10*domain

c = np.array([0.5,0.5,0.5])

large_left = c - np.ones(3)*large_box/2
large_right = c + np.ones(3)*large_box/2
large_region = ds.box(large_left, large_right)

mid_left = c - np.ones(3)*mid_box/2
mid_right = c + np.ones(3)*mid_box/2
mid_region = ds.box(mid_left, mid_right)

small_left = c - np.ones(3)*small_box/2
small_right = c + np.ones(3)*small_box/2
small_region = ds.box(small_left, small_right)

large_p = yt.ProjectionPlot(ds,'x','metallicity', weight_field='density', center=c, width=(large_box,'Mpc'), data_source=large_region)

for i in range(0, hd.num_halos):
    halo = hd.halos[i]
    hpos = np.array((halo[Fields.XPOS], halo[Fields.YPOS], halo[Fields.ZPOS]))/domain
    if hpos[0] >= large_left[0] and hpos[0] < large_right[0]:
        large_p.annotate_sphere(hpos, radius=(halo[Fields.RADIUS],'Mpc'))

large_p.set_cmap('metallicity', cmap='dusk')
large_p.save("imgs/large_region")

del large_p

mid_p = yt.ProjectionPlot(ds,'x','metallicity', weight_field='density', center=c, width=(mid_box,'Mpc'), data_source=mid_region)

for i in range(0, hd.num_halos):
    halo = hd.halos[i]
    hpos = np.array((halo[Fields.XPOS], halo[Fields.YPOS], halo[Fields.ZPOS]))/domain
    if hpos[0] >= mid_left[0] and hpos[0] < mid_right[0]:
        mid_p.annotate_sphere(hpos, radius=(halo[Fields.RADIUS],'Mpc'))

mid_p.set_cmap('metallicity', cmap='dusk')
mid_p.save("imgs/medium_region")

del mid_p

small_p = yt.ProjectionPlot(ds,'x','metallicity', weight_field='density', center=c, width=(small_box,'Mpc'), data_source=small_region)

for i in range(0, hd.num_halos):
    halo = hd.halos[i]
    hpos = np.array((halo[Fields.XPOS], halo[Fields.YPOS], halo[Fields.ZPOS]))/domain
    if hpos[0] >= small_left[0] and hpos[0] < small_right[0]:
        small_p.annotate_sphere(hpos, radius=(halo[Fields.RADIUS],'Mpc'))

small_p.set_cmap('metallicity', cmap='dusk')
small_p.save("imgs/small_region")

del small_p
