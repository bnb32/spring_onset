"""Preprocessing utilities"""
import numpy as np


def zonal_band_anomaly_squared_distance(y, y0):
    """Anomaly value for a band at constant latitude"""
    return (y - y0)**2


def meridional_band_anomaly_squared_distance(r, x, x0, y):
    """Anomaly value for a band at constant longitude"""
    ymin = np.sqrt(r) + 1
    ymax = 90 - ymin - 1
    if ymin < y < ymax:
        return (x - x0)**2
    elif y <= ymin:
        return (x - x0)**2 + (y - ymin)**2
    elif y >= ymax:
        return (x - x0)**2 + (y - ymax)**2


def disk_anomaly_squared_distance(x, x0, y, y0):
    """Compute squared distance for use in anomaly calcs"""
    return (x - x0)**2 + (y - y0)**2


def anomaly_smoothing(max_val, d, r):
    """Smooth anomaly at the edges"""
    if d <= r:
        return max_val * (r - d) / r
    return 0


def anomaly_value(max_val, r, x, x0, y, y0, anomaly_type='disk'):
    """Anomaly value for the specified anomaly type"""
    if x >= 180.0:
        x -= 360.0
    if x0 >= 180.0:
        x0 -= 360.0
    if anomaly_type == 'disk':
        d = disk_anomaly_squared_distance(x, x0, y, y0)
    if anomaly_type == 'zonal_band':
        d = zonal_band_anomaly_squared_distance(y, y0)
    if anomaly_type == 'meridional_band':
        d = meridional_band_anomaly_squared_distance(r, x, x0, y)
    if anomaly_type == 'none':
        return 0
    return anomaly_smoothing(max_val, np.sqrt(d), np.sqrt(r))
