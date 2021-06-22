import time

all_start = time.time()

import glob, os
import yt
import numpy as np
import sys
from yt.data_objects.particle_filters import add_particle_filter
yt.enable_parallelism()
yt.funcs.mylog.setLevel(50)

restart_snap = None  # filename of the first dataset in the restart
                     # (None for no restart; True to automatically find the output)
rockstar_base_cfg = """
OVERLAP_LENGTH = 0.1
FILE_FORMAT = ENZO
OUTPUT_FORMAT = BINARY
PARALLEL_IO = 1
FORK_READERS_FROM_WRITERS = 1
DELETE_BINARY_OUTPUT_AFTER_FINISHED = 0
FULL_PARTICLE_CHUNKS = 1
MIN_HALO_OUTPUT_SIZE = 100
MASS_DEFINITION = vir
"""

rockstar_cfg = "rockstar.cfg"
outbase = f"{os.getenv('APL_DATA_DIR')}/rockstar_halos"

# TODO: Figure out how to get this bullshit working across multiple nodes
#       in a parameterizable way
n_nodes = 1
n_procs = int(os.getenv('APL_NUM_PROCS'))
n_readers = n_procs

enzo_dir = os.getenv('APL_ENZO_DIR')

# Create file with parameter files, sorted by time.
pfs_file = f"{os.getenv('APL_DATA_DIR')}/pfs.dat"

if yt.is_root():
    print(f"""
    Running prep_rockstar.py with the following settings:
    Output directory : {outbase}
    Num procs : {n_procs}
    Enzo dir : {enzo_dir}
    pfs file : {pfs_file}
    """)
    


es = yt.simulation(os.getenv('APL_ENZO_DATA_FNAME'), "Enzo", find_outputs=True)
es.parameters['GlobalDir'] = enzo_dir
es._find_outputs()
files = [d["filename"] for d in es.all_outputs]

if yt.is_root():
    fp = open(pfs_file, "w")
    for i,f in enumerate(files):
        rel = f.replace(enzo_dir+'/', '')
        fp.write("%s\n" % (rel))
    fp.close()

    if not os.path.exists(outbase):
        os.mkdir(outbase)

    # Search for last analyzed output if restart_snap is True
    if restart_snap == True:
        last_rfile = None
        for f in reversed(files):
            dirname = f.split("/")[0]
            rfile = "%s/halos_%s.0.bin" % (outbase, dirname)
            if os.path.exists(rfile):
                if last_rfile == None:
                    raise RuntimeError("All datasets analyzed.  Not configuring.  "
                                   "Double-check if you think otherwise.")
                #end if
                print ("Starting with the first dataset without a rockstar halo file :: %s" \
                    % (last_rfile))
                restart_snap = last_rfile
                break
            #end if
            last_rfile = f
        #end for
    
        if last_rfile == None:
            print ("Cannot find any rockstar halo files.  Configuring to analyze everything.")
            restart_snap = None
        #end if
    #end if
    
    # Find the number of the restart snapshot
    if restart_snap == None:
        restart_num = 0
    else:
        if files.count(restart_snap) == 0:
            raise RuntimeError("restart snapshot %s not found" % (restart_snap))
        else:
            restart_num = files.index(restart_snap)
#end if is_root

# Find the finest proper resolution (use the last snapshot only)
start = time.time()
ds = yt.load(files[-1])
dx_min = ds.index.get_smallest_dx().in_units("Mpccm/h")
yt_load_time = time.time() - start

if yt.is_root():
    print(f"enzo dataset finished loading after {yt_load_time} seconds")


start = time.time()
    
def DarkMatter(pfilter, data):
    filter = data[("all", "particle_type")] == 1 # DM = 1, Stars = 2
    return filter
    
yt.add_particle_filter("dark_matter", function=DarkMatter, filtered_type='all', \
                    requires=["particle_type"])


ds.add_particle_filter('dark_matter')
ad = ds.all_data()
min_dm_mass = ad.quantities.extrema(('dark_matter','particle_mass'))[0]

if 4 in ad['particle_type']: # if the dataset contains must refine particles
    particle_type = 'must_refine'
    if yt.is_root():
        print("Searching for must refine particles")
else:
    particle_type = 'max_res_dark_matter'
    if yt.is_root():
        print("Searching for max resolution dark matter particles")
    
def MaxResDarkMatter(pfilter, data):
    return data["particle_mass"] <= 1.01 * min_dm_mass
    
add_particle_filter("max_res_dark_matter", function=MaxResDarkMatter, \
                    filtered_type='dark_matter', requires=["particle_mass"])
ds.add_particle_filter('max_res_dark_matter')

min_particle_mass = ad.quantities.extrema((particle_type,'particle_mass'))[0].in_units("Msun/h")
total_particles = ad.quantities.total_quantity((particle_type, "particle_ones"))

# Determine whether a zoom-in simulation
zoom_in = "StaticRefineRegionLevel[0]" in ds.parameters

# Assign cosmological parameters
h0 = ds.cosmology.hubble_constant.to('km/(Mpc*s)').value/100
Ol = ds.cosmology.omega_lambda
Om = ds.cosmology.omega_matter

# min_halo_size default value is 25 in the yt documentation
min_halo_output_size = 25

box_size = ds.domain_width[0].to("Mpccm/h")

dataset_read_time = time.time() - start

if yt.is_root():
    print(f"finished reading dataset after {dataset_read_time} seconds")
    print(f"""
Creating rockstar.cfg file with settings:
OUTBASE = {outbase}
FORCE_RES = {dx_min}
PARTICLE_MASS = {min_particle_mass}
SNAPSHOT_NAMES = {pfs_file}
    """)

    # Write rockstar config file
    fp = open(rockstar_cfg, "w")
    fp.write(rockstar_base_cfg)
    fp.write("\nOUTBASE = %s\n" % (outbase))
    fp.write("NUM_BLOCKS = %d\n" % (n_readers))
    fp.write("NUM_WRITERS = %d\n" % (n_procs))
    fp.write("FORK_PROCESSORS_PER_MACHINE = %d\n" % (n_procs/n_nodes))
    fp.write("SNAPSHOT_NAMES = %s\n" % (pfs_file))
    #fp.write("NUM_SNAPS = %d\n" % (len(files)))
    fp.write("STARTING_SNAP = %d\n" % (restart_num))
    fp.write("FORCE_RES = %g\n" % (dx_min))
    fp.write("PARTICLE_MASS = %g\n" % (min_particle_mass))
    fp.write("PERIODIC = %d\n" % (not zoom_in))
    fp.write("ENZO_ZOOMIN_RESTRICT = %d\n" % (zoom_in))
    fp.write("MIN_HALO_OUTPUT_SIZE = %d\n" % (min_halo_output_size))
    fp.write("h0 = %g\n" % (h0))
    fp.write("Ol = %g\n" % (Ol))
    fp.write("Om = %g\n" % (Om))
    fp.write("TOTAL_PARTICLES = %d\n" % (total_particles))
    fp.write("BOX_SIZE = %g\n" % (box_size))
    fp.close()

total_run_time = time.time() - all_start

if yt.is_root():
    print(f"""
prep_rockstar.py 
 -- total run time    : {total_run_time:.2f} seconds
 -- yt load time      : {yt_load_time:.2f} seconds
 -- dataset read time : {dataset_read_time:.2f} seconds
""")
