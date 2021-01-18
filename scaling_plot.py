import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from scaling_data import *

fig, (ax1,ax2) = plt.subplots(2,1,figsize=(7,7), sharex=True)

ideal      = np.max(times)/ncore

ax1.set_title(title)
ax2.set_title(title2)
ax2.set_xlabel(xlabel)

ax1.set_ylabel(ylabel1)
ax2.set_ylabel(ylabel2)

ax1.loglog(ncore, times, marker='o', linewidth=0, label="Measured")
ax2.loglog(ncore, times2, marker='o', linewidth=0, label="Measured")



ax2.set_xticks(ncore)
ax2.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax2.tick_params(which='major')

if show_ideal:
    ax1.loglog(ncore, ideal, label="Ideal")
    ax1.legend()

plt.show()
