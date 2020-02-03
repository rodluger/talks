import starry
import numpy as np

map = starry.Map(35)
map.load("jupiter", sigma=0.01)
map.inc = 60
map.show(theta=np.linspace(0, 360, 50), file="jupiter.mp4", cmap="twilight")
