"""Compute change indices: dNDVI, dNDRE, dBrightness.

Expect input arrays with bands in standard order (e.g., [B, G, R, RE, NIR]) for multi-sensor support.
Provide small, well-documented functions for clarity.
"""
import numpy as np


def safe_divide(a, b, eps=1e-6):
    return (a - b) / (np.maximum(a + b, eps))


def compute_ndvi(band_nir, band_red):
    return safe_divide(band_nir, band_red)


def compute_ndre(band_nir, band_rededge):
    return safe_divide(band_nir, band_rededge)


def compute_brightness(bands):
    """Brightness as the mean of available bands.

    Expected input shape is (bands, rows, cols) or (bands, n_pixels).
    """
    return np.nanmean(np.asarray(bands, dtype='float32'), axis=0)


def compute_change(pre, post, idx_func=None, *args, **kwargs):
    """Return post - pre for either raw arrays or derived indices.

    If idx_func is provided, it is applied to pre and post before differencing.
    """
    if idx_func is None:
        pre_idx = np.asarray(pre, dtype='float32')
        post_idx = np.asarray(post, dtype='float32')
    else:
        pre_idx = idx_func(*pre, *args, **kwargs) if isinstance(pre, (list, tuple)) else idx_func(pre, *args, **kwargs)
        post_idx = idx_func(*post, *args, **kwargs) if isinstance(post, (list, tuple)) else idx_func(post, *args, **kwargs)
    return post_idx - pre_idx
