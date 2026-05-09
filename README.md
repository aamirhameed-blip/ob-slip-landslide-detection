# OB-SLIP

OB-SLIP: A Terrain-Constrained Object-Based Extension of the SLIP Algorithm for Multi-Sensor Landslide Detection

Overview
--------
OB-SLIP applies an object-based post-processing and terrain-constrained weighting to pixel-wise spectral-change scores (e.g., dNDVI, dNDRE, brightness) to detect potential landslides in multi-sensor imagery (PlanetScope, Sentinel-2, etc.). The pipeline was developed for reproducible scientific use and is dataset-agnostic.

Required inputs
---------------
- Pre-event and post-event imagery (aligned and coregistered) — multi-band optical (PlanetScope, Sentinel-2, etc.).
- DEM (digital elevation model) covering the study area (for slope computation).

High-level workflow
-------------------
1. Preprocessing: read & align inputs, mask nodata, compute per-band normalization.
2. Spectral index computation: compute dNDVI, dNDRE, dBrightness (post - pre).
3. Robust normalization: percentile clipping (2nd–98th) and scale to [0, 1].
4. Terrain-constrained fusion: combine indices using weights and apply terrain weight Wterrain and post-event mask weight Wpost.
5. Thresholding: Otsu thresholding on fused score to produce binary detection mask.
6. Object-based filtering (MMU): remove objects smaller than MMU (pixels) and produce vector polygons.

How to run
----------
- From the command line (after installing requirements):

```bash
# install dependencies
pip install -r requirements.txt

# run example notebook (recommended)
# open notebooks/example_workflow.ipynb in Jupyter or VS Code
```

Parameter defaults
------------------
- Robust normalization: 2nd–98th percentile clipping, scaled to 0–1.
- Fusion example (PlanetScope-like): Score = (0.70 * dNDVI + 0.20 * dNDRE + 0.10 * dBrightness) * Wterrain * Wpost
- Terrain weighting: slope < 1° → 0; 1°–20° → linear 0.20 → 1.00; 20°–45° → 1.00; >45° → 0.85
- Thresholding method: `otsu`
- MMU: 9 pixels

Expected outputs
----------------
- Raster: fused score image, binary detection mask
- Vector: detected polygons (`GeoPackage`)
- Validation tables (CSV): detection counts, precision/recall metrics
- Figures: diagnostic plots (KDEs, maps)

Configuration
-------------
All parameters and input paths are controlled via `config/example_config.yml`.

Citation
--------
If you use OB-SLIP in published work, please cite:

> [Author], OB-SLIP: A Terrain-Constrained Object-Based Extension of the SLIP Algorithm for Multi-Sensor Landslide Detection, (paper details).

Reproducibility note
--------------------
The full repository will be archived on Zenodo upon publication to provide a permanent DOI and ensure long-term reproducibility.

License
-------
This project is released under the MIT License. See `LICENSE` for details.
