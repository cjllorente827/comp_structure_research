import sys

argc = len(sys.argv)

if argc != 3:
    print(f"\n\tUsage: python {sys.argv[0]} <enzo_dataset> <output_dir>\n")
    sys.exit()

import gc
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

    enzo_in     = sys.argv[1]
    output_dir  = sys.argv[2]

    ds = yt.load(enzo_in)

    # 1st: field to project, 2nd: field to weight by, 3rd: colormap to use
    field_list = [
        ("density", None, "viridis"),
        ("temperature", None, "plasma"),
        ("metallicity", None, "dusk"),
        ("density", "temperature", "plasma"),
        ("density", "metallicity", "dusk"),
        ]

    for f in field_list:
        #our boy uses a lot of fucking memory for these plots
        gc.collect()
        
        field  = f[0]
        weight = f[1]
        cmap   = f[2]
        plot = yt.ProjectionPlot(ds, 'x', field, weight_field=weight)
        plot.annotate_timestamp(corner='upper_left', redshift=True)
        plot.annotate_scale(corner='upper_right')
        plot.set_cmap(field, cmap=cmap)
        plot.save(output_dir)

