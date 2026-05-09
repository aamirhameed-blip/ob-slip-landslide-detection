"""Simple validation utilities comparing detections to inventory.

These functions are minimal and designed for inclusion in reproducible workflows.
"""
import geopandas as gpd


def compute_confusion(detections_gdf, inventory_gdf, buffer_m=0):
    """Compute TP/FP/FN by spatial intersection. Matches any overlap >0 counted as TP.
    - detections_gdf: GeoDataFrame of detected polygons
    - inventory_gdf: GeoDataFrame of reference polygons
    Returns dict with TP, FP, FN and matched IDs.
    """
    det = detections_gdf.copy()
    inv = inventory_gdf.copy()

    det['matched'] = False
    inv['matched'] = False

    for di, drow in det.iterrows():
        for ii, irow in inv.iterrows():
            dgeom = drow.geometry.buffer(buffer_m) if buffer_m else drow.geometry
            igeom = irow.geometry.buffer(buffer_m) if buffer_m else irow.geometry
            if dgeom.intersects(igeom):
                det.at[di, 'matched'] = True
                inv.at[ii, 'matched'] = True

    tp = int(det['matched'].sum())
    fp = int((~det['matched']).sum())
    fn = int((~inv['matched']).sum())

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    if precision + recall > 0:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = 0.0

    return {'TP': tp, 'FP': fp, 'FN': fn, 'precision': precision, 'recall': recall, 'f1': f1}
