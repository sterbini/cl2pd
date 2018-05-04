'''
A simple package to convert CERN Logging information (using pytimber/CALS, mat-files, massi-files, TFS-files) 
into a pandas dataframe.

import cl2pd # do "pip install --user git+https://github.com/sterbini/cl2pd.git" to install
from cl2pd import importData
from cl2pd import plotFunctions
import matplotlib.pyplot as plt
pd=importData.pd     # is the pandas package
np=importData.np     # is the numpy package
cals=importData.cals # pytimber log class
get_ipython().magic('matplotlib inline')
%config InlineBackend.figure_format = 'retina' # retina display
# mySource='string with full notebook address used to comment plots'
'''


class dotdict(dict):
    '''
    A dict with dot access and autocompletion.
    
    HINT: use as keys string starting with 'at' or 'b' to ease the autocompletion from the drop down menu. 

    The idea and most of the code was taken from 
    http://stackoverflow.com/a/23689767,
    http://code.activestate.com/recipes/52308-the-simple-but-handy-collector-of-a-bunch-of-named/
    http://stackoverflow.com/questions/2390827/how-to-properly-subclass-dict-and-override-get-set
    
    ===Example===     

    a=dotdict()
    for i in {'B1','B2'}:
        a[i]=dotdict()
        for j in range(100):
            a[i]['b'+str(j)]=np.random.randn(10)
    '''
    
    def __init__(self,*a,**kw):
        dict.__init__(self)
        self.update(*a, **kw)
        self.__dict__ = self
    
    def __setattr__(self, key, value):
        if key in dict.__dict__:
            raise AttributeError('This key is reserved for the dict methods.')
        dict.__setattr__(self, key, value)
    
    def __setitem__(self, key, value):
        if key in dict.__dict__:
            raise AttributeError('This key is reserved for the dict methods.')
        dict.__setitem__(self, key, value)
        
    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v
        
    def __getstate__(self):
        return self
 
    def __setstate__(self, state):
        self.update(state)
        self.__dict__ = self
        
    
