import starry
import numpy as np

map = starry.Map(20)
map.load("earth")
map.show(res=500, file="earth.pdf")

map.inc = 60
map.show(res=500, theta=30, file="earth2.pdf")
