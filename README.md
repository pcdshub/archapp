How to use archapp:

Create a conda environment that uses python 3. Make sure xarray is installed in the conda environment.

Go to archapp/lib and type ipython in the command line.

```python
#Type: 
from archapp.interactive import EpicsArchive

#Now create an object ---> 
arch = EpicsArchive()

#To get data, use --> 
data = arch.get("pv_name", xarray=True)

#To get the data in a data frame format --> 
data.to_dataframe()

#To get values of the data frame, such as vals or stat, for example --> 
data.to_dataframe()['pv_name']['vals']
```
