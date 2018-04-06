# cl2pd
A simple package to convert CERN Logging information (using pytimber/CALS, mat-files, massi-files, TFS-files) into pandas dataframes.

## Install the package
You can install the package, for instance on the SWAN terminal (www.swan.cern.ch), using:
```
pip install --user git+https://github.com/sterbini/cl2pd.git
```

## Example notebook 
Please have a look to this example file

/eos/user/s/sterbini/MD_ANALYSIS/cl2pdExaple.ipynb 

or follow the link

https://cernbox.cern.ch/index.php/s/FwLf6IDEJ6Ypdke

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

