"""
dates.py defines tools for working with timezones and units of time
"""
import time
import datetime as dt
from .doc_sub import doc_sub_txt
from .print_formats import list_print

days_map = {}
days_map.update({ x: 365              for x in ("years", "year", "yr", "y")        })
days_map.update({ x: 365./12          for x in ("months", "month", "mon")          })
days_map.update({ x: 7                for x in ("weeks", "week", "wks", "wk", "w") })
days_map.update({ x: 1                for x in ("days", "day", "d")                })
days_map.update({ x: 1./24            for x in ("hours", "hour", "hrs", "hr", "h") })
days_map.update({ x: 1./24/60         for x in ("minutes", "minute", "mins", "min")})
days_map.update({ x: 1./24/60/60      for x in ("seconds", "secs", "sec", "s")     })
days_map.update({ x: 1./24/60/60/1000 for x in ("milliseconds", "msec", "ms")      })

units_rule = \
"""
unit : string, optional
    How to interpret numeric inputs to start and end. Default is days.
    Allowed inputs are:
    {map_keys}
"""
map_keys = list_print(sorted(days_map.keys()), width=72, do_print=False)
units_rule = doc_sub_txt(units_rule, map_keys="\n".join(map_keys))

delta = None
def utc_delta():
    """
    Determine the offset from localtime to utc

    Returns
    -------
    delta : datetime.timedelta
        timedelta object that represents the UTC offset
    """
    global delta
    if delta is None:
        now = time.time()
        local_now = dt.datetime.fromtimestamp(now)
        utc_now = dt.datetime.utcfromtimestamp(now)
        delta = utc_now - local_now
    return delta

