import starry
import numpy as np
import matplotlib.pyplot as plt

starry.config.lazy = False

map = starry.Map(20, inc=90, obl=-23.5, reflected=True)
map.load("earth", psd=False)

# Light curve
npts = 50000
phase = np.linspace(-180, 180, npts)
source = np.array(
    [np.sin(np.pi / 180 * phase), np.zeros_like(phase), np.cos(np.pi / 180 * phase)]
).T
time = np.linspace(0, 365.25, npts)
theta = np.linspace(0, 365.25 * 360, npts)
flux = map.flux(theta=theta, source=source)
flux /= np.max(flux)
plt.plot(time, flux)
plt.xlabel("time [days]")
plt.ylabel("reflected flux")
plt.show()
quit()

# Video
npts = 300
phase = np.linspace(0, 360, npts)
source = np.array(
    [np.sin(np.pi / 180 * phase), np.zeros_like(phase), np.cos(np.pi / 180 * phase)]
).T
theta = np.linspace(0, 5 * 360, npts)
cmap = plt.get_cmap("plasma")
cmap.set_under("k")
map.show(theta=theta, source=source, vmin=1e-10, cmap=cmap, file="earth.mp4")
