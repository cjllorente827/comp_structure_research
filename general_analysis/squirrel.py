from universal import *
import yt
from yt.data_objects.particle_filters import add_particle_filter

from HaloData import Fields, HaloData

yt.funcs.mylog.setLevel(50)
yt.enable_parallelism()

IS_ROOT = yt.is_root()

add_particle_filter("stars", function=StarParticle, filtered_type='all', \
                    requires=["particle_type"])

def inspect_halo(ds, hd, zoom=3):
    sphere = to_YTRegion(ds, halo)

    fields = ['density', 'metallicity','temperature', ('deposit', 'stars_density')]
    p = yt.ProjectionPlot(ds, 'x', fields, sphere.center, data_source=sphere)
    
    frb = p.data_source.to_frb(2*sphere.radius/zoom, 1000)
    data = [None]*len(fields)
    for j,f in enumerate(fields):
        data[j] = np.array(frb[f])
    

    ##############################################################################
    # Special case pre-processing
    ##############################################################################
    
    # replaces the zeros with a very small value to make nice-looking plots
    star_density = np.array(frb[('deposit','stars_density')])
    star_density[star_density == 0.] = np.min(star_density)/100   
    data[3] = star_density[:]

    return data
        
def inspect_halos(ds, hd, output_fname):

    data = [None]*hd.num_halos
    for i,halo in enumerate(hd.halos):
        data[i] = inspect_halo(ds, halo)

    with open(output_fname, 'wb+') as f:
        pickle.dump(data, f)



    
if __name__ == '__main__':

    help_message = """
Usage: python squirrel.py <enzo_dataset> <halo_dataset> <output_filename> <analysis_type>
"""
    
    if len(sys.argv) != 5:
        print(help_message)
        sys.exit()
    
    enzo_fname    = str(sys.argv[1])
    halo_fname    = str(sys.argv[2])
    output_fname  = str(sys.argv[3])
    analysis_type = str(sys.argv[4])

    ds = yt.load(enzo_fname)
    ds.add_particle_filter('stars')

    hd = HaloData.load(halo_fname)
    hd = hd.filter_by(Fields.NUM_STAR_PARTICLES, greater_than, 10)\
           .filter_by(Fields.TOT_MASS, greater_than, 1e9)

    start = get_time()
    inspect_halos(ds, hd, output_fname)
    elapsed = get_time() - start

    ifprint(f"Squirrel completed its task in {elapsed} seconds.", IS_ROOT)

