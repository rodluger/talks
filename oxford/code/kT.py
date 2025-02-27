# -*- coding: utf-8 -*-
"""
Plots the basis of `g` kernels.

"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import paparazzi as pp


# Get the `kT` functions at high res
ydeg = 10
dop = pp.Doppler(ydeg=ydeg, inc=60)
dop.generate_data(R=1e6, nlam=99, y1=np.zeros(dop.N - 1))
kT = dop.kT()

# Set up the plot
fig, ax = plt.subplots(
    ydeg + 1, 2 * ydeg + 1, figsize=(16, 10), sharex=True, sharey=True
)
fig.subplots_adjust(hspace=0)
for axis in ax.flatten():
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["bottom"].set_visible(False)
    axis.spines["left"].set_visible(False)
    axis.set_xticks([])
    axis.set_yticks([])

# Loop over the orders and degrees
n = 0
for i, l in enumerate(range(ydeg + 1)):
    for j, m in enumerate(range(-l, l + 1)):
        j += ydeg - l
        ax[i, j].plot(kT[n])
        n += 1

# Labels
for j, m in enumerate(range(-ydeg, ydeg + 1)):
    ax[-1, j].set_xlabel("%d" % m, fontsize=14, alpha=0.5)
for i, l in enumerate(range(ydeg + 1)):
    ax[i, ydeg - l].set_ylabel(
        "%d" % l, fontsize=14, rotation=45, labelpad=20, alpha=0.5
    )

# Save
fig.savefig("kT.pdf", bbox_inches="tight")
