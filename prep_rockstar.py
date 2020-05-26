import glob, os
import yt
import numpy as np
import sys

restart_snap = None  # filename of the first dataset in the restart
                     # (None for no restart; True to automatically find the output)
rockstar_base_cfg = "rockstar_base.cfg"
rockstar_cfg = "rockstar.cfg"
outbase = "rockstar_halos"
n_nodes = 1
n_procs = 8
n_readers = 8

# Create file with parameter files, sorted by time.
filename = "pfs.dat"
es = yt.simulation(sys.argv[1], "Enzo", find_outputs=True)
es.parameters['GlobalDir'] = '/mnt/home/llorente/cosmo_bigbox/25Mpc_512'
es._find_outputs()
files = [d["filename"] for d in es.all_outputs]
fp = open(filename, "w")
for i,f in enumerate(files):
    fp.write("%s\n" % (f))
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
            print ("Starting with the first dataset without a rockstar halo file :: %s" \
                % (last_rfile))
            restart_snap = last_rfile
            break
        last_rfile = f
    if last_rfile == None:
        print ("Cannot find any rockstar halo files.  Configuring to analyze everything.")
        restart_snap = None
    
# Find the number of the restart snapshot
if restart_snap == None:
    restart_num = 0
else:
    if files.count(restart_snap) == 0:
        raise RuntimeError("restart snapshot %s not found" % (restart_snap))
    else:
        restart_num = files.index(restart_snap)

# Find the finest proper resolution (use the last snapshot only)
ds = yt.load(files[-1])
dx_min = 0 # ds.index.get_smallest_dx().in_units("Mpccm/h")

# Determine whether a zoom-in simulation
zoom_in = "StaticRefineRegionLevel[0]" in ds.parameters

# Write rockstar config file
lines = open(rockstar_base_cfg, "r").readlines()
fp = open(rockstar_cfg, "w")
for l in lines:
    fp.write(l)
fp.write("OUTBASE = %s\n" % (outbase))
fp.write("NUM_BLOCKS = %d\n" % (n_readers))
fp.write("NUM_WRITERS = %d\n" % (n_procs))
fp.write("FORK_PROCESSORS_PER_MACHINE = %d\n" % (n_procs/n_nodes))
fp.write("SNAPSHOT_NAMES = %s\n" % (filename))
#fp.write("NUM_SNAPS = %d\n" % (len(files)))
fp.write("STARTING_SNAP = %d\n" % (restart_num))
fp.write("FORCE_RES = %g\n" % (dx_min))
fp.write("PERIODIC = %d\n" % (not zoom_in))
fp.write("ENZO_ZOOMIN_RESTRICT = %d\n" % (zoom_in))
fp.close()
