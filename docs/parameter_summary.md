# OB-SLIP Parameter Summary

This document summarizes the key parameters used in OB-SLIP and their recommended defaults (as used in the paper).

Fusion weights
--------------
- `dNDVI`: 0.70
- `dNDRE`: 0.20
- `dBrightness`: 0.10

These weights reflect the relative importance assigned to change in NDVI, NDRE, and overall brightness in PlanetScope-like multispectral imagery. They are configurable in `config/example_config.yml`.

Terrain weighting logic
-----------------------
Given a slope in degrees `s`:
- `s < 1°` → Wterrain = 0.0 (very flat areas suppressed)
- `1° ≤ s < 20°` → Wterrain interpolates linearly from 0.20 to 1.00
- `20° ≤ s ≤ 45°` → Wterrain = 1.00
- `s > 45°` → Wterrain = 0.85

This reduces spurious detections in very flat or extremely steep terrain while prioritizing the mid-slope range where landslides commonly occur.

Normalization
-------------
- Robust percentile normalization: clip values to the 2nd and 98th percentiles and scale the clipped range to [0, 1]. This reduces the influence of outliers and sensor noise.

Thresholding and MMU
--------------------
- Threshold: Otsu thresholding on the fused score raster.
- Minimum Mapping Unit (MMU): 9 pixels (remove objects smaller than MMU).

Validation approach
-------------------
- Compute polygon intersections between detected objects and the reference inventory.
- Count True Positives (TP) as detections with any overlap with inventory polygons.
- False Positives (FP) are detection polygons not overlapping any inventory polygon.
- False Negatives (FN) are inventory polygons with no overlapping detection.
- Report precision, recall, and F1-score.

Notes
-----
- All parameters live in `config/example_config.yml` and should be adapted for other sensors (e.g., Sentinel-2) by adjusting fusion weights and preprocessing steps as appropriate.
