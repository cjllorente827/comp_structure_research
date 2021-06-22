import sys, subprocess, time, psutil, gc

from matplotlib.animation import FuncAnimation, ImageMagickFileWriter
from matplotlib import projections, rc_context
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})
import numpy as np
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import AxesGrid, make_axes_locatable

import blk

from mpi4py import MPI
MPI_COMM = MPI.COMM_WORLD
MPI_NPROCS = MPI_COMM.Get_size()
MPI_RANK = MPI_COMM.Get_rank()


if len(sys.argv) not in [3,4]:
    print("""
Usage: python thin_projection_movie.py <dataset_filename> <nframes> [start_from]
""")

import yt
yt.enable_parallelism()

def main():

    total_start = time.time()

    # pull in command line arguments
    ds_fname = str(sys.argv[1])
    nframes = int(sys.argv[2])
    #START_FROM = int(sys.argv[3]) if len(sys.argv) == 4 else 0

    # calculate interval from desired framerate
    fps = 5
    interval = int(100/fps) # Imagemagick uses centiseconds

    # grab the data from the dataset
    frame_data, projection_time = blk.Do_Query(
        simple_projection, ds_fname, 'density', nframes, clear_cache=True)

    sys.exit()

    if yt.is_root():

        # create the temp images that will become our gif
        # TODO: figure out how to exploit the parallelism
        #       we're already using
        print("Generating frames...")
        plot_start = time.time()
        for i in range(nframes):
            simple_plot(frame_data[i], i)
            #plot_2_by_2_img(frame_data[i], i)
        plot_time = time.time() - plot_start
        print("Done.")

        # convert images into a gif
        conversion_start = time.time()
        runConversion(interval)
        conversion_time = time.time() - conversion_start
        
        # clean up temp files
        cleanup_start = time.time()
        cleanup()
        cleanup_time = time.time() - cleanup_start

        total = time.time() - total_start
        print(f"""
Projection Time  : {format_time(projection_time)}
Plot Time        : {format_time(plot_time)}
Conversion Time  : {format_time(conversion_time)}
Cleanup Time     : {format_time(cleanup_time)}
Total time       : {format_time(total)}
""")

def simple_projection(ds_fname, field, nframes):

    # load the dataset and add the particle filter
    ds = yt.load(ds_fname)
    #ds.add_particle_filter("stars")

    # calculate some necessary quantities to 
    # determine what each frame contains
    L = ds.domain_width[0].to('Mpc/h')
    dL = (ds.quan(0.5, 'Mpc/h') / L ).value
    vel = (1.0-dL)/nframes

    # shorthand for grabbing the specific part of the slab we need
    def slab(n):
        return ds.r[:,:,n*vel : n*vel+dL]

    # make a projection for every frame
    frame_data = np.zeros((nframes, 800, 800))
    for i in range(nframes):
        plot = yt.ProjectionPlot(ds, 'z', field, 
            data_source=slab(i), weight_field='density')

        frame_data[i] = np.array(plot.frb['density'])[:]

        if yt.is_root():
            print(gc.get_stats())
            frame_data_mem = sys.getsizeof(frame_data)/(2**30)
            print(f"Total frame data: {frame_data_mem} GB")
            check_mem_usage()

    return frame_data

# define the function that will be used as our query
def create_projections_2x2(ds_fname, fields, nframes):

    # load the dataset and add the particle filter
    ds = yt.load(ds_fname)
    ds.add_particle_filter("stars")

    # calculate some necessary quantities to 
    # determine what each frame contains
    L = ds.domain_width[0].to('Mpc/h')
    dL = (ds.quan(0.5, 'Mpc/h') / L ).value
    vel = (1.0-dL)/nframes

    # shorthand for grabbing the specific part of the slab we need
    def slab(n):
        return ds.r[:,:,n*vel : n*vel+dL]

    # make a projection for every frame
    frame_data = []
    for i in range(nframes):
        plot = yt.ProjectionPlot(ds, 'z', fields, 
            data_source=slab(i), weight_field='density')

        # coerce the data into 1024x1024 pixel images
        frb = plot.data_source.to_frb(L, 1024)
        data = [None]*4 
        data[0] = np.array(frb['density'])
        data[1] = np.array(frb['metallicity'])
        data[2] = np.array(frb['temperature'])

        # Fix stellar density to have a floor
        star_density = np.array(frb[('deposit','stars_density')])
        star_density[star_density == 0.] = 1e-33
        
        data[3] = star_density[:]
        frame_data.append(data)

    return frame_data

FIELDS = [
        'density', 
        'metallicity',
        'temperature', 
        ('deposit', 'stars_density')]

CMAPS = [
    'viridis', 
    'dusk', 
    'plasma', 
    'Purples_r']

TITLES = [
    'Density',
    'Metallicity', 
    'Temperature', 
    'Stellar Density']

def output_fname(n):
    return f'tmp/tmp_{n:04d}.png'

def simple_plot(data, index):

    fig, ax = plt.subplots(1,1)

    im = ax.imshow(data, origin='lower', 
        norm=LogNorm(), cmap=CMAPS[0],
        vmin=1e-32, vmax=1e-27)

    cbar = fig.colorbar(im)
    cbar.set_label(TITLES[0])

    
    plt.savefig(output_fname(index))
    plt.close()

    
def plot_2_by_2_img(data, index=0):
    
    HEIGHT = 15
    WIDTH = 18

    axes = [None]*4
    fig, ((axes[0], axes[1]),(axes[2], axes[3])) = plt.subplots(
        2,2,
        figsize=(WIDTH, HEIGHT),
        sharex='all',
        sharey='all')

    plt.subplots_adjust(left=0.03, \
                        bottom=0.05,\
                        right=0.9,\
                        top=0.95,\
                        wspace=0.1,\
                        hspace=0.01)

    imgs = []
    for i,ax in enumerate(axes):
        im = ax.imshow(data[i], origin='lower', 
            norm=LogNorm(), cmap=CMAPS[i])

        # capture these image objects for editing for animations
        imgs.append(im)

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = fig.colorbar(im, cax=cax)
        cbar.set_label(TITLES[i])

    
    plt.savefig(output_fname(index))
    plt.close()
        
        
def runConversion(interval):
    print("Running conversion to gif format...")
    cmd = f"convert -delay {interval} -loop 0 tmp/*.png projection.gif"
    subprocess.run(cmd, shell=True)

    print("Done.")

def cleanup():
    print("Removing files from tmp")
    subprocess.run(['ls', 'tmp'])
    subprocess.run('rm tmp/*.png', shell=True)

def format_time(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

def check_mem_usage():
    mem = psutil.Process().memory_info().vms / (2**30)
    print(f"Currently using {mem} GB")

# set up yt's particle filter
def stars(pfilter, data):
    filter = data[("all", "particle_type")] == 2 # DM = 1, Stars = 2
    return filter

yt.add_particle_filter("stars", function=stars, filtered_type='all', \
                       requires=["particle_type"])


if __name__ == "__main__":
    main()