#!/usr/bin/env python
# -*- coding: utf-8 -*-
from planetplanet.constants import *
from planetplanet import Star, Planet, System, jwst
import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u
import starry


starry.config.lazy = False


def pp_sim():
    """
    From this script, I conclude that in the F770W filter,
    
    - sigma is 2.90e-5 per minute-long exposure
    - eclipse depth is 3.85e-3

    """
    # Instantiate the star
    mstar = 0.846
    rstar = 0.805
    teff = (0.328 * LSUN / (4 * np.pi * (rstar * RSUN) ** 2 * SBOLTZ)) ** 0.25
    star = Star("A", m=mstar, r=rstar, teff=teff, color="k")

    # Instantiate `b`
    RpRs = 0.145
    r = RpRs * rstar * RSUN / REARTH
    b = Planet(
        "b",
        m=369.3,
        per=2.22,
        inc=85.76,
        r=r,
        t0=0,
        Omega=0,
        w=0,
        ecc=0,
        color="firebrick",
        tnight=40.0,
        albedo=0.0,
        phasecurve=True,
    )

    # Instantiate the system
    system = System(star, b, distance=19.8, oversample=10)
    time = np.arange(-2, 2, MINUTE)

    # Compute the light curve
    system.compute(time, lambda1=1, lambda2=35)

    # Observe it (one exposure)
    np.random.seed(1234567)
    filter = jwst.get_miri_filter_wheel()[1]  # F770W
    filter.compute_lightcurve(
        system.time,
        system.flux,
        system.continuum,
        system.wavelength,
        stack=1,
        time_hr=system.time_hr,
        flux_hr=system.flux_hr,
        atel=25.0,
        thermal=True,
        quiet=False,
    )
    lightcurve = filter.lightcurve

    plt.plot(lightcurve.time, lightcurve.Nsys / lightcurve.norm)
    plt.plot(lightcurve.time, lightcurve.obs, "k.", ms=2)
    plt.show()


star = starry.Primary(
    starry.Map(udeg=2, amp=1), r=0.805, m=0.846, length_unit=u.Rsun, mass_unit=u.Msun
)
star.map[1:] = [0.5, 0.25]

planet_amp = 0.6 * 0.0035  # ensure depth is 3.85 ppt
planet = starry.Secondary(
    starry.Map(6, amp=planet_amp, inc=85.76,),
    r=1.138,
    m=1.162,
    inc=85.76,
    porb=2.22,
    prot=2.22,
    theta0=180,
    length_unit=u.Rjup,
    mass_unit=u.Mjup,
    angle_unit=u.degree,
)

sys = starry.System(star, planet)
time = np.arange(-2, 2, MINUTE)

A0 = planet_amp * sys.design_matrix(time)[:, 1]
A = planet_amp * sys.design_matrix(time)[:, 2:]

# Generate
sigma = 2.9e-5
N = (planet.map.ydeg + 1) ** 2 - 1
for lon in np.linspace(-180, 180, 30, endpoint=False):
    planet.map.add_spot(intensity=0.01, sigma=0.1, lat=0, lon=lon, relative=False)
planet.map.rotate([0, 1, 0], 15)
planet.map[1, 0] = 0.5
np.random.seed(6)
planet.map[1:, :] += 3e-2 * np.random.randn(N)
y = planet.map[1:, :]
flux0 = A0 + A.dot(y)
flux = flux0 + sigma * np.random.randn(len(time))

# Infer
L = (
    np.concatenate(
        [
            np.ones(2 * l + 1) * np.std(planet.map[l, :])
            for l in range(1, planet.map.ydeg + 1)
        ]
    )
    ** 2
)
LInv = np.diag(1 / L)
CInv = A.T.dot(A) / sigma ** 2
yhat = np.linalg.solve(CInv + LInv, A.T.dot(flux - A0) / sigma ** 2)

fig, ax = plt.subplots(1)
ax.plot(time, 1e3 * flux, "k.", ms=2)
ax.plot(time, 1e3 * (A0 + A.dot(yhat)))
ax.set_xlabel("time [days]")
ax.set_ylabel("planet flux [ppt]")
fig.savefig("hd189_lc.pdf", bbox_inches="tight")
ax.set_xlim(-1.22, -1.00)
fig.savefig("hd189_lc_zoom.pdf", bbox_inches="tight")

planet.map[1:, :] = y
theta = np.linspace(0, 360, 50, endpoint=False)
planet.map.show(res=500, theta=theta, file="hd189_tru.mp4")
planet.map.show(res=500, projection="rect", file="hd189_tru.pdf")

planet.map[1:, :] = yhat
planet.map.show(res=500, theta=theta, file="hd189_inf.mp4")
planet.map.show(res=500, projection="rect", file="hd189_inf.pdf")

print(np.linalg.matrix_rank(CInv), CInv.shape[0])
