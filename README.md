# Cylinder scattering simulations with Sionna-RT

Bachelor's degree thesis work (*Ingegneria Elettronica per l'Intelligenza Artificiale*, UNIBO Cesena) on wireless channel simulation with ray tracing. This repository contains the scenes, simulation scripts and results used to assess how accurately **Sionna-RT** reproduces the field scattered by a **cylinder**, a canonical scatterer for which an exact analytical solution exists.

## Introduction

Ray tracing is the basis of many channel simulators, but its accuracy in the **shadow region** behind an object, where the field is dominated by diffraction, is not guaranteed. A circular cylinder is an ideal test case: the total field around it can be computed exactly with the modal (Bessel/Hankel) series, and this is used here as ground truth.

The cylinder is approximated in Sionna-RT by a prism with a finite number of faces (the *discretization*, ν), so that it can be handled by the geometric optics / UTD machinery of the ray tracer. The study compares the ray-traced field with the analytical one while varying:

- the **cylinder radius** (5 to 25.6 λ);
- the **discretization** of the cylinder (ν = 6, 8, 12, 17 faces);
- the **distance of the receivers** from the cylinder (from 0.1 λ to thousands of λ);
- the **distance of the transmitter**, to approximate an incident plane wave.

### Simulation setup

| Parameter | Value |
|---|---|
| Carrier frequency | 2 GHz (λ = 0.15 m) |
| Polarization | HH (TE) |
| Antennas | single isotropic element for TX and RX |
| Receivers | ring of RX around the cylinder (720 points, one every 0.5°, in `simulate_loop.py`) |
| Ray-tracing mechanisms | LOS, reflection, diffraction and double-edge diffraction (`max_depth=1`) |
| Reference | exact analytical solution of scattering by a cylinder (`cylinder_te_inc_scat_total`, 512 terms) |
| Metrics | RMSE and MAE in dB between analytical and ray-traced total field in the forward-scattering (shadow) region |

The TX is placed on the x axis at a distance from the cylinder derived from the Fraunhofer condition (`2·(2D)²/λ + D`, with D the cylinder radius), or much farther away (10⁷ m) in the TX distance study. The ray-traced field is multiplied by `4π·d_tx` so that the incident field is normalized and results at different distances are comparable.

### First results

- With the TX at the Fraunhofer distance, a cylinder discretized with **12 faces** gives the best agreement. The RMSE heatmaps in `results/RMSE/short_cylinder/tables/` show errors of about 10-18 dB very close to the cylinder (below about 4 λ), and RMSE of about 1-3 dB from roughly 10 λ onward. The lowest values (about 0.7-0.8 dB) are reached for a radius of 12.8 λ at 20-30 λ.
- Coarser discretizations (8 faces) are more accurate in the area close to the cylinder surface; 17 faces is not necessarily than 12 (see `results/MAE/`).
- At **large receiver distances the RMSE grows again**, this problem hasn't be resolved yet.
- A first attempt to fix this by modifying the diffraction coefficients (uniform theory of diffraction with plane-wave parameter L) is kept in `OBSOLETE_DEV/`. That analysis is **obsolete**: the growth of the RMSE was most likely caused by the TX not being far enough away.
- Moving the TX much farther (10⁷ m) improves the results, but in the deep shadow region the ray tracer is then unable to compute the field, and at intermediate TX distances this happens only sometimes, in a way that is not yet predictable. This is the open problem described in `TODO_TX_dist/`.
- The comparison with a full-wave CST simulation (`TODO_Electromagnetic_validation/`) has not been conclusive so far: the teaching version of CST probably does not allow enough mesh cells for a reliable simulation.

## Repository structure

```
.
├── ENV_SIONNA.yml                 # conda environment (Sionna 0.17.0)
├── simulate.py                    # single simulation, TX/RX setup, RMSE and plots
├── simulate_loop.py               # loop over radii, discretizations and distances (RMSE/MAE .csv)
├── simulate_dev.py                # development version of simulate.py (TX at 10e6 m, debug output)
├── scattered_field_loop.py        # scattered field (analytical vs ray tracing) saved to .csv
├── simulate.ipynb                 # notebook version of the simulation
├── visualizer.ipynb               # notebook to visualize scenes and results
├── models/                        # Sionna scenes (see below)
├── results/                       # RMSE / MAE results and plotting scripts
├── plane/                         # simplified plane model (Blender file, notebook, field plot)
├── TODO_TX_dist/                  # open analysis: effect of the TX distance
├── TODO_Electromagnetic_validation/  # comparison with full-wave CST results
└── OBSOLETE_DEV/                  # obsolete modification of the diffraction coefficients
```

### Sionna version

The scripts use the double-edge and vertex diffraction objects developed by Ainur Ziganshin (https://github.com/AinurZiga/sionna-RT-reflectivity.git).

### `models/`

Scenes in the Sionna/Mitsuba format (`scene.xml` + `meshes/*.ply`). Each cylinder is identified by its radius (in λ) and by the number of faces:

```
models/cylinder_<radius>_lamda/<length>/cylinder_<nu>/cylinder_<nu>.xml
```

- radii: 5, 10, 12.8, 15.9, 19, 22.3 and 25.6 λ;
- `short`: 4 m long cylinder; `long long`: 10 km long cylinder (only for some configurations);
- `plane/`: simplified model of a plane;
- `stl_files/`: `.stl` models generated with Blender and `trimesher.py`, which converts them to `.ply` files compatible with Sionna-RT (`.stl` files are git-ignored).

### `results/`

- `RMSE/short_cylinder/`: RMSE for all radii and discretizations (`simulation_RESULTS/RESULTS_<nu>_<radius>.csv`), heatmaps (`tables/`), comparison between radii (`cylinder_radius_comparison/`) and the analysis and plotting scripts.
- `RMSE/long_cylinder/`: RMSE for the long cylinders (radii 12.8 and 25.6 λ; 8 and 12 faces), including the comparison between cylinder lengths.
- `MAE/radius_12.8_lambda/`: MAE versus distance for ν = 6, 8, 12, 17 and a radius of 12.8 λ.

### `TODO_TX_dist/`

Analysis of the effect of the TX distance, with `frahonoufer_distance/` (TX at the Fraunhofer distance) and `long_distance/` (TX at 10⁷ m). Each plot shows the total field in the shadow region, analytical versus Sionna-RT, for a given receiver distance. See its README.

### `TODO_Electromagnetic_validation/`

Near-field comparison between the analytical solution, Sionna-RT (`sionna_results.csv`) and CST (`near_field*.txt`), with `validation.py` producing `near_field_validation.png`.

### `OBSOLETE_DEV/`

Modified diffraction coefficients (`diffraction_coef.txt`, to be pasted in the Sionna-RT source) and comparison of the different thresholds against base Sionna. Kept for reference only, see its README.

### Running a simulation

Scripts use relative paths, so they must be launched from the root of the repository. `simulate_loop.py` writes its output to `./temp/`, which must exist:

```bash
mkdir -p temp
python simulate_loop.py
```

The parameters (radius, discretization, TX distance, receiver distances, polarization) are set at the top of each script.

## Future developments

- **Estending deep shadow prediction to different scenes and objects**: extend the analysis from cylinders to other objects.
- **Understand the TX distance problem**: find why the ray tracer does not compute the field in the deep shadow region for a very distant TX, and why this happens unpredictably at intermediate distances (see `TODO_TX_dist/`), and fix or work around it.
- **Re-assess the RMSE at large distances** once the TX distance issue is solved, now that the earlier increase is attributed to the TX position and not to the diffraction coefficients.

