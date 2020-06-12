import numpy as np            

class Fields:
    # Field keys
    HALO_ID          = 0
    XPOS             = 1
    YPOS             = 2
    ZPOS             = 3
    RADIUS           = 4
    STR_MASS         = 5
    BAR_MASS         = 6
    GAS_MASS         = 7
    STR_MASS_FRAC    = 8
    DM_MASS          = 9
    TOT_MASS         = 10
    NUM_STAR_PARTICLES = 11
    
    NUM_FIELDS       = 12

    FIELD_LIST_VERSION = 1.1

    # Field names
    names = [
        "Halo Id",
        "Xpos",
        "Ypos",
        "Zpos",
        "Radius",
        "Stellar Mass",
        "Baryon Mass",
        "Gas Mass",
        "Stellar Mass Fraction",
        "Dark Matter Mass",
        "Total Mass",
        "Star Particles"
    ]

    
class HaloData:

    halos = None
    num_halos = 0

    def __init__(self, num_halos, data=None):
        self.halos = data if data is not None else np.zeros((num_halos, Fields.NUM_FIELDS))
        self.num_halos = num_halos

    def check_version(infile):
        pass
    
    def load_from_file(infile):
        HaloData.check_version(infile)
        
        data = np.genfromtxt(infile, skip_header=2)

        return HaloData(np.shape(data)[0], data )

    def save_to_file(self, outfile):
        print(f"Writing to file: {outfile}...")
        tabs = 30
        header = f"Version: {Fields.FIELD_LIST_VERSION}\n"
        header += '\t'.join(Fields.names).expandtabs(tabs) + '\n'
        format_str = '\t'.join(['%3d'] + ["%.10e"]*(Fields.NUM_FIELDS-1)) + '\n'

        data_string = ''
        for i in range(0, self.num_halos):
        
            data_string += (format_str % tuple(self.halos[i])).expandtabs(tabs)
            
        with open(outfile, "w+") as f:
            f.write(header + data_string)
        print("Done")


####################################################################
# Returns a new HaloData object with a filtered halo list
# field - the field to filter on
# filter_func - the filter function to use, ideally some sort of
#               lambda function such as lambda val, cut: val > cut
# value - the threshold value to filter by, becomes the second arg
#         to the filter function
#
# returns filtered HaloData object
#
# Example:
#    cutoff = 1e10 # ignore halos less than 1e10 solar masses
#    filter_func = lambda val, cut: val > cut
#    filtered_halos = filter_by(hd, Fields.NUM_STAR_PARTICLES, filter_func, cutoff)
####################################################################
    def filter_by(self, field, filter_func, value):

        filtered_indices = []
        for i in range(0, self.num_halos):
            if filter_func(self.halos[i,field], value):
                filtered_indices.append(i)

        N = len(filtered_indices)
        filtered = HaloData(N)
        for i in range(0,N):
            for j in range(0,Fields.NUM_FIELDS):
                filtered.halos[i,j] = self.halos[filtered_indices[i],j]
        return filtered
    
####################################################################
# Performs a data reduction that bins the data according to a specific
# field, and then performs a reduction on each bin, returning the result
# hd - the HaloData object
# bin_field - the field that binning is done on
# field - the field to apply the reduction function to
# func - the reduction function to apply to each bin (or a list of functions)
# bin_scale - 'lin' or 'log', bin edges will be equidistant on either
#             a linear or log scale, default 'lin'
# nbins - number of bins to use, if None, defaults to the sqrt of the
#         number of data points
#
# returns - array of arrays, first array are the bin edges, all other arrays are the field
#           values in the order the functions are given
#
# Example:
#    median = apply_reduction(hd, Fields.TOT_MASS, Fields.STR_MASS_FRAC, np.median, bin_scale='log')
####################################################################
def apply_reduction(hd, bin_field, field, func, bin_scale='lin', nbins=None):

    if type(func) == type(lambda x:x):
        N = 1
        func_list = [func]
    elif type(func) == type([]):
        N = len(func)
        func_list = func
    
    if bin_scale not in ['lin', 'log']:
        print(f"Error: Invalid value for bin_scale: {bin_scale}. Valid values are 'lin' or 'log'.")
        return None

    nbins = int(np.sqrt(hd.num_halos)) if nbins is None else nbins
    
    data = hd.halos[:,bin_field]
    hist, bins = np.histogram(data, bins=nbins)

    if bin_scale == 'log':
        logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
        hist, null = np.histogram(data, bins=logbins)
        bins = logbins
    
    maxlen = np.max(hist)+1 # have an extra slot at the end for safety
    data_bins = np.zeros((nbins, maxlen))

    reduced_data = np.zeros((N+1,nbins))
    reduced_data[0] = bins[:-1]


    # iterate over reduction functions
    for f in range(0, N):
        func = func_list[f]

        # iterate over bins
        for i in range(0, nbins):
            left_edge = bins[i]
            right_edge = bins[i+1]
            count = 0

            # iterate over halos in the list
            for j in range(0, hd.num_halos):
                halo = hd.halos[j]
                if halo[bin_field] >= left_edge and halo[bin_field] < right_edge:
                    data_bins[i, count] = halo[field]
                    count += 1
            # end for j

            # reduce the data (if it exists)
            if count > 0:
                reduced_data[f+1,i] = func_list[f](data_bins[i,:count])
        #end for i

    if bin_scale == 'log':
        # some data cleanup, replaces zero values with nan so they are not plotted
        reduced_data[reduced_data==0.] = np.nan

    #end for f

    return reduced_data 

    
