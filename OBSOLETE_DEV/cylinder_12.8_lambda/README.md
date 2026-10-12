# Modified Version of Sionna

> **Note: this analysis is obsolete.** The increase in RMSE at large distances was most likely due to the TX not being far enough away: it was located in the Fraunhofer zone computed with respect to the cylinder radius. See the `TODO_TX` folder for the updated analysis.

At some point during the simulations, the RMSE was found to increase at large distances. It was therefore decided to modify the diffraction coefficients. The relevant code is in the file `diffraction_coeff.txt`, which can be pasted into the Sionna-RT source code.

The modifications are taken from the article *A Uniform Geometrical Theory of Diffraction for an Edge in a Perfectly Conducting Surface*.

In particular:

- the parameter L used to compute the Fresnel integrals was changed from the spherical-wave formulation to the plane-wave one;
- close to the shadow boundaries, a function different from the Fresnel integral is used to avoid singularities.

For the latter, a threshold must be defined. Three were chosen: one at 0.03, one at 0.04, and a moving threshold. The comparison of the thresholds against base Sionna is in the `trashold_comparison` folder.
