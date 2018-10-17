"""
In this module we will put the functions needed for the noise analysis.
===EXAMPLE===
from cl2pd import noise
myDict=noise.importEmptyDF('/eos/project/a/abpdata/lhc/rawdata/power_converter')
myDF=myDict.atCurrent.head(5).copy() # one can filter in a smarter way usign the cl2pd.importData methods.
myDF['data']=myDF['fileName'].apply(noise.loadData)
"""
import numpy as np
import pandas as pd
import glob  
import os
import dotdict

def fromName2Timestamp(myString,tz_start='CET',tz_end='UTC'):
    """
    Convert a file path in a pd.Timestamp. 
    tz_start: the initial tz.
    tz_end: the tz of the returned pd.Timestamp.
    ====
    EXAMPLE:
    myString='/eos/project/a/abpdata/lhc/rawdata/power_converter/05Oct2018_21_15_36_current'
    fromName2Timestamp(myString)
    """
    [a,b,c,d,e]=myString.split('/')[-1].split('_')
    aa=a[:2]+'-'+a[2:5] + '-'+a[5:9]+' '
    return pd.Timestamp(aa + b+':' + c+':'+ d).tz_localize(tz_start).tz_convert(tz_end)
    
def importEmptyDF(folderName):
    """
    Import the list of the EPC acquisition stored in folderName.
    ===EXAMPLE===
    from cl2pd import noise
    myDict=noise.importEmptyDF('/eos/project/a/abpdata/lhc/rawdata/power_converter')
    """
    myDATA=dotdict.dotdict()
    for i,j in zip(['current','voltage'],['Current','Voltage']):
      myFileList=glob.glob(folderName+'/*'+i)
      myTimestampList=[]
      for fileName in myFileList:
          myTimestampList.append(fromName2Timestamp(fileName))
      myDATA['at'+j]=pd.DataFrame(index=myTimestampList)
      myDATA['at'+j]['fileName']=myFileList
    return myDATA

def loadData(fileName):
    """
    Load data from the fileName. It returns a numpy.ndarray.
    ===EXAMPLE===
    from cl2pd import noise
    myData=noise.loadData('/eos/project/a/abpdata/lhc/rawdata/power_converter/05Oct2018_20_57_24_current')
    """
    return np.reshape(pd.read_csv(fileName,sep='\t',header=None).as_matrix(),1000000,1)
