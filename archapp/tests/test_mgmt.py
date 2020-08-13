import unittest
from archapp.appliance import mgmt

class ArchiveMgmtTestCase(unittest.TestCase):
    def setUp(self):
        self.arch = mgmt.ArchiveMgmt()

    def test_search_pv(self):
        pvs = self.arch.search_pvs("XPP:USR:MMS:0?", do_print=False)
        err = "Got {0} pvs instead of {1} in search for 'XPP:USR:MMS:0?'"
        self.assertEqual(len(pvs), 9, err.format(len(pvs), 9))

    def test_search_bad_pv(self):
        pvs = self.arch.search_pvs("junkjunktestjunk", do_print=False)
        self.assertEqual(pvs, [],
            "Recieved {0} instead of empty list!".format(pvs))

    def test_search_print_no_crash(self):
        pvs = self.arch.search_pvs("", do_print=True)
        pvs = self.arch.search_pvs("XPP:USR:MMS:01", do_print=True)

class ArchiveMgmtBadTestCase(unittest.TestCase):
    def test_search_bad_hostname(self):
        arch = mgmt.ArchiveMgmt(hostname="bacon_test")
        pvs = arch.search_pvs("XPP:USR:MMS:0?", do_print=False)
        self.assertEqual(pvs, [], "We did not fail gracefully with an empty list")

    def test_search_bad_port(self):
        arch = mgmt.ArchiveMgmt(mgmt_port=99999999999)
        pvs = arch.search_pvs("XPP:USR:MMS:0?", do_print=False)
        self.assertEqual(pvs, [], "We did not fail gracefully with an empty list")
