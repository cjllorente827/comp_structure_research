
from typing import NewType
import numpy as np
import yt, gc, sys

yt.funcs.mylog.setLevel(50)
yt.enable_parallelism()

from memory_profiler import profile

run_test = int(sys.argv[1])
nframes = int(sys.argv[2])


#ds_fname='/mnt/research/galaxies-REU/sims/cosmological/set1_LR/halo_008508/RD0042/RD0042'
ds_fname='/mnt/home/llorente/cosmo_bigbox/25Mpc_512/RD0265/RD0265'
ds = yt.load(ds_fname)
#ds.add_particle_filter("stars")

# calculate some necessary quantities to 
# determine what each frame contains
L = ds.domain_width[0].to('Mpc/h')
dL = (ds.quan(0.5, 'Mpc/h') / L ).value
vel = (1.0-dL)/nframes

@profile
def test_func1():
    
    frame_data = np.zeros((nframes, 800, 800))
    
    for i in range(nframes):
        next_slab = ds.r[:,:,i*vel : i*vel+dL]
        plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')

        frame = np.array(plot.frb['density'])

        frame_data[i] =  frame[:]
    return frame_data

@profile
def test_func2():
    
    frame_data = np.zeros((nframes, 800, 800))
    gc.disable()
    
    for i in range(nframes):
        next_slab = ds.r[:,:,i*vel : i*vel+dL]
        plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')

        frame = np.array(plot.frb['density'])

        frame_data[i] =  frame[:]

        del frame
        del next_slab
        del plot

        gc.collect()

    gc.enable()
    return frame_data

@profile
def test_func3():
    
    frame_data = np.zeros((nframes, 800, 800))
    next_slab = ds.r[:,:,0 : dL]
    plot = yt.ProjectionPlot(ds, 'z', 'density', data_source=next_slab, weight_field='density')

    for i in range(nframes):
        next_slab = ds.r[:,:,i*vel : i*vel+dL]
        plot._switch_ds(ds, data_source=next_slab)

        frame = np.array(plot.frb['density'])

        frame_data[i] =  frame[:]
    return frame_data

@profile
def test_func4():

    frame_data = np.zeros((nframes, 800, 800))
    next_slab = ds.r[:,:,0 : dL]
    
    for i in range(nframes):
        next_slab = ds.r[:,:,i*vel : i*vel+dL]
        plot = ds.proj('density', 'z', weight_field='density', data_source=next_slab)
        frb = plot.to_frb(1, 800)
        frame = np.array(frb['density'])

        frame_data[i] =  frame[:]
    return frame_data

@profile
def test_func5():

    frame_data = np.zeros((nframes, 800, 800))
    gc.disable()
    
    for i in range(nframes):
        next_slab = ds.r[:,:,i*vel : i*vel+dL]
        plot = ds.proj('density', 'z', weight_field='density', data_source=next_slab)
        frb = plot.to_frb(1, 800)
        frame = np.array(frb['density'])

        frame_data[i] =  frame[:]

        del frame
        del frb
        del plot
        del next_slab
        gc.collect()

    gc.enable()
    return frame_data


if run_test == 1:
    result = test_func1()
elif run_test == 2:
    result = test_func2()
elif run_test == 3:
    result = test_func3()
elif run_test == 4:
    result = test_func4()
elif run_test == 5:
    result = test_func5()

print(f"Final product is {sys.getsizeof(result)/(2**20)} MB")

