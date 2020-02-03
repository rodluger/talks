import starry
import matplotlib.pyplot as plt
import numpy as np

starry.config.lazy = False

map = starry.Map(5)

for lon in np.linspace(-180, 180, 30, endpoint=False):
    map.add_spot(intensity=0.1, sigma=0.1, lat=0, lon=lon, relative=False)
map[1, 0] = 0.5

map.show(projection="rect")
