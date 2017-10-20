"""
data.py defines how to extract data from the archive appliance
"""
import time
import datetime as dt
import numpy as np
import xarray as xr

from datetime import datetime
from . import config
from .dates import utc_delta
from .doc_sub import doc_sub
from .url import arch_url, get_json, hostname_doc, data_port_doc
from .url import PV_ARG, URL_ARG, URL_FLAG

GET_URL = "/retrieval/data/getData.json"

url_args = \
"""
pvs : string or list of string
    pv or pvs to look up in the archiver
start : datetime
    start time of archiver lookup
end : datetime
    end time of archiver lookup
chunk : bool
    if True, chunk data
"""

xarray_doc = \
"""
data : xarray.DataArray
    timestamped data with metadata
"""

raw_doc = \
"""
data : dict
    Raw data from the archiver. This is a dictionary with the following keymap:
    {
       data : [  <list of n entries>
                 {
                    *fields : {
                                 *cnxlostepsecs
                                 *cnxregainedepsecs
                                 *startup
                                 *DESC
                                 *EGU
                                 *PREC
                              }
                    nanos
                    secs
                    severity
                    status
                    val
                 }
              ]
       meta : {
                 EGU
                 PREC
                 name
              }
    }
"""

class ArchiveData(object):
    """
    Class to get data from the archiver.

    Attributes
    ----------
    base_url : string
        url to make data queries at
    """
    @doc_sub(hostname=hostname_doc, data_port=data_port_doc)
    def __init__(self, hostname=config.hostname, data_port=config.data_port):
        """
        Parameters
        ----------
        {hostname}
        {data_port}
        """
        self.base_url = arch_url(hostname, data_port, GET_URL)

    @doc_sub(args=url_args, xarray=xarray_doc)
    def get(self, pvs, start, end, chunk=False, merge=True):
        """
        Parameters
        ----------
        {args}

        merge : bool, optional
            If True, merge results into one xarray.
            If False, return a list of xarrays,
            provided more than one pv was given.

        Returns
        -------
        {xarray}
        """
        if isinstance(pvs, str):
            data = self.get_raw(pvs, start, end, chunk=chunk)
            return make_xarray(data)
        else:
            arrays = []
            for pv in pvs:
                arrays.append(self.get(pv, start, end, chunk=chunk))
            if merge:
                return xr.merge(arrays)
            else:
                return arrays

    @doc_sub(args=url_args, raw=raw_doc)
    def get_raw(self, pv, start, end, chunk=False):
        """
        Parameters
        ----------
        {args}

        Returns
        -------
        {raw}
        """
        url = make_url(self.base_url, pv, start, end, chunk=chunk)
        data = get_json(url)
        return data

@doc_sub(raw=raw_doc, xarray=xarray_doc)
def make_xarray(data):
    """
    Interpret json dictionary as an xarray.DataFrame with proper metadata.

    Parameters
    ----------
    {raw}

    Returns
    -------
    {xarray}
    """
    # Approach:
    #   - put 2d points with val, sevr, stat at timestamps
    #   - use meta to set array attributes
    #   - use most recent EGU PREC DESC, etc. to update meta values
    points = data["data"]
    meta = data["meta"]
    n_pts = len(points)

    # Allocate arrays
    data_ndarray = np.zeros((3, n_pts), dtype=object)
    vals = data_ndarray[0]
    sevr = data_ndarray[1]
    stat = data_ndarray[2]

    times = np.zeros(n_pts, dtype="datetime64[ns]")

    # Not sure how I want to handle disconnection data yet
    skipfields = ("cnxlostepsecs", "cnxregainedepsecs", "startup")

    for i, pt in enumerate(points):
        vals[i] = pt["val"]
        utc = np.datetime64(int(pt["secs"]*1e9+pt["nanos"]), "ns")
        times[i] = utc - np.timedelta64(utc_delta())
        sevr[i] = pt["severity"]
        stat[i] = pt["status"]
        try:
            fields = pt["fields"]
            for fld, fldval in list(fields.items()):
                if fld not in skipfields:
                    meta[fld] = fldval
        except KeyError:
            pass
        
    field_names = ["vals", "sevr", "stat"]
    data_xarray = xr.DataArray(data_ndarray, coords=[field_names, times],
                               dims=["field", "time"], name=meta["name"],
                               attrs=meta)
    return data_xarray

@doc_sub(args=url_args)
def make_url(base_url, pv, start, end, chunk=False):
    """
    Create a full data retrieval url.

    Parameters
    ----------
    {args}

    Returns
    -------
    url : string
        full url used to request data
    """
    url = (base_url + PV_ARG.format(pv)
          + URL_ARG.format("from", date_spec(start))
          + URL_ARG.format("to", date_spec(end)))
    if not chunk:
        url += URL_FLAG.format("donotchunk")
    return url

def date_spec(dtobj):
    """
    Convert local datetime object to UTC for archiver and construct the url
    argument string.

    Parameters
    ----------
    dtobj : datetime
        local date and time for archiver request

    Returns
    -------
    date_spec_arg : string
        url string in UTC and iso format for archiver request
    """
    iso = (dtobj + utc_delta()).isoformat()
    # Differences from standard ISO:
    #    .000 3 precision max instead of 6 (enforce exactly 3)
    #    Z at the end if no timezone offset (enforce always Z and use UTC)
    n = iso.find(".")
    if n > 0:
        iso = iso[:n+4] + "Z"
    else:
        iso += ".000Z"
    return iso
