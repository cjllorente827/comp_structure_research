import os
from universal import *

import argparse
parser = argparse.ArgumentParser()

parser.add_argument('enzo_dataset', type=str, \
                    help="Name of the enzo dataset")
parser.add_argument('halo_dataset', type=str, \
                    help="Name of the halo dataset")
parser.add_argument('-o', '--output_dir', type=str, \
                    help="Directory where output files should be saved")
args = parser.parse_args()


import yt
from yt.data_objects.particle_filters import add_particle_filter

from HaloData import Fields, HaloData, to_YTRegion

yt.funcs.mylog.setLevel(50)
yt.enable_parallelism()

from yt.utilities.parallel_tools.parallel_analysis_interface \
    import communication_system

NUM_PROCS = communication_system.communicators[-1].size

IS_ROOT = yt.is_root()

add_particle_filter("stars", function=StarParticle, filtered_type='all', \
                    requires=["particle_type"])

extracted_fields = ['density', 'metallicity','temperature', ('deposit', 'stars_density')]

                    
       
def inspect_halos(ds, hd, output_dir=None):
    global extracted_fields

    # by default output to a data directory
    if output_dir is None:
        output_dir = os.path.join('data', str(ds))

    for halo in yt.parallel_objects(hd.halos, NUM_PROCS): 
        sphere = to_YTRegion(ds, halo)
        fname = os.path.join(output_dir, f'{str(ds)}_halo_{int(halo[Fields.HALO_ID])}')
        sphere.save_as_dataset(fname, fields=extracted_fields)
        

if __name__ == '__main__':
    
    # TODO: Possibly work on making this not have to run on every processor
    #       when running in parallel

    enzo_fname = args.enzo_dataset
    halo_fname = args.halo_dataset
    output_dir = args.output_dir
    
    ################################
    # Load datasets into memory
    ################################
    start = get_time()
    ds = yt.load(enzo_fname)
    ds.add_particle_filter('stars')
    enzo_time = get_time() - start

    yt.only_on_root(print, f"Enzo dataset loaded")

    # Filter for large halos

    
    start = get_time()
    hd = HaloData.load(halo_fname)
    hd = hd.filter_by(Fields.NUM_STAR_PARTICLES, greater_than, 10)\
           .filter_by(Fields.TOT_MASS, greater_than, 1e11)
    halo_time = get_time() - start

    yt.only_on_root(print, f"Halo dataset loaded")

    ################################
    # Extract relevant fields for each halo
    # Save to files
    ################################
    start = get_time()
    if output_dir is not None:
        inspect_halos(ds, hd, output_dir)
    else:
        inspect_halos(ds, hd)
    inspect_time = get_time() - start

    yt.only_on_root(print, f"Enzo dataset load took {enzo_time} seconds")
    yt.only_on_root(print, f"Halo dataset load took {halo_time} seconds")
    yt.only_on_root(print, f"Halo inspection took {inspect_time} seconds")
    yt.only_on_root(print, f"Processing complete for {hd.num_halos} halos on {NUM_PROCS} cores")
