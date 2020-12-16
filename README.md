# cl2pd
A simple package to convert CERN Logging information (using pytimber/CALS, mat-files, massi-files, TFS-files) into a pandas dataframe. 

This data type is very convenient to represent time series and it offers a large set of methods to manage missing data, to do data aggregation and group operation, to perform data wrangling, to handle timezones, to plots data, etc...
For a schematic and succinct introduction to pandas please refers for example to 
http://datasciencefree.com/pandas.pdf.

An important source of inspiration was the package **pytimber** by R. De Maria et al. and their generous approach in sharing tools and foster collaborations.

## Install the package
You can install the package, for instance on the SWAN terminal (www.swan.cern.ch), using:
```
pip install --user git+https://github.com/sterbini/cl2pd.git
```
or to upgrade it
```
pip install --upgrade --user git+https://github.com/sterbini/cl2pd.git
```
or to upgrade a fork of the project
```
pip install --upgrade --user git+https://github.com/sterbini/cl2pd.git@fork_name
```

## Example notebook 
Please have a look to this example file

/eos/user/s/sterbini/MD_ANALYSIS/cl2pdExample.ipynb 

or follow the link

https://cernbox.cern.ch/index.php/s/2X6nUheIdfl8sFq

## Minimal example

```python
import cl2pd
from cl2pd import importData
pd=importData.pd     #is the pandas package

variables=['LHC.BCTDC.A6R4.B1:BEAM_INTENSITY', 'LHC.BCTDC.A6R4.B2:BEAM_INTENSITY']
startTime = pd.Timestamp('2017-10-01 17:30', tz='CET')
endTime = pd.Timestamp('2017-10-01 17:31', tz='CET')
raw_data = importData.cals2pd(variables,startTime,endTime)
raw_data.head()
```

