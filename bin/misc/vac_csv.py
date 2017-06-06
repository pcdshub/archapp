"""
Get csv of 1 month of FEE vac parameters
"""
import sys
import os
import datetime
from archapp.file_formats import load_pvnames, csv_coll, build_csv
from archapp.interactive import EpicsArchive

arch = EpicsArchive()
folder = os.path.dirname(__file__)
#pvs = load_pvnames(os.path.join(folder, "short.txt"))
pvs = load_pvnames(os.path.join(folder, "pvlist.txt"))

colls = []
end = datetime.datetime.now()
delta = datetime.timedelta(days=31)
start = end - delta

max_attempts = 5
for pv in pvs:
    attempts = max_attempts
    while attempts > 0:
        try:
            #data = arch.get(pv, start=1, unit="month", xarray=True)
            data = arch.get(pv, start=start, end=end, xarray=True)
            if len(data) > 0:
                attempts = 0
            else:
                attempts -= 1
        except:
            attempts -= 1
    if len(data[pv][0].values) > 700:
        coll = csv_coll(data, pv, "hour")
    else:
        coll = csv_coll(data, pv)
    colls.append(coll)

#build_csv(colls, filename="test.csv")
build_csv(colls, filename="fee_vac_arch_export_{0}-{1}-{2}.csv".format(end.year, end.month, end.day))
