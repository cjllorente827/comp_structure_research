import sys
import yt
import numpy as np
import matplotlib.pyplot as plt
from HaloData import *


def stellar_mass_fraction_scatter(fname):
    hd = HaloData.load_from_file(fname)

    fig, ax = plt.subplots(1,1,figsize=(7,7))

    ax.loglog(hd.halos[:,Fields.TOT_MASS], hd.halos[:,Fields.STR_MASS_FRAC], lw=0, marker='o')
    ax.set_title("Stellar Mass Fraction")
    ax.set_xlabel("$M_{tot}$  ($M_{\odot}$)")
    ax.set_ylim(top=1.)
    ax.set_ylabel("$M_{*}/(\Omega_b/\Omega_m)/M_{vir}$")

    #plt.savefig("stellar_mass_fraction_bigbox.png")

def main(dataset_fname, halo_dat_fname):
    stellar_mass_fraction_scatter(halo_dat_fname)
    plt.show()


if __name__ == "__main__":

    usage_str =\
    """
Usage: 
    python plots.py <dataset_file_name> <halo_dat_file>
    """

    argc = len(sys.argv)
    if argc != 2 and argc != 1:
        print(usage_str)
        sys.exit()

    if argc == 1:
        print("Running in test mode")
        dataset_fname  = "test_data/RD0009/RD0009"
        halo_dat_fname = "test_data/halo_test.dat"
    else:
        dataset_fname  = sys.argv[1]
        halo_dat_fname = sys.argv[2]
        
    main(dataset_fname, halo_dat_fname)
