# ArmourPenetrationSandbox

A 3D, War Thunder–style **Protection Analysis & Armor Penetration Simulator** built with a **Python (FastAPI)** ballistics backend and a **Three.js** WebGL frontend.

Instead of a heavy Finite Element Method (FEM) physics engine, the simulator uses real-time 3D raycasting, vector math, and empirical ballistics formulas—giving you instant penetration readouts, automatic slow-motion impact replays, and X-ray spall simulation directly in your browser.

---

## Features

* **Interactive 3D Viewport:** Full orbit, pan, and zoom controls around sloped armor test plates and internal target modules.
* **Live Protection Readout:** Hover anywhere on the armor plate to inspect real-time impact angle ($\theta$) and line-of-sight effective thickness.
* **Automatic Slow-Motion Hit-Cam:** Shells approach at normal speed and automatically drop into configurable slow motion (down to `0.02x`) the millisecond they contact the armor plate.
* **Three Distinct Impact Outcomes:**
  * **Penetration:** Switches the armor plate into translucent X-ray mode, bores through the steel, and unleashes a 3D spall cone out the back of the plate.
  * **Ricochet:** Deflects the shell along the reflected surface vector with a yellow ricochet trail.
  * **Non-Penetration:** Stops and shatters the projectile on impact.
* **Internal Module Damage:** Tracks spall hits against internal **Crew**, **Ammo Rack**, and **Engine Block** volumes behind the armor, shifting them from undamaged $\rightarrow$ yellow (damaged) $\rightarrow$ red (critical) $\rightarrow$ black (destroyed).
* **Configurable Ballistics:** Switch between `APCBC`, `APFSDS`, and `HEAT-FS` shells, adjust plate thickness (`40–300 mm`), slope angle (`0°–80°`), armor material (`RHA`, `Cast`, `Composite`), and firing distance (`100–2000 m`).

---

## How It Works Under the Hood

The simulation is split cleanly between the browser (3D rendering & raycasting) and Python (ballistics math & shell database):

1. **Raycasting & Impact Angle:** Clicking the armor casts a 3D ray from the camera to find the exact hit point and plate surface normal. The impact angle ($\theta$) is computed via the dot product of the shell vector and surface normal.
2. **Effective Thickness:** Line-of-sight thickness is adjusted by the material modifier ($M_{\text{mat}}$):
   $$T_{\text{eff}} = \frac{T}{\cos\theta} \times M_{\text{mat}}$$
3. **Penetration & Ricochet Check:** Python compares the impact angle against the shell's ricochet threshold (`71°` for APCBC, `81°` for APFSDS, `78°` for HEAT-FS) and calculates distance-adjusted penetration (kinetic rounds lose penetration over distance; chemical HEAT rounds do not).
4. **Post-Penetration Spalling:** If penetration exceeds $T_{\text{eff}}$, residual penetration determines the density and spread of secondary spall particles emitted from the exit point on the back of the plate.

---

## Project Structure

```text
ArmourPenetrationSandbox/
├── backend/
│   ├── ballistics.py    # Shell database, material modifiers, penetration & ricochet math
│   └── main.py          # FastAPI server (ballistics API + serves frontend)
├── frontend/
│   └── index.html       # Three.js 3D scene, slow-mo hit-cam, X-ray spall engine, HUD
└── README.md
