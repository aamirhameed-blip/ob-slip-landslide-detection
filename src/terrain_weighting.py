"""Compute terrain-based weight Wterrain from slope in degrees.

Rules (from paper):
- slope < 1° => 0
- 1°–20° => linear scaling from 0.20 to 1.00
- 20°–45° => 1.00
- >45° => 0.85
"""
import numpy as np


def terrain_weight(slope_deg_array, *, ramp_min=1.0, ramp_max=20.0, ramp_min_weight=0.2, ramp_max_weight=1.0, flat_max=45.0, high_slope_weight=0.85):
    s = np.array(slope_deg_array, dtype=float)
    w = np.ones_like(s)

    # slope < ramp_min -> 0
    w[s < ramp_min] = 0.0

    # ramp between ramp_min and ramp_max -> linear interpolation
    mask_ramp = (s >= ramp_min) & (s < ramp_max)
    if np.any(mask_ramp):
        frac = (s[mask_ramp] - ramp_min) / (ramp_max - ramp_min)
        w[mask_ramp] = ramp_min_weight + frac * (ramp_max_weight - ramp_min_weight)

    # between ramp_max and flat_max -> 1.0 (already default)

    # above flat_max -> high_slope_weight
    w[s > flat_max] = high_slope_weight

    return w


def terrain_weight_from_config(slope_deg_array, terrain_cfg):
    """Map example_config.yml terrain settings into terrain_weight()."""
    thresholds = terrain_cfg.get('slope_thresholds', {})
    return terrain_weight(
        slope_deg_array,
        ramp_min=float(thresholds.get('ramp_min', 1.0)),
        ramp_max=float(thresholds.get('ramp_max', 20.0)),
        ramp_min_weight=float(terrain_cfg.get('ramp_min_weight', 0.2)),
        ramp_max_weight=float(terrain_cfg.get('ramp_max_weight', 1.0)),
        flat_max=float(thresholds.get('flat_max', 45.0)),
        high_slope_weight=float(terrain_cfg.get('high_slope_weight', 0.85)),
    )
