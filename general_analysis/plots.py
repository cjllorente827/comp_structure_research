import sys
import yt
yt.enable_parallelism()

# def projection_w_halos(ds, hd, field):

#     proj = yt.ProjectionPlot(ds, 'x', field)

#     # for coordinate system offsets
#     ad = ds.all_data()
#     dims = (ad.right_edge-ad.left_edge).to('Mpc')
#     yoff = (dims[1]/2).value
#     zoff = (dims[2]/2).value

#     print("Annotating halos...")
#     for i in tqdm(range(0,hd.num_halos)):
#         halo = hd.halos[i]
#         halo_pos = np.array([halo[Fields.YPOS],halo[Fields.ZPOS]]) # in kpc

#         # TODO: Figure out a better way of handling this.
#         # Probably best to just save the data in code units during data extraction
        
#         # convert to Mpc
#         halo_pos *= 1e-3

#         # offset center of coordinate system
#         halo_pos[0] -= yoff
#         halo_pos[1] -= zoff
        
#         rad = halo[Fields.RADIUS] # in kpc
#         proj.annotate_sphere(halo_pos, radius=(1000,'kpc'), coord_system='plot')

#     return proj

if __name__ == '__main__':
    argc = len(sys.argv)

    if argc != 3:
        print("""
Usage: python plots.py <enzo_dataset> <output_dir>
""")
    
    enzo_in     = sys.argv[1]
    output_dir  = sys.argv[2]

    ds = yt.load(enzo_in)

    density = yt.ProjectionPlot(ds, 'x', "density")

    density_w_temp = yt.ProjectionPlot(ds, 'x', "density", weight_field='temperature')
    density_w_metal = yt.ProjectionPlot(ds, 'x', "density", weight_field='metallicity')

    temperature = yt.ProjectionPlot(ds, 'x', "temperature")

    metallicity = yt.ProjectionPlot(ds, 'x', "metallicity")

    all_plots = [
        density,
        density_w_temp,
        density_w_metal,
        temperature,
        metallicity,
    ]

    for plot in all_plots:
        plot.annotate_timestamp(corner='upper_left', redshift=True)
        plot.annotate_scale(corner='upper_right')
        plot.save(output_dir)
