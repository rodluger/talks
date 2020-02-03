import starry
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

map = starry.Map(20, reflected=True)
map.load("earth")
npts = 100

theta = np.linspace(0, 360 * 2, npts)
phi = np.linspace(0, 2 * np.pi, npts)
xs = np.cos(phi)
zs = np.sin(phi)
ys = 0.5


cmap = plt.get_cmap("plasma")
cmap.set_over("k")
image = map.render(res=500, theta=theta, xs=xs, ys=ys, zs=zs).eval()
vmin = 0
vmax = np.nanmax(image)
norm = colors.Normalize(vmin=vmin, vmax=vmax)
image[image == 0] = 999

map.show(image=image, file="reflected.mp4", cmap=cmap, norm=norm)
