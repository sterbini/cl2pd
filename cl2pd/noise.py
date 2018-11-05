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
import h5py as h5

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


class ADT:
    """
    ===EXAMPLE===
    path = '/eos/user/s/skostogl/SWAN_projects/Noise/ADTObsObox/'
    adt = ADT(path)
    myDict = adt.importEmptyDF
    myDF = myDict.atB1H.copy()
    myDF['Data'] = myDF['fileName'].apply(adt.loadData)
    """
    def __init__(self,folderName):
        myDATA=dotdict.dotdict()
        for x in (['B1H', 'B1V','B2H', 'B2V']):
          myFileList=glob.glob(folderName + '/*%s*.h5' %x)
          myTimestampList=[]
          pus = []
          status = []
          if myFileList:
            fills = np.unique([int(filename.split('/')[-1].split('_')[0]) for filename in myFileList])
            df = {}
            for fill in fills:
                df[fill] = importData.LHCFillsByNumber(fill)
                df[fill] = df[fill][df[fill]['mode']!='FILL']
                df[fill] = df[fill].reset_index(drop=True)
          for fileName in myFileList:
            fill  = int((fileName.split('/')[-1].split('_'))[0])
            time  = self.fromName2Timestamp(fileName.split('/')[-1])
            status.append(self.getStatus(time,fill, df))
            myTimestampList.append(time)
            pus.append(self.fromName2PU(fileName.split('/')[-1]))    
          myDATA['at'+x]=pd.DataFrame(index=np.array(myTimestampList))
          myDATA['at'+x]['fileName']=np.array(myFileList)
          myDATA['at'+x]['Status'] = status
          myDATA['at'+x]['PU'] = pus
        self.importEmptyDF = myDATA
    
    def getStatus(self,time,fill_number, fills):
        df = fills[fill_number]
        return    df[(df['startTime']<=time)  & (df['endTime']>=time)]['mode'].values[0]  
    
    def fromName2PU(self, myString):
        return myString.split('/')[-1].split('_')[3]
    
    def fromName2Timestamp(self,myString,tz_start='CET',tz_end='UTC'):
        [a,b]=myString.split('/')[-1].split('_')[4:]       
        aa=a[:4]+'-'+a[4:6] + '-'+a[6:]+' '
        bb=  b[:2] + ':' + b[3:5] + ':' + b[6:8]+' '  
        return pd.Timestamp(aa + bb).tz_localize(tz_start).tz_convert(tz_end)    
        
    def loadData(self,fileName):
        fi = h5.File(fileName, 'r')
        beam  = (fileName.split('_')[-4])[0:2]
        plane = (fileName.split('_')[-4])[2:3]
        if plane == 'H':
          plane = 'horizontal'
        else:
          plane = 'vertical'   
        alldat = fi[beam][plane]
        print 'Buffer: Turns = %s, Bunches = %s' %(alldat.shape[0], alldat.shape[1])
        return alldat[:]

class BBQ:
    """
    HS BBQ data and frev interpolated. 
    Input: a list of tuples [(t_interval1_start, t_interval1_end), (t_interval2_start, t_interval2_end)...]
    Output: dotdict with keys :atB1H, atB2H, atB1V, atB2V
    === EXAMPLE ===
    time_list = [(pd.Timestamp('2018-10-25 22:43:33+00:00'), pd.Timestamp('2018-10-25 22:43:50+00:00'))  ]
    bbq = BBQ()
    df = bbq.getData(time_list)
    """

    def FindStatus(self,time):
        return importData.LHCInstant(time)['mode'].values[0]

    def flattenoverlap(self, v,timestamps, frf,test=100,start=0):
      """
      Remove overlap in BBQ data, from pytimber https://github.com/rdemaria/pytimber
      """
      out=[v[0]]
      out2=[timestamps[0] for i in v[0]]
      out3=[frf[0] for i in v[0]]
      stat=[]
      for j in range(1,len(v)):
        v1=v[j-1]
        v2=v[j]
        newi=0
        for i in range(start,len(v2)-test):
          s=sum(v1[-test:]-v2[i:i+test])
          if s==0:
            newi=i+test
            break
        if newi==0:
          print("Warning: no overlap for chunk %d,%d"%((j-1,j)))
        out.append(v2[newi:])
        out2.append([timestamps[j] for k in v2[newi:]])
        out3.append([frf[j] for k in v2[newi:]])
        stat.append(newi)
      return np.hstack(out), np.hstack(out2), np.hstack(out3)

    def getData(self, time_list, return_status = False, for_beam='both', for_plane='both', remove_overlap=False, span = 3, buffer_size=2048, skip=0):

        df = dotdict.dotdict()
        if for_beam == 'both':
          beams  = ['B1', 'B2']
        else:
          beams = [for_beam]
        if for_plane == 'both':
          planes = ['H', 'V']
        else:
          planes = [for_plane]

        for beam in beams:
          for plane in planes:
            df['at%s%s' %(beam, plane)] = pd.DataFrame()
            var = ['LHC.BQBBQ.CONTINUOUS_HS.%s:ACQ_DATA_%s' % (beam, plane), 'ALB.SR4.%s:FGC_FREQ' % beam]
            for time in time_list:
              raw_data = importData.cals2pd(var, time[0], time[1])
              if return_status:
                raw_data['status'] = raw_data.index.map(FindStatus)
              raw_data[var[1]] = raw_data[var[1]].interpolate(limit_direction='both')
              raw_data['frev'] = raw_data[var[1]]/35640.
              raw_data.dropna(subset=[var[0]], inplace=True)
              raw_data['shape'] = raw_data[var[0]].apply(lambda x: len(x))
              raw_data = raw_data[raw_data['shape'] == buffer_size]

              if not remove_overlap:
                df['at%s%s' %(beam, plane)] = pd.concat([df['at%s%s' %(beam, plane)], raw_data])      
              elif not raw_data.empty:### Remove overlap
                data = []
                for i in raw_data[var[0]]:
                  data.append(i)
                to_flatten = tuple([np.array(raw_data.index), np.array(data), np.array(raw_data[var[1]])]) 
                test={var[0]:to_flatten}
                flatten={}
                for name,(timestamps,values, values2) in test.items():
                  flatten[name], timestamps2, frf2=flattenoverlap(values, timestamps, values2)
                step=1 + skip
                n = span*buffer_size
                turns = np.arange(0, len(flatten[var[0]]))
                chunk_t = [turns[x] for x in xrange(0, len(turns)-n, step)]
                chunk_var = [flatten[var[0]][x:x+n] for x in xrange(0, len(flatten[var[0]])-n, step)]
                chunk_time = [timestamps2[x] for x in xrange(0, len(timestamps2)-n, step)]
                chunk_frf = [frf2[x] for x in xrange(0, len(frf2)-n, step)]
                raw_data2 = pd.DataFrame({ var[0]:chunk_var, 'turns':chunk_t, var[1]: chunk_frf }, index=chunk_time )
                raw_data2['frev'] = raw_data2[var[1]]/35640.
                raw_data2['shape'] = raw_data2[var[0]].apply(lambda x: len(x))
                df['at%s%s' %(beam, plane)]= raw_data2
        return df 


