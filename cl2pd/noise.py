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
    
def importEmptyDF(folderName,startFile=0,endFile=-1):
    """
    Import the list of the EPC acquisition stored in folderName.
    One can select the list of files to consider in folderName by startFile and endFile.
    ===EXAMPLE===
    from cl2pd import noise
    myDict=noise.importEmptyDF('/eos/project/a/abpdata/lhc/rawdata/power_converter')
    """
    myDATA=dotdict.dotdict()
    for i,j in zip(['current','voltage'],['Current','Voltage']):
      myFileList=glob.glob(folderName+'/*'+i)
      myFileList=myFileList[startFile:endFile]
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

class DOROS:
    """
    Script converted from Mathematica (from Jakub Olexa) to Python
    ===EXAMPLE===
    path = '/eos/user/s/skostogl/SWAN_projects/Noise/DOROS_data/181025'
    doros = DOROS(path)
    myDict= doros.importEmptyDF
    pu = 'rr13'
    myDF=myDict.atDOS['%s' %pu].head(5).copy()
    myDF = myDF['fileName'].apply(doros.loadData)
    """
    def __init__(self,folderName):
        """
        Import the list of the DOROS acquisitions during MD4147. Sort by DOR (orbit) and DOS(oscillations) and by name of BPM. The final DataFrame will be: *.at*(DOS or DOR).*(name of BPM)
        ===EXAMPLE===
        from cl2pd import noise
        doros = noise.DOROS(/eos/user/s/skostogl/SWAN_projects/Noise/DOROS_data/181025)
        myDict= noise.doros.importEmptyDF
        """
        myDATA=dotdict.dotdict()
        for i,j in zip(['ORB','OSC'],['DOR','DOS']):
          myFileList=glob.glob(folderName+'/%s*'%i)
          unique_bpms = self.fromName2BPM(myFileList)
          myTimestampList=[]
          bpms = []
          for fileName in myFileList: 
              myTimestampList.append(self.fromName2Timestamp(fileName))
              bpms.append(self.fromName2BPM(fileName))
          myDATA['at'+j] = dotdict.dotdict() 
          for bpm in unique_bpms:
            idx = [a for a,b in enumerate(bpms) if b == bpm]     
            myDATA['at'+j][bpm]=pd.DataFrame(index=np.array(myTimestampList)[idx])
            myDATA['at'+j][bpm]['fileName']=np.array(myFileList)[idx]
        self.importEmptyDF = myDATA
        
    def fromName2BPM(self, myString):
        """
        Find names of BPMs. If myString is a list, the unique BPM names are returned.
        ===EXAMPLE===
        from cl2pd import noise
        myString = 'OSC_TbT_cfb-rr17-bidrs1_2018_10_25-00_43_33.bin'
        fromName2BPM(myString)
        """
        if isinstance(myString, list):
          bpms = []
          for i in myString:
            bpms.append(i.split('/')[-1].split('_')[2].split('-')[1])
          return np.unique(bpms)
        else:
          return myString.split('/')[-1].split('_')[2].split('-')[1]
    
    def fromName2Timestamp(self,myString,tz_start='CET',tz_end='UTC'):
        """
        Convert a file path in a pd.Timestamp. 
        tz_start: the initial tz.
        tz_end: the tz of the returned pd.Timestamp.
        ====
        EXAMPLE:
        myString='eos/user/s/skostogl/SWAN_projects/Noise/DOROS_data/181025/OSC_TbT_cfb-rr17-bidrs1_2018_10_25-00_43_33.bin'
        fromName2Timestamp(myString)
        """
        [a,b,c,d,e]=myString.split('/')[-1].split('_')[3:]       
        aa=a[:2]+'-'+a[2:5] + '-'+a[5:9]+' '
        aa=  c[:2] + '-' + b + '-' + a+' '      
        
        return pd.Timestamp(aa + c[3:] +':' + d+':'+ e.split('.')[0]).tz_localize(tz_start).tz_convert(tz_end)    
    
    def preprocess_data(self, Data, key='DOS'):
        """
        key=DOR: Returns FFT [units are normalized position]
        key=DOS: Returns tbt data [units are relative position values]
        """
        B1ChanDec    = Data[5] & (2**8-1)
        B2ChanDec    = (Data[5] & (2**8-1)*2**16)/2**16
        B1NumofChan  = Data[6] & (2**8-1)
        B2NumofChan  = (Data[6] & (2**8-1)*2**16)/2**16
        Fullscale32b = (2**32)-1
        CaptureDecimationFactor = B1ChanDec
        HeaderOffset = 8
        Numofsamples = Data[7]
        if key == 'DOS':
            ADCB1dosCHdata = []
            for i in range(0, B1NumofChan):
              ADCB1dosCHdata.append(Data[HeaderOffset  + i*Numofsamples: HeaderOffset + Numofsamples + i*Numofsamples]*1.0/Fullscale32b)
            ADCB2dosCHdata = []
            for i in range(0, B2NumofChan):
              ADCB2dosCHdata.append(Data[HeaderOffset + B1NumofChan*Numofsamples + i*Numofsamples: HeaderOffset + B1NumofChan*Numofsamples + Numofsamples + i*Numofsamples]*1.0/Fullscale32b)
            B1oscH = ADCB1dosCHdata[0] - np.mean(ADCB1dosCHdata[0])
            B1oscV = ADCB1dosCHdata[1] - np.mean(ADCB1dosCHdata[1])
            B2oscH = ADCB2dosCHdata[0] - np.mean(ADCB2dosCHdata[0])
            B2oscV = ADCB2dosCHdata[1] - np.mean(ADCB2dosCHdata[1])
            return pd.Series([B1oscH, B1oscV, B2oscH, B2oscV], index = ['Data_B1H', 'Data_B1V', 'Data_B2H', 'Data_B2V'])
        else:
            ADCB1dorCHdata = []
            for i in range(0, B1NumofChan):
              ADCB1dorCHdata.append(Data[HeaderOffset  + i*Numofsamples: HeaderOffset + Numofsamples + i*Numofsamples]*1.0/Fullscale32b)
            ADCB2dorCHdata = []
            for i in range(0, B2NumofChan):
              ADCB2dorCHdata.append(Data[HeaderOffset + B1NumofChan*Numofsamples + i*Numofsamples: HeaderOffset + B1NumofChan*Numofsamples + Numofsamples + i*Numofsamples]*1.0/Fullscale32b)
            ## BPM electrode channels
            B1eleH1 = ADCB1dorCHdata[0]
            B1eleH2 = ADCB1dorCHdata[1]
            B1eleV1 = ADCB1dorCHdata[2]
            B1eleV2 = ADCB1dorCHdata[3]
            B2eleH1 = ADCB2dorCHdata[0]
            B2eleH2 = ADCB2dorCHdata[1]
            B2eleV1 = ADCB2dorCHdata[2]
            B2eleV2 = ADCB2dorCHdata[3]
            ## HV orbit position change
            B1orbH = (B1eleH1-B1eleH2)/(B1eleH1+B1eleH2)
            B1orbV = (B1eleV1-B1eleV2)/(B1eleV1+B1eleV2)
            B1orbHmean = np.mean(B1orbH)
            B1orbVmean = np.mean(B1orbV)
            B2orbH = (B2eleH1-B2eleH2)/(B2eleH1+B2eleH2)
            B2orbV = (B2eleV1-B2eleV2)/(B2eleV1+B2eleV2)
            B2orbHmean = np.mean(B2orbH)
            B2orbVmean = np.mean(B2orbV)
            ## HV orbit spectra
            elecdist = 0.061
            PUgain   = elecdist/4.
            FsamADC  = 400.8*1e6/35640
            B1orbHFFT = 2.0*abs(np.fft.fft(PUgain*(B1orbH-B1orbHmean)*np.hanning(len(B1orbH))))
            B1orbHFFT /= len(B1orbHFFT)
            B2orbHFFT = 2.0*abs(np.fft.fft(PUgain*(B2orbH-B2orbHmean)*np.hanning(len(B2orbH))))
            B2orbHFFT /= len(B2orbHFFT)
            B1orbVFFT = 2.0*abs(np.fft.fft(PUgain*(B1orbV-B1orbVmean)*np.hanning(len(B1orbV))))
            B1orbVFFT /= len(B1orbHFFT)
            B2orbVFFT = 2.0*abs(np.fft.fft(PUgain*(B2orbV-B2orbVmean)*np.hanning(len(B2orbV))))
            B2orbVFFT /= len(B2orbVFFT) 
            n = len(B1orbH)
            freqs = np.arange(0, n)*FsamADC/n
            return pd.Series([B1orbHFFT, B1orbVFFT, B2orbHFFT, B2orbVFFT, freqs], index = ['Spectrum_B1H', 'Spectrum_B1V', 'Spectrum_B2H', 'Spectrum_B2V', 'Frequencies'])
        
    def loadData(self,fileName):
        """
        Load data from the binary fileName.         
        -DOR read as unsigned 32 bit Integers
        -DOS read as signed 32 bit Integers
        -Pseudoheader unsigned 32 bit
        ===EXAMPLE===
        from cl2pd import noise
        myData=noise.doros.loadData('/eos/user/s/skostogl/SWAN_projects/Noise/DOROS_data/181025/OSC_TbT_cfb-rr13-bidrs1_2018_10_25-00_43_33.bin')
        """
        f = open(fileName, "r")
        if 'ORB' in fileName:
          Data = np.fromfile(f, dtype=np.uint32)
          return pd.concat([pd.Series({'fileName': fileName}) ,self.preprocess_data(Data, key='DOR')])
        else:
          Data = np.fromfile(f, dtype=np.int32) 
          return pd.concat([pd.Series({'fileName': fileName}) ,self.preprocess_data(Data, key='DOS')])
