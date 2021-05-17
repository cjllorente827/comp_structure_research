import yt
from HaloData import *
HOME='/mnt/home/llorente/'
sys.path.append(HOME+'comp_structure_research/src')

ds = yt.load(f'/mnt/home/llorente/cosmo_bigbox/25Mpc_512/RD0265/RD0265')
halo_dat_fname =\
    f"{HOME}/comp_structure_research/bigbox_25Mpc/halodata_RD0265.dat"

hd = HaloData.load_from_file(halo_dat_fname)\
             .filter_by(Fields.STR_MASS, greater_than, 1e11)


ds.add_particle_filter('stars')

domain = ds.domain_width.to('Mpc').value
halo_data = hd.halos[0]
halo_pos = (halo_data[Fields.XPOS], halo_data[Fields.YPOS], halo_data[Fields.ZPOS])/domain
halo_rad = halo_data[Fields.RADIUS]/domain[0]

halo = ds.sphere(halo_pos, halo_rad)

p = yt.ProjectionPlot(ds, "z", ("enzo", "Density"), data_source=halo)
p.save()
