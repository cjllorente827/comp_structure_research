import sys
import yt
import numpy as np
import matplotlib.pyplot as plt
from HaloData import *

fname = sys.argv[1]

hd = HaloData.load_from_file(fname)

fig, ax = plt.subplots(1,1,figsize=(7,7))

ax.loglog(hd.halos[:,Fields.TOT_MASS], hd.halos[:,Fields.STR_MASS_FRAC], lw=0, marker='o')
ax.set_title("Stellar Mass Fraction")
ax.set_xlabel("$M_{tot}$  ($M_{\odot}$)")
ax.set_ylim(top=1.)
ax.set_ylabel("$M_{*}/(\Omega_b/\Omega_m)/M_{vir}$")

#plt.show()
plt.savefig("stellar_mass_fraction_bigbox.png")
