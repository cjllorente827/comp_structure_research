import numpy as np

ncore = np.array([1, 2, 4, 8, 16, 32, 64 ])
#times = np.array([934, 445,  179, 82.5, 55, 66.3, 83.2]) # first run
times = np.array([1057, 497,  254, 113, 57.6, 55.0, 73.6]) # second run
title = "Halo Inspection scaling"
xlabel = "# of processes"
ylabel1 = "Runtime (s)"


# times2 = np.array([23.8, 23.9,  24.7, 23.1, 27.3, 67.5, 263]) # first run
times2 = np.array([25.8, 24.9,  24.8, 24.5, 28.5, 75.9, 294]) # second run
title2 = "Enzo dataset load scaling"
ylabel2 = "Runtime (s)"

show_ideal = True
#show_ideal = False
