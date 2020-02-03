import starry
import numpy as np

map = starry.Map(20)
map.load("earth")
map.show(res=500, theta=np.linspace(0, 360, 50), file="earth.mp4")
