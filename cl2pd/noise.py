"""
In this module we will put the functions needed for the noise analysis
"""
import numpy as np
import pandas as pd
import glob  
import os
import dotdict

def fromName2Timestamp(myString,tz_start='CET',tz_end='UTC'):
    """
    Convert a file path in a pd.Timestamp. 
    tz_start: the initial tz
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
    """
    myDATA=dotdict.dotdict()
    for i in ['current','voltage']:
      myFileList=glob.glob(folderName+'/*'+i)
      myTimestampList=[]
      for fileName in myFileList:
          myTimestampList.append(fromName2Timestamp(fileName))
      myDATA['at'+i]=pd.DataFrame(index=myTimestampList)
      myDATA['at'+i]['fileName']=myFileList
    return myDATA
