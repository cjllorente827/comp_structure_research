import sys
import yt
import numpy as np
import matplotlib.pyplot as plt

fname = sys.argv[1]

halo_id, xpos, ypos, zpos, rad, s_mass, b_mass, g_mass, s_frac, dm_mass, tot_mass =\
    np.genfromtxt(fname, skip_header=1, unpack=True)

fig, ax = plt.subplots(1,1,figsize=(7,7))

ax.loglog(tot_mass, s_frac, lw=0, marker='o')
ax.set_title("Stellar Mass Fraction")
ax.set_xlabel("$M_{tot}$  ($M_{\odot}$)")
ax.set_ylabel("$M_{*}/M_b$")

plt.show()
