import starry
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

starry.config.lazy = False

map = starry.Map(20)

nstars = 10
inc = np.linspace(0, 90, nstars + 2)[1:-1]
nspots = 20
theta = np.linspace(0, 360, 50, endpoint=False)
for k in tqdm(range(nstars)):
    map.reset()
    map.inc = inc[k]
    for n in range(nspots):
        intensity = -0.1 + 0.01 * np.random.random()
        sigma = 0.025 + 0.01 * np.random.random()
        lat = (30 + 5 * np.random.randn()) * np.sign(np.random.randn())
        lon = 360 * np.random.random()
        map.add_spot(intensity=intensity, sigma=sigma, lat=lat, lon=lon, relative=False)
    map.show(theta=theta, file="inc{}.mp4".format(k))
    fig = plt.figure()
    theta_ = np.linspace(0, 2 * 360, 500)
    plt.plot(theta_, map.flux(theta=theta_))
    plt.gca().axis("off")
    fig.savefig("inc{}.pdf".format(k), bbox_inches="tight")
