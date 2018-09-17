"""
file_formats.py defines file outputs from input xarray objects
"""
import copy
import numpy as np
import pandas as pd

def load_pvnames(filename):
    """
    Given a file with one pv on each line, return a list of pvs.
    """
    with open(filename, "r") as f:
        lines = f.readlines()
        return [l[:-1] for l in lines]

def csv_coll(xarray, pv, avg_period=None):
    data = xarray[pv][0].values # numeric
    times = xarray[pv].time.values # datetime64
    # strip nans
    d = []
    t = []
    for val, tim in zip(data, times):
        if not np.isnan(val):
            d.append(val)
            t.append(tim)
    data = d
    times = t

    def out_str(ts_array):
        out = str(ts_array[0])
        delims = "-- ::"
        for i, d in enumerate(delims):
            try: out += d + str(ts_array[i+1])
            except: return out
        return out

    periods = ("year", "month", "day", "hour", "minute", "second")
    def stat_append(vals, methods, lists):
        for m, lst in zip(methods, lists):
            lst.append(m(vals))

    def tim_spec(dt64, spec):
        timestamp = pd.to_datetime(dt64)
        return [getattr(timestamp, periods[i]) for i in range(spec+1)]

    if avg_period is not None:
        coll = [(pv, "avg", "min", "max")]
        if avg_period in periods:
            spec = periods.index(avg_period)
            # split time into chunks to average
            # replace data and times appropriately
            avg = []
            min = []
            max = []
            t = []
            curr_time = None

            for val, tim in zip(data, times):
                tim = tim_spec(tim, spec)
                if curr_time is None:
                    curr_time = tim
                    curr_vals = [val]
                elif tim == curr_time:
                    curr_vals.append(val)
                else:
                    stat_append(curr_vals,
                        [np.mean, np.min, np.max],
                        [avg, min, max])
                    t.append(out_str(curr_time))
                    curr_time = None
            if curr_time is not None and curr_vals:
                stat_append(curr_vals,
                    [np.mean, np.min, np.max],
                    [avg, min, max])
                t.append(out_str(curr_time))
            combined = [(str(t[n]), str(avg[n]), str(min[n]), str(max[n])) for n in range(len(t))]
        else:
            print("bad avg_period, must be in {}".format(periods))
            return coll
    else:
        coll = [(pv, "value")]
        spec = len(periods) - 1
        times = [tim_spec(t, spec) for t in times]
        times = [out_str(t) for t in times]
        combined = [(times[n], str(data[n])) for n in range(len(data))]
    coll.extend(combined)
    return coll

def build_csv(colls, filename=None):
    colls = copy.copy(colls)
    lens = [len(c) for c in colls]
    max_len = max(lens)
    for c in colls:
        while len(c) < max_len:
            #c.append(("",""))
            c.append([""]*len(c[0]))

    lines = []
    for i in range(max_len):
        lines.append([])
    for coll in colls:
        for i, row in enumerate(coll):
            txt = ",".join(row)
            if not lines[i]:
                lines[i] = txt
            else:
                lines[i] = ",".join((lines[i],txt))
    for i in range(len(lines)):
        lines[i] += "\n"
    if filename:
        with open(filename, "w") as f:
            f.writelines(lines)
    else:
        for line in lines:
            print(line)
   

def csv(xarray, filename=None, sync_timestamps=False):
    """
    Write xarray data into a csv file. Assumes the data came from an archiver
    query, as defined in data.py. Format is something like:
    pvname,desc,pvname,desc,pvname,desc
    time,value,time,value,time,value
    time,value,time,value,time,value
    time,value,,,time,value
    """
    skip_fields = ("field", "time")
    colls = []
    for pv in xarray:
        if pv not in skip_fields:
            coll = [(pv, xarray[pv].attrs.get("DESC", ""))]
            data = xarray[pv][0].values
            times = xarray[pv].time.values
            data = [(str(times[n]), str(data[n])) for n in range(len(data)) if not np.isnan(data[n])]
            coll.extend(data)
            colls.append(coll)
    lens = [len(c) for c in colls]
    if lens:
        max_len = max(lens)
    else:
        max_len = 0
    for c in colls:
        while len(c) < max_len:
            c.append(("",""))
    lines = []
    for i in range(max_len):
        lines.append([])
    for coll in colls:
        for i, row in enumerate(coll):
            txt = ",".join(row)
            if not lines[i]:
                lines[i] = txt
            else:
                lines[i] = ",".join((lines[i],txt))
    if filename:
        with open(filename, "w") as f:
            f.writelines(lines)
    else:
        for line in lines:
            print(line)

