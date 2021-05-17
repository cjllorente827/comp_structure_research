# temp file to ease creation of plots until something more permanent can be written

import sys
HOME='/mnt/home/llorente/'
#HOME='/home/cj/'
sys.path.append(HOME+'comp_structure_research')
sys.path.append(HOME+'comp_structure_research/src')
sys.path.append(HOME+'comp_structure_research/general_analysis')
sys.path.append(HOME+'comp_structure_research/star_formation_rate')
sys.path.append(HOME+'comp_structure_research/stellar_mass_fraction')
DATA_DIR = HOME+'comp_structure_research/bigbox_25Mpc'

from HaloData import *
from general_analysis_plots import *


hdfile_z_2 = DATA_DIR+"/halodata_RD0111.dat" # z = 2.00
hdfile_z_1 = DATA_DIR+"/halodata_RD0166.dat" # z = 1.00
hdfile_z_0 = DATA_DIR+"/halodata_RD0265.dat" # z = 0.00

hd_z_2 = HaloData.load_from_file(hdfile_z_2)\
                    .filter_by(Fields.STR_MASS, greater_than, 1e9)\
                    .filter_by(Fields.NUM_STAR_PARTICLES, greater_than, 10)
hd_z_1 = HaloData.load_from_file(hdfile_z_1)\
                    .filter_by(Fields.STR_MASS, greater_than, 1e9)\
                    .filter_by(Fields.NUM_STAR_PARTICLES, greater_than, 10)
hd_z_0 = HaloData.load_from_file(hdfile_z_0)\
                    .filter_by(Fields.STR_MASS, greater_than, 1e9)\
                    .filter_by(Fields.NUM_STAR_PARTICLES, greater_than, 10)

hd_list = [hd_z_0, hd_z_1,hd_z_2]
z_list = [0., 1., 2.]

metallicity_vs_stellar_mass(hd_list, z_list)
