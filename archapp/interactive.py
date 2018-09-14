"""
interactive.py defines ipython archive interface
"""

import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime
from . import config
from . import data
from . import mgmt
from .doc_sub import doc_sub, doc_sub_txt
from .dates import days_map, units_rule
from .print_formats import print_xarray
from .url import hostname_doc, data_port_doc, mgmt_port_doc

interactive_args = \
"""
pvname : string or list of strings, optional
    Pv or pvs to look up in the archiver. You can include glob
    wildcards in the pv name and we will look up all matching pvs.
    If not selected, we'll use the last pvname we looked up.

{date_args}

chunk : bool, optional
    If True, chunk the data
"""

time_args = \
"""
Time can be designated in three ways:
    1. A number, to designate "units of time ago".
       For example, if units='days', 30 means 30 days ago.
    2. A list of integers to designate a specific date.
       For example, [2016, 11, 10, 5, 0, 0] is Nov 10, 2016 at 5am.
       This list must have at least 3 entries to specify a day and
       may be extended up to 7 entries to specify a time.
       At minimum: [year, month, day].
       At maximum: [year, month, day, hour, min, sec, ms].
    3. A datetime object to designate a specific date.

    The list and datetime objects are in the local timezone.
"""

date_arg = \
"""
{{0}} : number, list of int, or datetime, optional
    {{1}} time in the archiver{{2}}
    {time_args}
"""
date_arg = doc_sub_txt(date_arg, time_args=time_args)

date_args = \
"""
{start}

{end}

{units_rule}
"""
date_args = doc_sub_txt(date_args,
    start=date_arg.format("start", "Start", ", default is 30 days ago."),
    end=date_arg.format("end", "End", ", default is now, the present time."),
    units_rule=units_rule)
interactive_args = doc_sub_txt(interactive_args, date_args=date_args)

class EpicsArchive(object):
    """
    Interactive interface to an Archive Appliance
    """
    @doc_sub(host=hostname_doc, data=data_port_doc, mgmt=mgmt_port_doc)
    def __init__(self, hostname=config.hostname,
                       data_port=config.data_port,
                       mgmt_port=config.mgmt_port):
        """
        Parameters
        ----------
        {host}
        {data}
        {mgmt}
        """
        self._data = data.ArchiveData(hostname, data_port)
        self._mgmt = mgmt.ArchiveMgmt(hostname, mgmt_port)

    @doc_sub(args=interactive_args)
    def get(self, pvname=None, start=30, end=None, unit="days", chunk=False, xarray=False):
        """
        Return timeseries data from the archiver.

        Parameters
        ----------
        {args}

        xarray : bool, optional
            If True, return the xarray. Otherwise, return numpy arrays.

        Returns
        -------
        data : np.ndarray or xarray
        """
        if pvname is None:
            raise NotImplementedError()
        pvs = self._expand_pvnames(pvname)
        dt_objs = sorted(interactive_args(start, end, unit))
        xarr = self._data.get(pvs, dt_objs[0], dt_objs[1], chunk=chunk)
        if xarray:
            return xarr
        raise NotImplementedError()

    def _expand_pvnames(self, pvname):
        """
        Given globs or list of globs, expand to the full set of pvs to look up
        """
        if isinstance(pvname, str):
            return self.search(pvname, do_print=False)
        elif isinstance(pvname, (list, tuple)):
            pvs = []
            for pv in pvname:
                pvs.extend(self._expand_pvnames(pv))
            return pvs
        else:
            raise Exception("pvname must be string, list, or tuple")

    @doc_sub(args=interactive_args)
    def prints(self, pvname=None, start=30, end=None, unit="days", chunk=False):
        """
        Print timeseries data from the archiver.

        Parameters
        ---------
        {args}
        """
        xarr = self.get(pvname=pvname, start=start, end=end, unit=unit, chunk=chunk, xarray=True)
        print_xarray(xarr, "vals")

    @doc_sub(args=interactive_args)
    def plot(self, pvname=None, start=30, end=None, unit="days", chunk=False):
        """
        Plot timeseries data from the archiver in a new figure.

        Parameters
        ----------
        {args}

        Returns
        -------
        plot_handle
        """
        xarr = self.get(pvname=pvname, start=start, end=end, unit=unit, chunk=chunk, xarray=True)
        #print (xarr)
        df = xarr.to_dataframe()
        #return df
        values = df[pvname]['vals']
        sevrs = df[pvname]['sevr']
        #return values
        dft = xarr['time'].to_dataframe()['time']
        #return xarr.to_dataframe()        
        #return xarr# DOING test_plot = arch.plot("pvname") --> test_plot.to_dataframe yeilds the same Pandas dataframe!

        #plt.plot(sevrs, values)
        #plt.scatter(sevrs, values)
        plt.plot_date(dft, values, linestyle='solid', marker='None')
        plt.title(pvname)
        plt.xlabel(unit)
        plt.xticks(rotation=60)
        plt.ylabel('vals')
        plt.show()




    def search(self, glob, do_print=True):
        return self._mgmt.search_pvs(glob, do_print=do_print)
    search.__doc__ = mgmt.ArchiveMgmt.search_pvs.__doc__

@doc_sub(date_args=date_args)
def interactive_args(start, end, unit):
    """
    Return datetime objects given the interactive args.

    Parameters
    ----------
    {date_args}

    Returns
    -------
    endpts : list
        the start and end points of the archive search
    """
    start = convert_date_arg(start, unit)
    if end is None:
        end = dt.datetime.now()
    else:
        end = convert_date_arg(end, unit)
    return [start, end]

@doc_sub(date_arg=date_arg.format("arg", "Arg", ""))
def convert_date_arg(arg, unit):
    """
    Return datetime object corresponding to date argument.

    Parameters
    ----------
    {date_arg}

    Returns
    -------
    date : datetime
    """
    if isinstance(arg, (list, tuple)):
        try:
            return dt.datetime(*arg)
        except:
            raise
    elif not isinstance(arg, dt.datetime):
        try:
            days = days_map[unit] * float(arg)
        except:
            raise
        delta = dt.timedelta(days)
        return dt.datetime.now() - delta
    return arg
