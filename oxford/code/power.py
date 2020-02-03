import starry
import numpy as np
import matplotlib.pyplot as plt


starry.config.lazy = False
plt.style.use("default")
plt.rcParams["savefig.dpi"] = 100
plt.rcParams["figure.dpi"] = 100
plt.rcParams["figure.figsize"] = (12, 4)
plt.rcParams["font.size"] = 14
plt.rcParams["text.usetex"] = False
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Liberation Sans"]
plt.rcParams["font.cursive"] = ["Liberation Sans"]
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["mathtext.fallback_to_cm"] = True
np.random.seed(0)


def power_spectrum(l, mu, sig):
    """A very simple gaussian power spectrum."""
    A = 1.0 / (np.sqrt(2 * np.pi) * sig)
    return A * np.exp(-((l - mu) ** 2) / sig ** 2)


def random_map(power):
    """Generate a random isotropic map with a given power spectrum."""
    lmax = len(power)
    N = (lmax + 1) ** 2
    y = np.random.randn(N - 1)
    for l in range(1, lmax + 1):
        m = np.arange(-l, l + 1)
        n = l ** 2 + l + m - 1
        y[n] *= np.sqrt(power[l - 1] / np.sum(y[n] ** 2))
    return y


# Create a starry map
ydeg = 20
map = starry.Map(ydeg)
map.inc = 45

l = np.arange(1, ydeg + 1)
mu = 0.0
sigs = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
fig, ax = plt.subplots(1)

for n, sig in enumerate(sigs):

    # Get the power spectrum
    power = power_spectrum(l, mu, sig)

    # Sample from this power spectrum
    map[1:, :] = random_map(power)

    # Show the map
    theta = np.linspace(0, 360, 50, endpoint=False)
    map.show(theta=theta, file="power{}.mp4".format(n))

    ax.plot(l, power, "-", color="C{}".format(n))

for k in np.arange(3, ydeg + 1, 2):
    ax.axvspan(k - 0.5, k + 0.5, color="r", alpha=0.075, ec="none")

ax.set_xlim(1, ydeg)
ax.set_xticks(np.arange(1, ydeg + 1))
ax.set_xticklabels(
    [1, 2, "", 4, "", 6, "", 8, "", 10, "", 12, "", 14, "", 16, "", 18, "", 20]
)
ax.set_yscale("log")
ax.set_ylim(1e-5, 1e0)
ax.set_xlabel("spherical harmonic degree", fontsize=16)
ax.set_ylabel("power", fontsize=16)
fig.savefig("power.pdf".format(n), bbox_inches="tight")
