import unittest
from archapp.appliance import config
from archapp.util import url as url_utils

sample_good_url = "http://pscaa02:17668/retrieval/data/getData.json?pv=XPP:USR:MMS:01&from=2016-11-11T20:23:03.000Z&to=2016-11-11T20:24:03.000Z&donotchunk"

sample_404 = sample_good_url.replace("XPP", "asdfebk")

sample_no_connect = "http://xpp-monitor:17668/retrieval/data/getData.json?pv=XPP:USR:MMS:01&from=2016-11-11T20:23:03.000Z&to=2016-11-11T20:24:03.000Z&donotchunk"

class UrlJsonCase(unittest.TestCase):
    def test_url_basic_quote(self):
        url = url_utils.url_quote(sample_good_url)
        expected = "http://pscaa02:17668/retrieval/data/getData.json?pv=XPP%3AUSR%3AMMS%3A01&from=2016-11-11T20%3A23%3A03.000Z&to=2016-11-11T20%3A24%3A03.000Z&donotchunk"
        self.assertEqual(url, expected, "Not quoting reserved characters properly. Expected {0} but got {1}".format(expected, url))

    def test_url_normal_get(self):
        data = url_utils.get_json(sample_good_url)
        self.assertIsInstance(data, dict,
            "Did not get a dictionary! Got {} instead!".format(type(data)))
        self.assertTrue(data, "No data! {}".format(data))

    def test_url_bad_pv(self):
        data = url_utils.get_json(sample_404)
        self.assertFalse(data, "We got data... How??? {}".format(data))

    def test_url_no_connect(self):
        data = url_utils.get_json(sample_no_connect)
        self.assertFalse(data, "We got data... How??? {}".format(data))

    def test_url_base(self):
        host = "localhost"
        port = 12345
        ext = "/test/test"
        url = url_utils.arch_url(host, port, ext)
        ans = "http://localhost:12345/test/test"
        self.assertEqual(url, ans, 
            "wrong url, expected {0} but got {1}".format(ans, url))
