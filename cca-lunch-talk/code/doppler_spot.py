# -*- coding: utf-8 -*-
"""
Show the effect a rotating spot has on an absorption line.

"""
import matplotlib.pyplot as plt
import numpy as np
import starry
import paparazzi as pp
from matplotlib.animation import FuncAnimation


# Generate two maps
ydeg = 20
N = (ydeg + 1) ** 2
map1 = starry.Map(ydeg)
map1.add_spot(amp=-0.03, sigma=0.05, lat=30, lon=0)
map1.inc = 90

map2 = starry.Map(ydeg)
map2.load("spot")
map2.inc = 40

for map, name in zip([map1, map2], ["spot1", "spot2"]):

    # Get the map coeffs
    y1 = np.array(map.y.eval())[1:]

    # Generate the dataset
    vsini = 40.0  # km/s
    nt = 100
    theta = np.linspace(-180, 180, nt)
    dop = pp.Doppler(ydeg, vsini=vsini, inc=map.inc.eval())
    dop.generate_data(
        y1=y1, R=3.0e5, nlam=149, sigma=2.0e-5, nlines=1, theta=theta, ferr=0.0
    )
    lnlam = dop.lnlam
    F0 = dop.F[0]
    F = dop.F

    # Render the images
    img = map.render(theta=theta, res=300).eval()

    # Set up the plot
    fig, ax = plt.subplots(1, 3, figsize=(12, 4))
    cmap = plt.get_cmap("plasma")
    vmin = np.nanmin(img)
    vmax = np.nanmax(img)
    rng = vmax - vmin
    vmin -= 0.1 * rng
    vmax += 0.1 * rng

    # Plot spectrum
    ax[1].plot(dop.lnlam, F0, "k:", lw=1, alpha=0.5)
    spec, = ax[1].plot(dop.lnlam, F[0], "k-")
    ax[1].set_ylim(0.9 * np.min(F), 1.1 * np.max(F))
    ax[1].axis("off")

    # Plot residuals
    color = [cmap(x) for x in np.linspace(0.75, 0.0, 5)]
    lw = np.linspace(2.5, 0.5, 5)
    alpha = np.linspace(0.25, 1, 5)
    res = [None for i in range(5)]
    for i in range(5):
        res[i], = ax[2].plot(
            lnlam, F[0] - F0, ls="-", lw=lw[i], color=color[i], alpha=alpha[i]
        )
    ax[2].axis("off")
    ax[2].set_ylim(-0.055, 0.055)

    # Plot current stellar image
    ims = ax[0].imshow(
        img[0], origin="lower", extent=(-1, 1, -1, 1), cmap=cmap, vmin=vmin, vmax=vmax
    )
    ax[0].set_xlim(-3, 1.05)
    ax[0].set_ylim(-1.05, 1.05)
    ax[0].axis("off")

    def updatefig(t):
        ims.set_array(img[t])
        spec.set_ydata(F[t])
        for i in range(5):
            res[i].set_ydata(F[t] - F0)
        return [ims, spec] + res

    ani = FuncAnimation(fig, updatefig, interval=50, blit=False, frames=nt)
    ani.save("%s.mp4" % name, writer="ffmpeg")
