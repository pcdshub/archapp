"""
url.py defines basic url utilities
"""

import signal
import urllib.request, urllib.parse, urllib.error
try: import simplejson as json
except: import json
from .doc_sub import doc_sub

PV_ARG = "?pv={0}"
URL_ARG = "&{0}={1}"
URL_FLAG = "&{0}"

hostname_doc = \
"""
hostname : string
    archiver appliance host
"""

data_port_doc = \
"""
data_port : int
    port on host that has the retrieval directory
"""

mgmt_port_doc = \
"""
mgmt_port : int
    port on host that has the mgmt directory
"""

@doc_sub(hostname=hostname_doc)
def arch_url(hostname, port, ext):
    """
    Return the base url for a particular archiver service.

    Parameters
    ----------
    {hostname}
    port : int
        port on host that has the ext directory
    ext : string
        directory that hosts the desired service
    """
    return "http://" + hostname + ":" + str(port) + ext

def get_json(url, timeout=1):
    """
    Makes the URL request and interprets it as a json file.
    Formats the url, quoting the reserved characters appropriately.
    Returns an empty dictionary if no data is found, and prints an
    appropriate explanation.

    Parameters
    ----------
    url : string
        url that will point us to a json data dictionary

    Returns
    -------
    data : dict or list
        json data
    """
    url = url_quote(url)
    signal.signal(signal.SIGALRM, _raise_timeout)
    signal.alarm(timeout)
    try:
        http = urllib.request.urlopen(url)
    except (UrlTimeout, IOError):
        print("No conection to archiver.")
        return {}
    finally:
        signal.alarm(0)
    if check_error(http):
        return {}
    data = json.load(http)
    http.close()
    if isinstance(data, list) and len(data) == 1 and isinstance(data[0], dict):
        return data[0]
    else:
        return data

def url_quote(url):
    """
    Properly quotes reserved characters for the http request.

    Parameters
    ----------
    url : string
        any valid request url

    Returns
    -------
    url : string
        url with properly quoted reserved characters
    """
    parts = url.split("?")
    parts[1] = urllib.parse.quote(parts[1], safe="=&")
    url = "?".join(parts)
    return url

def check_error(http):
    """
    Checks for http errors (400 series) and returns True if an error exists.

    Parameters
    ----------
    http : addinfourl whose fp is a socket._fileobject

    Returns
    -------
    has_error : bool
    """
    err = http.code
    if 400<= err < 500:
        print("HTTP error {}. Make sure your PV exists.".format(err))
        return True
    return False

def _raise_timeout(signum, frame):
    raise UrlTimeout()

class UrlTimeout(Exception):
    pass
