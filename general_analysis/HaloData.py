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
    
    NUM_FIELDS       = 11

    FIELD_LIST_VERSION = 1

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
        "Total Mass"
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
        tabs = 20
        header = f"Version: {Fields.FIELD_LIST_VERSION}\n"
        header += '\t'.join(Fields.names).expandtabs(tabs) + '\n'
        format_str = '\t'.join(['%3d'] + ["%.3e"]*(Fields.NUM_FIELDS-1)) + '\n'

        data_string = ''
        for i in range(0, self.num_halos):
        
            data_string += (format_str % tuple(self.halos[i])).expandtabs(tabs)
            
        with open(outfile, "w+") as f:
            f.write(header + data_string)
        print("Done")