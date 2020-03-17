import sys
import yt
from yt.extensions.astro_analysis.halo_analysis.api import HaloCatalog
from yt.data_objects.particle_filters import add_particle_filter
from yt.extensions.astro_analysis.halo_finding.rockstar.api import RockstarHaloFinder
yt.enable_parallelism()

def stars(pfilter, data):
    filter = data[("all", "particle_type")] == 2 # DM = 1, Stars = 2
    return filter

yt.add_particle_filter("stars", function=stars, filtered_type='all', \
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


def run_rockstar(fname, particle_type='must_refine'):
    assert(yt.communication_system.communicators[-1].size >= 3)

    ds = yt.load(fname)
    ds.add_particle_filter('stars')
    ds.add_particle_filter('dark_matter')
    ds.add_particle_filter('must_refine')
    ad = ds.all_data()
    min_dm_mass = ad.quantities.extrema(('dark_matter','particle_mass'))[0]
    
    def MaxResDarkMatter(pfilter, data):
        return data["particle_mass"] <= 1.01 * min_dm_mass
    
    add_particle_filter("max_res_dark_matter", function=MaxResDarkMatter, \
                        filtered_type='dark_matter', requires=["particle_mass"])
    ds.add_particle_filter('max_res_dark_matter')
    
    hc = HaloCatalog(data_ds=ds, finder_method='rockstar', \
                     finder_kwargs={'particle_type':particle_type})

    hc.create()

if __name__ == "__main__":
    fname = sys.argv[1]
    run_rockstar(fname)
