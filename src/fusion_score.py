"""Combine normalized indices and apply terrain and post-event weights.

Score = (w1*dNDVI + w2*dNDRE + w3*dBrightness) * Wterrain * Wpost
"""
import numpy as np


def compute_fusion(dndvi, dndre, dbrightness, weights=None, wterrain=1.0, wpost=1.0):
    if weights is None:
        weights = {'dndvi': 0.7, 'dndre': 0.2, 'dbrightness': 0.1}
    s = weights.get('dndvi', 0.7) * dndvi
    s = s + weights.get('dndre', 0.2) * dndre
    s = s + weights.get('dbrightness', 0.1) * dbrightness
    # Multiply arrays element-wise by terrain and post weights
    # wterrain and wpost may be scalars or arrays matching s
    return s * wterrain * wpost
