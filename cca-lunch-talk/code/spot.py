import starry
import numpy as np

map = starry.Map(15, inc=40)
map.load("spot")
map.show(theta=np.linspace(0, 360, 100), res=300, file="spot.mp4")
