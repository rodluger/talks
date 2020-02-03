import starry
import numpy as np

map = starry.Map(3)
map[3, 3] = 1
map.show(theta=np.linspace(0, 360, 50), file="Y33.mp4", dpi=400)
