"""
mgmt.py defines pv management interface
"""


from . import config
from .doc_sub import doc_sub
from .print_formats import list_print
from .url import arch_url, get_json, PV_ARG
from .url import hostname_doc, mgmt_port_doc

MGMT_URL = "/mgmt/bpl/"

class ArchiveMgmt(object):
    """
    Class to get metadata and manage pvs in the archiver.
    """
    @doc_sub(hostname=hostname_doc, mgmt_port=mgmt_port_doc)
    def __init__(self, hostname=config.hostname, mgmt_port=config.mgmt_port):
        """
        Parameters
        ----------
        {hostname}
        {mgmt_port}
        """
        self.base_url = arch_url(hostname, mgmt_port, MGMT_URL)

    def search_pvs(self, glob, do_print=True):
        """ 
        Queries the archiver with a PV search using glob format.

        Parameters
        ----------
        glob : string
            glob search string to look into the archiver
        do_print : bool, optional
            If True, prints the PVs nicely on your screen.
            If False, returns the list of PVs.

        Returns
        -------
        pvs : list of string
            All pvs that match the glob search. Can be an empty list.
        """
        url = self.base_url + "getAllPVs"
        url += PV_ARG.format(glob)
        # Increase timeout on search calls because they take approx 5-6 secs
        # Call time is mostly independent of which glob we use
        pvs = get_json(url, timeout=10)
        if not pvs:
            pvs = []
        if do_print:
            success = list_print(pvs)
            if not success:
                print("No PVs found.")
        else:
            return pvs
