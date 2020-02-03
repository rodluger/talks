import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 1000)
line1 = -np.exp(-(x ** 2 / (0.1) ** 2))
fig = plt.figure()
plt.plot(x, line1, lw=10)
plt.gca().axis("off")
fig.savefig("line1.pdf")

line2 = -np.exp(-(x ** 2))
fig = plt.figure()
plt.plot(x, line2, lw=14)
plt.gca().axis("off")
fig.savefig("line2.pdf")
