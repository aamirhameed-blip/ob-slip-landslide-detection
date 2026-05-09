"""Preprocessing utilities: read, mask, normalize.

Functions are dataset-agnostic and accept file paths or opened arrays.
"""
import numpy as np
from .utils import read_raster


def percentile_normalize(arr, lower=2, upper=98, clip=(0, 1)):
    """Robust normalization: clip to [lower, upper] percentiles then scale to clip range.

    Parameters
    - arr: numpy array (any shape)
    - lower/upper: percentiles
    - clip: tuple(min, max) -> resulting range

    Returns normalized array in clip range (float32).
    """
    a = arr.astype('float32')
    lo = np.nanpercentile(a, lower)
    hi = np.nanpercentile(a, upper)
    if hi == lo:
        hi = lo + 1e-6
    a = (a - lo) / (hi - lo)
    a = np.clip(a, 0.0, 1.0)
    out_min, out_max = clip
    return a * (out_max - out_min) + out_min


def read_pre_post(pre_path, post_path):
    pre, pre_profile = read_raster(pre_path)
    post, post_profile = read_raster(post_path)
    return pre, post, pre_profile, post_profile
