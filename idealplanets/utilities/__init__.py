"""Utilities"""


def open_file(file, mode):
    """Use Nio to open file. Should replace this with xarray"""
    import Nio
    return Nio.open_file(file, mode)
