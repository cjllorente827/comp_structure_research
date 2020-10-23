
import sys

def print_help_and_exit():
    print("""
Usage: python star_formation_rate_plots.py <enzo_dataset> <halo_dataset> <output file prefix> <full-run|plots-only>
    """)
    exit()
    
if len(sys.argv) != 5:
    print_help_and_exit()
    
sys.path.append('/mnt/home/llorente/comp_structure_research')

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from HaloData import *
from HaloHistory import HaloHistory, load_history
from matplotlib.colors import LogNorm

matplotlib.rcParams.update({'font.size': 16})
matplotlib.rcParams.update({"figure.facecolor": 'FFFFFF'})
np.set_printoptions(threshold=sys.maxsize)

RUN_DATA_EXTRACTION = False
OUTPUT_PREFIX = ''

def inspect_history(hist):
    rows = 2
    cols = 1
    fig, axes = plt.subplots(rows,cols,figsize=(18*cols,7*rows))

    index = 0

    m = hist.ssfr_fit[index,0]
    b = hist.ssfr_fit[index,1]
    fit = lambda t: 10**(m*np.log10(t) + b)

    axes[0].loglog(hist.tbins/1e9, fit(hist.tbins), c='b', linestyle='dashed')
    axes[0].loglog(hist.tbins/1e9, hist.ssfr[index], c='b', linewidth=0, marker='o')
    axes[1].loglog(hist.tbins/1e9, hist.csm[index], c='b', linewidth=0, marker='o')
    
    axes[0].set_xlabel('Time (Gyr)')
    axes[0].set_ylabel('sSFR  [yr$^{-1}$]')

    plt_fname = f"{OUTPUT_PREFIX}_inspect.png"
    print(f"Saving plot to {plt_fname}")
    fig.savefig(plt_fname)

    

def ssfr_v_sm(hist):
    pass

def data_extraction(ds_fname, hd_fname, redshifts, pkl_fname):
    global RUN_DATA_EXTRACTION
    hist = HaloHistory(ds_fname, hd_fname, redshifts)

    print(f"Outputting HaloHistory to {pkl_fname}")
    hist.dump(pkl_fname)
    return hist

def make_plots(halo_history):
    inspect_history(halo_history)
    ssfr_v_sm(halo_history)

def main(ds_fname, hd_fname, pkl_fname):

    redshifts = [0.1,0.5,1,2,3,4,5,6,7,8]
    hist = None
    if RUN_DATA_EXTRACTION:
        hist = data_extraction(ds_fname, hd_fname, redshifts, pkl_fname)
    else:
        hist = load_history(pkl_fname)

    make_plots(hist)


if __name__ == "__main__":
    ds_fname   = sys.argv[1]
    hd_fname   = sys.argv[2]
    pkl_fname = str(sys.argv[3])

    if sys.argv[4] == 'full-run':
        RUN_DATA_EXTRACTION = True
    elif sys.argv[4] == 'plots-only':
        RUN_DATA_EXTRACTION = False
    else:
        print_help_and_exit()

    main(ds_fname, hd_fname, pkl_fname)
