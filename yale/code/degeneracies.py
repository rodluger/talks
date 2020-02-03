import starry
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

starry.config.lazy = False
np.random.seed(12)

map = starry.Map(15)
map.inc = 60.0
map.load("earth")

l_vis = np.append([1], np.arange(2, map.ydeg + 1, 2, dtype=int))
l_null = np.arange(3, map.ydeg + 1, 2, dtype=int)

fig, ax = plt.subplots(1)
time = np.linspace(0, 3, 1000)
theta = np.linspace(0, 3 * 360, 1000)
flux = map.flux(theta=theta)
flux_obs = flux + 0.005 * np.random.randn(1000)
ax.plot(time, flux_obs, "k.", ms=2, alpha=0.5)
ax.plot(time, flux, "C0")
ax.set_xlabel(r"time [days]")
ax.set_ylabel("normalized flux")
fig.savefig("star.pdf", bbox_inches="tight")

a = 0.01
for i in tqdm(range(4)):
    if i > 0:
        for l in l_null:
            map[int(l), :] = 0.1 * np.exp(-a * l ** 2) * np.random.randn(2 * l + 1)
    map.show(theta=np.linspace(0, 360, 50), vmin=0, vmax=1, file="star%d.gif" % (i + 1))
