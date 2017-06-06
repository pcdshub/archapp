"""
command_line.py defines argument parsing for command-line utilities
"""
import sys
import argparse
from archapp.interactive import EpicsArchive
from archapp.dates import days_map

name = "arch_app"
arch = EpicsArchive()

units_doc = "Valid units are: " + ", ".join(sorted(days_map.keys())) + "."
units_doc = ", and ".join(units_doc.rsplit(",", 1))

parser = argparse.ArgumentParser(
    prog=name,
    description="Retrieve data from the Archiver Appliance for all input "
               +"pvnames. These pvnames may include glob wildcards.",
    epilog=units_doc,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("pvnames", nargs="+")
parser.add_argument("-a", default="print",
                    help="Either print, plot, or search.",
                    metavar="ACTION",
                    dest="action")
parser.add_argument("-s", default=30, type=float,
                    help="Define start time of query in units of time ago.",
                    metavar="START",
                    dest="start")
parser.add_argument("-e", default=0, type=float,
                    help="Define end time of query in units of time ago.",
                    metavar="END",
                    dest="end")
parser.add_argument("-u", default="days", type=str,
                    help="Unit of time for start and end parameters.",
                    metavar="UNIT",
                    dest="unit")
parser.add_argument("--chunk", action="store_const", const=True,
                    default=False,
                    help="Include this parameter to chunk data.")

# Set module doc for autodocumentation
__doc__ = \
"""
``{}`` is a command-line script for accessing archiver data.

**Usage:**

""".format(name) + parser.format_help()[7:]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = parser.parse_args()

        valid_actions = ("print", "plot", "search")
        valid_units = days_map.keys()
        if args.action not in valid_actions:
            print "Action parameter (-a) must be one of {}".format(valid_actions)
            exit()
        if args.unit not in valid_units:
            print "Units parameter (-u) must be one of {}".format(valid_units)
            exit()

        if args.action == "print":
            func = arch.prints
        else:
            func = getattr(arch, args.action)
        if func == arch.search:
            for name in args.pvnames:
                func(name)
        else:
            func(pvname=args.pvnames, start=args.start, end=args.end,
                 unit=args.unit, chunk=args.chunk)
