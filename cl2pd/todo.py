##### TODO ####

import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
import os
plt.plot([1,2,3,])
plt.text(0.99,0.01,os.getcwd()+'/Test.ipynb', 
         horizontalalignment='right', 
         color='lightgray',
         verticalalignment='bottom', 
         transform=plt.gca().transAxes,rotation=0, fontsize=7)
