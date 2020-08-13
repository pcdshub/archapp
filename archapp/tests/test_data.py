import unittest
import datetime as dt
import re
import xarray as xr
from archapp.appliance import data
from archapp.util.dates import utc_delta

class ArchiveDataFuncTestCase(unittest.TestCase):
    def test_date_spec(self):
        regex = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z")
        for arg in (dt.datetime.now(),dt.datetime(2015, 1, 1),dt.datetime(2015, 1, 1)-utc_delta()):
            spec = data.date_spec(arg)
            match = regex.match(spec)
            self.assertTrue(match,
                "date_spec gives invalid arguments, such as {0} -> {1}".format(arg, spec))
        ans = "2015-01-01T00:00:00.000Z"
        spec = data.date_spec(dt.datetime(2015, 1, 1)-utc_delta())
        self.assertEqual(spec, ans,
            "utc offset is handled wrong in date_spec, expected {0} but got {1}".format(ans, spec))

    def test_make_url(self):
        url = data.make_url("base", "PV:NAME",
            dt.datetime(2015, 1, 1)-utc_delta(),
            dt.datetime(2016, 1, 1)-utc_delta())
        ans = "base?pv=PV:NAME&from=2015-01-01T00:00:00.000Z&to=2016-01-01T00:00:00.000Z&donotchunk"
        self.assertEqual(url, ans, "Make url is broken. Got {0}, expected {1}".format(url, ans))

    def test_make_xarray(self):
        # Just make sure we can take a reasonable input and return the right type
        data_source = {"data" : [{"fields" : {"DESC" : "fake!"},
                                  "nanos" : 0,
                                  "secs" : 10000,
                                  "severity" : 0, 
                                  "status" : 0,
                                  "val" : 125.43},
                                 {"fields" : {"DESC" : "fake!"},
                                  "nanos" : 0,
                                  "secs" : 20000,
                                  "severity" : 0, 
                                  "status" : 0,
                                  "val" : 126.43},
                                 {"fields" : {"DESC" : "fake!"},
                                  "nanos" : 0,
                                  "secs" : 30000,
                                  "severity" : 0, 
                                  "status" : 0,
                                  "val" : 127.43}],
                       "meta" : {"EGU" : "mm", "PREC" : 0, "name" : "FAKE:DATA"}}
        arr = data.make_xarray(data_source)
        self.assertIsInstance(arr, xr.DataArray)

class ArchiveDataClassTestCase(unittest.TestCase):
    def setUp(self):
        self.arch = data.ArchiveData()

    def test_get_raw(self):
        # We already tested the parts of this separately, just check that we
        # get a dictionary out.
        data = self.arch.get_raw("XPP:USR:MMS:01", dt.datetime(2016, 11, 10), dt.datetime(2016, 11, 11))
        self.assertIsInstance(data, dict, "get_raw returns type {0} instead of dict".format(type(data)))
        self.assertEqual(len(data.keys()), 2, "raw data has {0} keys, more than 2!".format(data.keys()))

    def test_get(self):
        # Make sure we get an xarray with multiple pvs
        data1 = self.arch.get("XPP:USR:MMS:01", dt.datetime(2016, 11, 10), dt.datetime(2016, 11, 11))
        data2 = self.arch.get(["XPP:USR:MMS:01", "XPP:USR:MMS:02", "XPP:USR:MMS:03"], dt.datetime(2016, 11, 10), dt.datetime(2016, 11, 11))
        self.assertIsInstance(data1, xr.DataArray, "get returns a {0} instead of a DataArray!".format(type(data)))
        self.assertIsInstance(data2, xr.Dataset, "get returns a {0} instead of a Dataset!".format(type(data)))
