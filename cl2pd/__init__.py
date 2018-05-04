'''
A simple package to convert CERN Logging information (using pytimber/CALS, mat-files, massi-files, TFS-files) 
into a pandas dataframe.

Here you are an header example:

import cl2pd # do "pip install --user git+https://github.com/sterbini/cl2pd.git" to install
from cl2pd import importData
from cl2pd import plotFunctions
from cl2pd import dotdict
dotdict

pd=importData.pd     # is the pandas package
np=importData.np     # is the numpy package
cals=importData.cals # pytimber log class

import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
%config InlineBackend.figure_format = 'retina' # retina display
# mySource='string with full notebook address used to comment plots'
'''
