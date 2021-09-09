archapp
=======

PCDS conda Python environments already include archapp.

In order to access the archiver interactively, use the following:

Source the environment first:
```bash
$ source /cds/group/pcds/pyps/conda/pcds_conda
```

And then start IPython:
```bash
$ ipython
```

Import a helper class that lets you access the archiver:

```python
from archapp.interactive import EpicsArchive
```

Now create a reusable object that will let you access our photon-side archiver:

```python
arch = EpicsArchive()
```

To get data, use the following:

```python
data = arch.get("pv_name", xarray=True)
```

It's recommended to use ``xarray=True`` in order to get an easy-to-use time series
array back.

To get the data as a pandas data frame, you can use:

```python
df = data.to_dataframe()
```

To get just values (or alarm status) from the data frame, use the following:
```python
df = data.to_dataframe()
values = df["pv_name"].vals
alarm_stat = df["pv_name"].stat
```

To resample the values to just once per day, interpolating linearly (common
alternative options may include "quadratic" or "cubic" or "nearest"):

```python
data.resample(time="1D").interpolate("linear")
```

To merge data from different PVs - using a real pair for example - one option
may be the following:

```python
In [1]: m1 = arch.get("AT2K2:L2SI:MMS:01.RBV", xarray=True).resample(time="1D").interpolate("linear").to_dataframe()

In [2]: m2 = arch.get("AT2K2:L2SI:MMS:02.RBV", xarray=True).resample(time="1D").interpolate("linear").to_dataframe()

In [3]: m1.merge(m2, left_index=True, right_index=True)[:10]
Out[3]:
                 AT2K2:L2SI:MMS:01.RBV AT2K2:L2SI:MMS:02.RBV
field time
vals  2021-08-09                26.994              27.71345
      2021-08-10                26.994              27.71345
      2021-08-11               26.9939              27.71345
      2021-08-12               26.9939              27.71345
      2021-08-13               26.9939               27.7134
      2021-08-14               26.9939              27.71325
      2021-08-15               26.9939              27.71335
      2021-08-16              26.99395              27.71335
      2021-08-17                26.994               27.7135
      2021-08-18                26.994              27.71345
```


Usage outside of PCDS environments
----------------------------------

Create a conda environment that uses python 3. Make sure xarray is installed in the conda environment.

Go to archapp/lib and type ``ipython`` in the command line.
