
import cl2pd # do "pip install --user git+https://github.com/sterbini/cl2pd.git" to install
from cl2pd import importData
from cl2pd import plotFunctions
from cl2pd import dotdict
from cl2pd import variablesDF

dotdict=dotdict.dotdict
pd=importData.pd     # is the pandas package
np=importData.np     # is the numpy package
cals=importData.cals # pytimber log class

import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
%config InlineBackend.figure_format = 'retina' # retina display

import pjlsa
lsa = pjlsa.LSAClient()
