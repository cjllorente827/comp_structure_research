import sys
from time import time
import yt
from yt.extensions.astro_analysis.halo_analysis.api import HaloCatalog
from yt.data_objects.particle_filters import add_particle_filter
from yt.extensions.astro_analysis.halo_finding.rockstar.api import RockstarHaloFinder
yt.enable_parallelism()

def StarParticle(pfilter, data):
    filter = data[("all", "particle_type")] == 2 # DM = 1, Stars = 2
    return filter

add_particle_filter("stars", function=StarParticle, filtered_type='all', \
                       requires=["particle_type"])

def DarkMatter(pfilter, data):
    filter = data[("all", "particle_type")] == 1 # DM = 1, Stars = 2
    return filter
    
add_particle_filter("dark_matter", function=DarkMatter, filtered_type='all', \
                    requires=["particle_type"])

def MustRefineDarkMatter(pfilter, data):
    filter = data[("all", "particle_type")] == 4 # Must Refine Particle type
    return filter
    
add_particle_filter("must_refine", function=MustRefineDarkMatter, filtered_type='all', \
                    requires=["particle_type"])


def run_rockstar(fname):
    assert(yt.communication_system.communicators[-1].size >= 3)

    ds = yt.load(fname)
    ds.add_particle_filter('stars')
    ds.add_particle_filter('dark_matter')
    ds.add_particle_filter('must_refine')
    ad = ds.all_data()
    min_dm_mass = ad.quantities.extrema(('dark_matter','particle_mass'))[0]

    if 4 in ad['particle_type']: # if the dataset contains must refine particles
        particle_type = 'must_refine'
        print("Searching for must refine particles")
    else:
        particle_type = 'max_res_dark_matter'
        print("Searching for max resolution dark matter particles")
    
    def MaxResDarkMatter(pfilter, data):
        return data["particle_mass"] <= 1.01 * min_dm_mass
    
    add_particle_filter("max_res_dark_matter", function=MaxResDarkMatter, \
                        filtered_type='dark_matter', requires=["particle_mass"])
    ds.add_particle_filter('max_res_dark_matter')
    
    hc = HaloCatalog(data_ds=ds, finder_method='rockstar', \
                     finder_kwargs={'particle_type':particle_type})

    hc.create()

def run_hop(fname):

    ds = yt.load(fname)
    ds.add_particle_filter('stars')
    ds.add_particle_filter('dark_matter')    
    
    hc = HaloCatalog(data_ds=ds, finder_method='hop')

    hc.create()

if __name__ == "__main__":
    fname = sys.argv[1]

    start = time()
    run_rockstar(fname)
    elapsed = time() - start
    print(f"run_rockstar.py took {elapsed} seconds to run using rockstar")

    # start = time()
    # run_hop(fname)
    # elapsed = time() - start
    # print(f"run_rockstar.py took {elapsed} seconds to run using hop")
