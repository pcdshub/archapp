"""
plot.py defines all plotting macros
"""
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr

def epics_data_plot(data):
    """
    Plot the EPICS timeseries data values.

    Parameters
    ----------
    data : xarray.DataArray, xarray.Dataset, pandas.Series, or pandas.DataFrame
        EPICS data in some standard form. If you have headers, values should be
        under "val".
    """
    if isinstance(data, (xr.DataArray, xr.Dataset)):
        data = data.to_dataframe()
