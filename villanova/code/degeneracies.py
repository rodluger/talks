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
theta = np.linspace(0, 360, 1000)
ax.plot(theta, map.flux(theta=theta))
ax.set_xlabel(r"$\theta$ [degrees]")
ax.set_ylabel("normalized flux")
fig.savefig("star.pdf", bbox_inches="tight")

a = 0.01
for i in tqdm(range(9)):
    if i > 1:
        for l in l_null:
            map[int(l), :] = np.exp(-a * l ** 2) * np.random.randn(2 * l + 1)
    map.show(theta=np.linspace(0, 360, 50), file="star%d.gif" % (i + 1))
