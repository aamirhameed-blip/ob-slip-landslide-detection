"""Utility helpers for OB-SLIP.

Keep functions small and dataset-agnostic. No hardcoded paths here.
"""
from pathlib import Path
import yaml
import rasterio


def load_config(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, 'r') as f:
        cfg = yaml.safe_load(f)
    return cfg


def read_raster(path):
    """Return tuple (array, profile) with raster read as float32."""
    with rasterio.open(path) as src:
        arr = src.read().astype('float32')
        profile = src.profile
    return arr, profile


def write_raster(path, array, profile):
    path = Path(path)
    profile = dict(profile)
    data = array.astype('float32')
    if data.ndim == 2:
        profile.update(dtype='float32', count=1)
    else:
        profile.update(dtype='float32', count=data.shape[0])
    path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(path, 'w', **profile) as dst:
        if data.ndim == 2:
            dst.write(data, 1)
        else:
            dst.write(data)


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)
