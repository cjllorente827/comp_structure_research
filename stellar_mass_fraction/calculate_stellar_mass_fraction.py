import sys
import yt
from tqdm import tqdm
from collections import OrderedDict
from yt.extensions.astro_analysis.halo_analysis.api import HaloCatalog
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid

def stars(pfilter, data):
    filter = data[("all", "particle_type")] == 2 # DM = 1, Stars = 2
    return filter

yt.add_particle_filter("stars", function=stars, filtered_type='all', \
                       requires=["particle_type"])

def extract_data_to_dat_file(hc, ds, outfile):

    omega_b = 0.0486
    omega_c = 0.2589
    baryonic_mass_fraction = omega_b * ds.cosmology.omega_matter
    fields = OrderedDict()
    data_string = ""

    print(f"Parsing halo catalogs.....")
    for halo in tqdm(hc.catalog):
        
        fields["Halo Id"] = halo['particle_identifier']

        halo_pos = (halo['particle_position_x'],halo['particle_position_y'],halo['particle_position_z'])

        fields["Xpos"] = halo_pos[0].in_units('kpc').value
        fields["Ypos"] = halo_pos[1].in_units('kpc').value
        fields["Zpos"] = halo_pos[2].in_units('kpc').value
        
        fields["Radius"] = halo['virial_radius'].in_units('kpc')
        sphere = ds.sphere(halo_pos, fields["Radius"])
            
        stellar_mass = sphere[('stars', 'particle_mass')].sum().in_units('Msun').value
        gas_mass = sphere.quantities.total_mass()[0].in_units('Msun').value
        total_mass = sphere.quantities.total_mass().sum().in_units('Msun').value
        dm_mass = omega_c * total_mass
        b_mass  = omega_b * total_mass
        baryonic_mass = gas_mass + stellar_mass
        mass_fraction = stellar_mass/baryonic_mass

        fields["Stellar Mass"] = stellar_mass
        fields["Baryon Mass"] = baryonic_mass
        fields["Gas Mass"] = gas_mass
        fields["Star Mass Fraction"] = mass_fraction
        fields["Dark Matter Mass"] = dm_mass
        fields["Total Mass"] = total_mass
        
        tabs = 20
        try : header
        except NameError:
            header = '\t'.join(fields.keys()).expandtabs(tabs) + '\n'
        try : format_str
        except NameError:
            format_str = '\t'.join(['%3d'] + ["%.3e"]*(len(fields.keys())-1)) + '\n'
        data_string += (format_str % tuple([x for x in fields.values()])) .expandtabs(tabs)
        
    with open(outfile, "w+") as f:
        f.write(header + data_string)
    print(f"Data written to {outfile}")

def annotate_halos(hc, ds):
    fig = plt.figure()
    grid = AxesGrid(fig, (0.1,0.1,0.9,0.9),
                nrows_ncols = (1, 2),
                axes_pad = 0.05,
                label_mode = "1",
                share_all = True,
                cbar_location="right",
                cbar_mode="single",
                # cbar_size="3%",
                cbar_pad="0%")
    
    left_edge  = [0.488794, 0.473535, 0.505703]
    right_edge = [0.492794, 0.477535, 0.509703]
    must_refine_region = ds.box(left_edge, right_edge)
    proj = yt.ProjectionPlot(ds, "z", "density", data_source=must_refine_region, width=(0.4,'Mpc'))
    part = yt.ParticlePlot(ds, 'particle_position_x', 'particle_position_y',
                           color='k',data_source=must_refine_region, width=(0.4,'Mpc'))
    max_rad = 0.
    max_pos = [0.,0.]
    for halo in tqdm(hc.catalog):
        rad = halo['virial_radius'].in_units('kpc').value
        if rad > max_rad:
            max_rad = rad
            max_pos[0] = float(halo['particle_position_x'].to('Mpc').value)
            max_pos[1] = float(halo['particle_position_y'].to('Mpc').value)
        halo_pos = [halo['particle_position_x'],
                    halo['particle_position_y'],
                    halo['particle_position_z']]
        proj.annotate_sphere(halo_pos, radius=(rad, 'kpc'), coord_system='data')
        part.annotate_sphere(halo_pos, radius=(rad, 'kpc'), coord_system='data')

    print(max_pos)
    proj.set_center(max_pos, unit='Mpc')
    proj.annotate_timestamp(redshift=True)
    proj.annotate_scale()
    proj.set_log('density', True)
    proj.save("density")

    part.set_center(max_pos, unit='Mpc')
    part.save("particles")



def main(infile, outfile):
        print(f"Reading from {infile}")
        ds = yt.load(infile)
        ds.add_particle_filter('stars')
        outfile = outfile % ds.current_redshift
        # hds = yt.load("halo_catalogs/catalog/catalog.0.h5")
        hds = yt.load("rockstar_halos/halos_0.0.bin")

        hc = HaloCatalog(data_ds=ds, halos_ds=hds)
        hc.load()

        #extract_data_to_dat_file(hc, ds, outfile)
        annotate_halos(hc, ds)

if __name__ == "__main__":
    
    OUTFILE = "stellar_mass_fraction_z%.5f.dat"

    infile = sys.argv[1]

    main(infile, OUTFILE)

    
