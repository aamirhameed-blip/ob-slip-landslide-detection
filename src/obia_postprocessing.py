"""Object-based postprocessing: thresholding and size filtering.

Uses skimage for morphological operations where available.
"""
import numpy as np
from skimage.filters import threshold_otsu
from skimage.morphology import label


def otsu_threshold(score_array):
    flat = score_array[np.isfinite(score_array)]
    if flat.size == 0:
        return np.zeros_like(score_array, dtype=bool)
    thr = threshold_otsu(flat)
    mask = score_array >= thr
    return mask, float(thr)


def apply_mmu(mask_bool, mmu_pixels=9):
    # Label connected components and keep only objects meeting the MMU.
    lbl = label(mask_bool)
    if lbl.max() == 0:
        return np.zeros_like(mask_bool, dtype=bool)
    counts = np.bincount(lbl.ravel())
    keep = counts >= mmu_pixels
    keep[0] = False
    return keep[lbl]
