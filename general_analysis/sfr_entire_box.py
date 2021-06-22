import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 14})
import numpy as np
import h5py
import sys, os, re
from time import time
from tqdm import tqdm

if len(sys.argv) != 4:
    print("""
Usage: python sfr_entire_box.py <dataset_filename> <z start> <z end>
""")

    sys.exit()
#end if

# importing this down here cuz yt takes forever to fucking load
import yt
yt.funcs.mylog.setLevel(50)

ds_fname = str(sys.argv[1])
zstart   = float(sys.argv[2])
zend     = float(sys.argv[3])
#nbins    = int(sys.argv[4])

ds = yt.load(ds_fname)

# calculating dm particle mass
omega_dm = float(ds.get_parameter('CosmologyOmegaDarkMatterNow'))
H_0 = ds.cosmology.hubble_constant
G = yt.units.G
rho_c = 3 * H_0**2 / 8 / np.pi / G
L_box = ds.domain_width[0]
N_root = ds.get_parameter('TopGridDimensions')[0]

mass_dm = (omega_dm * rho_c * (L_box / N_root)**3 ).to('Msun').value
time_conversion_factor = ds.time_unit.to('yr').value

Madau_fit = lambda z : 0.015 * (1+z)**2.7 / (1 + ((1+z)/2.9)**5.6) # Msun / yr / Mpc**3
    
t_start = float(ds.cosmology.t_from_z(zstart).in_units('yr').value)
t_end   = float(ds.cosmology.t_from_z(zend).in_units('yr').value)

nfiles = 1024

bin_counts = [25, 50, 100, 250]

def main():

    all_data = {}
    ngrids, nwodm = 0, 0

    start = time()

    all_files = getCPUFiles(ds_fname)

    for cpu_fname in tqdm(all_files):
            
        f = h5py.File(cpu_fname, 'r')

        # all_data is modified in place
        counts = processFile(f, all_data)
        ngrids += counts[0]
        nwodm  += counts[1]
    # end for i
    elapsed = time() - start

    print(f"""
Operation took: {elapsed} seconds
Processed {ngrids} total grids
{nwodm} had stars but no dark matter
Edge case rate at: {nwodm/ngrids * 100} %
Largest DM particle : {all_data[25]["max_dm"]}
""")

    plotResult(all_data)
# end main

def getCPUFiles(fname, limit=None):

    dir = os.path.dirname(fname)
    ls = os.listdir(dir)

    paths = []

    for name in ls:
        match = re.search("RD[0-9]{4}.cpu[0-9]{4}", name)
        if match:
            paths.append(os.path.join(dir, name) )

        if limit is not None and len(paths) >= limit:
            return paths
            
    return paths


def processFile(f, all_data):
    
    ngrids, nwodm = 0, 0
    for key in list(f.keys()):

        # dont bother reading the Metadata
        if key == 'Metadata': continue

        ngrids += 1

        grid = f[key]
        fields = list(grid.keys())

        # if particle_type is not available, then there are no particles
        # (star or otherwise) in this grid
        if "particle_type" not in fields: continue
        
        particle_types = np.array(grid["particle_type"])

        # create boolean arrays index star particles and dark matter particles
        dm_only = particle_types == 1
        stars_only = particle_types == 2

        nstars = len(particle_types[stars_only])


        # if no stars, then what are we even doing here?
        if nstars == 0: continue

        # figure out if we have dark matter
        ndm = len(particle_types[dm_only])
        if ndm == 0:
            nwodm += 1
            continue

        all_particle_densities = np.array(grid["particle_mass"])
        # grab the dm particle density
        rho_dm = all_particle_densities[dm_only][0]

        mass_conversion_factor = mass_dm / rho_dm

        # grab the data and handle unit conversions
        particle_masses = all_particle_densities[stars_only]*mass_conversion_factor
        creation_times = np.array(grid["creation_time"])[stars_only]*time_conversion_factor

        
        # create data lines for multiple bin counts
        for nbins in bin_counts:

            if nbins not in all_data.keys():
                sfr, tbins = calcStarFormationRate(
                    particle_masses, creation_times, t_start, t_end, nbins
                )
                all_data[nbins] = {
                    "sfr"   : sfr,
                    "tbins" : tbins,
                    "max_dm" : rho_dm
                }
                
            else:
                grid_sfr, *other = calcStarFormationRate(
                    particle_masses, creation_times, t_start, t_end, nbins
                )
                all_data[nbins]["sfr"] += grid_sfr
                if rho_dm > all_data[nbins]["max_dm"]:
                    all_data[nbins]["max_dm"] = rho_dm 
        # end for nbins
    # end for key

    # return the total number of grids we looked at
    # as well as the number that had stars but
    # no dark matter
    return ngrids, nwodm

    
def calcStarFormationRate(particle_masses, creation_times, t_start, t_end, nbins):

    time_range = [t_start, t_end]

    # create histogram of creation times over the time range
    hist, bins = np.histogram(creation_times, bins=nbins, range=time_range)

    # I forget what this does
    inds = np.digitize(creation_times, bins=bins)

    # bins represents the edge of each time bin
    # this returns the center of each bin for plotting
    tbins = (bins[:-1] + bins[1:])/2
    
    # calculate star formation rate for each bin
    sfr = np.array([
        particle_masses[inds == j+1].sum()/(bins[j+1]-bins[j]) for j in range(len(tbins))
    ])

    return sfr, tbins



def plotResult(data):

    row, col = 1,1
    fig, ax = plt.subplots(row,col, figsize=(8*col,7*row))

    Vol = L_box.to('Mpc/h').value**3

    # plot the data
    for key in data.keys():
        sfr = data[key]["sfr"]
        tbins = data[key]["tbins"]

        ax.loglog(tbins, sfr/Vol, label=f"{len(sfr)}")

    # get the Madau fit to observations
    #convert time to redshift
    zbins = np.array([ds.cosmology.z_from_t( ds.quan(t, 'yr') ) for t in tbins ])   
    ax.loglog(tbins, Madau_fit(zbins), label="Madau fit")

    xtick_labels = np.arange(zstart,zend-1,-1, dtype=int)
    xticks = ds.cosmology.t_from_z(xtick_labels).to('yr').value

    ax.set(
        title=f'Star formation rate density for {L_box.to("Mpc/h").value:.0f} Mpc box',
        xlabel=r"Redshift",
        ylabel=r"SFR $(M_{\odot})$ yr$^{-1}$ Mpc$^{-3}$",
        xticks=xticks,
        xticklabels=xtick_labels
    )
    ax.minorticks_off()

    ax.legend()
    plt.show()
    #fig.savefig('SFR_25Mpc.png')
    plt.close()
    
if __name__ == "__main__":
    
    main()
    


