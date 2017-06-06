import unittest
import time
import datetime as dt

from archapp.util import dates

class DatesTestCase(unittest.TestCase):
    def test_utc_delta_type(self):
        delta = dates.utc_delta()
        err = "utc_delta returns type {0} instead of {1}"
        self.assertIsInstance(delta, dt.timedelta,
            err.format(type(delta), dt.timedelta))

    def test_utc_delta_sanity(self):
        delta = dates.utc_delta()
        self.assertEqual(delta, dates.utc_delta(),
            "utc_delta not cached properly")
        result = delta.seconds/3600
        possible_results = [time.timezone/3600]
        if time.daylight:
            possible_results.append(time.altzone/3600)
        err = "utc_delta yeilds impossible value {0}. Should be among {1}"
        self.assertIn(result, possible_results,
            err.format(result, possible_results))
