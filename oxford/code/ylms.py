import starry
import numpy as np

ydeg = 2
map = starry.Map(ydeg)

n = 0
for l in range(ydeg + 1):
    for m in range(-l, l + 1):
        map.reset()
        if l > 0:
            map[l, m] = 1.0
        map.show(theta=np.linspace(0, 360, 50), file="y{}.mp4".format(n))
        n += 1
