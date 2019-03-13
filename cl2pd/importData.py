import pandas as pd 
import numpy as np
import os
import inspect
# Fundamental contribution by R. De Maria et al.
import pytimber
from . import dotdict
#For the dBLM2pd
import h5py


dotdict=dotdict.dotdict

# TODO: discuss about the possible problem if the user has already defined a variable named 'cals' 
cals=pytimber.LoggingDB()

def _smartList(myList):
    '''
    Return a list with no duplicate and resolve the '%' search pattern.
    
    ===Example===
    _smartList(['CPS.LSA:%','TFB-DSPU-%-NEW:OPERATION:BLOWUPENABLE'])
    _smartList('CPS.LSA:%')

    '''
    if isinstance(myList,str):
        if '%' in myList:
            return cals.search(myList)
        else:
            return [myList]
    
    newList=[]
    for i in myList:
        if '%' in i:
            newList=newList+cals.search(i)
        else:
            newList=newList+[i]
    return list(np.unique(newList))

def _noSplitcals2pd(listOfVariables, t1, t2, fundamental='', verbose=False):
    '''
    It is a cals2pd without splitting feature.

    This function is supposed to be private.

    t1 and t2 are pandas datetime, therefore you can use tz-aware expression.
    Tz-naive expressions will be consider UTC-localized.

    This function returns a pandas dataframe of the listOfVariables within the interval [t1,t2].
    It can be used in the verbose mode if the corresponding flag is True.
    It can be used to filter fundamentals (especially intended for the injectors).
    The index timestamps of the output are UTC-localized.
    '''

    if len(listOfVariables)==0:
        return pd.DataFrame()
    
    listOfVariables=_smartList(listOfVariables)
    
    if t1.tz==None:
        t1=t1.tz_localize('UTC')
        if verbose: print(('t1 is UTC localized: ' + str(t1)))

    # pyTimber needs CET as internal variable
    t1=t1.astimezone('CET')

    if not isinstance(t2, str):
        if t2.tz==None:
            t2=t2.tz_localize('UTC')
            if verbose: print(('t2 is UTC localized: '+ str(t2)))
        # pyTimber needs CET as internal variable
        t2=t2.astimezone('CET')

        
    # Retrieving the variables
    listOfVariableToAdd=list(set(listOfVariables))
    if fundamental=='':
        if verbose: print('No fundamental filter.')
        DATA=cals.get(listOfVariableToAdd,t1,t2 )
    else:
        DATA=cals.get(listOfVariableToAdd,t1,t2,fundamental)
    myDataFrame=pd.DataFrame()

    if DATA!={}:
        for i in listOfVariableToAdd:
            if verbose: print(('Elaborating variable: '+ i))
            auxDataFrame=pd.DataFrame()                
            auxDataFrame[i]=pd.Series(DATA[i][1].tolist(),pd.to_datetime(DATA[i][0],unit='s'))
            # important function to keep in mind
            myDataFrame=pd.merge(myDataFrame,auxDataFrame, how='outer',left_index=True,right_index=True)
        
    #Time-zone localization
    if len(myDataFrame):
        myDataFrame.index=myDataFrame.index.tz_localize('UTC')
    return myDataFrame
    
def cals2pd(listOfVariables, t1, t2, fundamental='', split=1, verbose=False): 
    '''
    cals2pd(listOfVariables, t1, t2, fundamental='', split=1, verbose=False)

    This is the most important function of the importData class.

    t1 and t2 are pandas datetime. We encourage to use "time zone", tz , aware expression (see example).
    Tz-naive expressions (without explicit time zone) will be consider UTC-localized.

    It returns a pandas dataframe of the listOfVariables within the interval [t1,t2].
    The index timestamps of the output dataframe are UTC-localized.

    It can be used to filter fundamentals (especially intended for the injectors).
    It can be used in the verbose mode if the corresponding flag is True.
    The data extraction can be done splitting it in several n intervals (split=n). 

    ===Example===     

    # you can use different timezone, in this example we use Central European Time (local time at CERN).
    t1 = pd.Timestamp('2017-10-01 17:30', tz='CET')
    t2 = pd.Timestamp('2017-10-01 17:31', tz='CET')
    raw_data = importData.cals2pd(['LHC.BCTDC.A6R4.B%:BEAM_INTENSITY','CPS.%:USER'],t1,t2)
    # By default the index timezone is UTC but, even if not encouraged, you can chance the index time zone.
    raw_data.index=raw_data.index.tz_convert('CET')
    '''
    if split<1: split=1

    if split==1: 
        myDF=_noSplitcals2pd(listOfVariables, t1, t2, fundamental, verbose)
    else:
        times= pd.to_datetime(np.linspace(t1.value, t2.value, split+1))
        myDF=pd.DataFrame()
        for i in range(len(times)-1):
            if verbose: print(('Time window: '+str(i+1))) 
            aux=_noSplitcals2pd(listOfVariables,times[i],times[i+1], fundamental=fundamental, verbose=verbose)
            myDF=pd.concat([myDF,aux], sort=True)
    return myDF.sort_index(axis=1)

def cycleStamp2pd(variablesList,cycleStampList,verbose=False):
    '''
    Return a pandas DataFrame with the specified variables and cyclestamps.
    This can be significantly slow since it accesses CALS for each cyclestamp.

    ===Example===     
    startTime=pd.Timestamp('2018-03-27 06:00')
    endTime=pd.Timestamp('2018-03-27 06:10')
    CPSDF=importData.cals2pd(['CPS.LSA:CYCLE'], startTime, endTime, fundamental='%LHC25%')
    # to get the correspind PSB of the 1st batch
    importData.cycleStamp2pd(['PSB.LSA:CYCLE'],CPSDF.index[1:]-pd.offsets.Milli(635))
    '''

    myDF=pd.DataFrame()
    for i in cycleStampList:
        if verbose:
            print(i)
        aux=cals2pd(variablesList,i,i)
        myDF=myDF.combine_first(aux)
    return myDF 

def _UTClocalizeMe(x):
    '''
    Return the tz-aware datetime. In case of error returns x.
    '''
    try:
        return x.tz_localize('UTC')
    except:
         return x # in case NaT or None

def LHCFillsByTime(t1,t2, verbose=False):
    '''
    Retrieve the LHC fills between t1 and t2.

    t1 and t2 are pandas datatime, therefore you can use tz-aware expression.
    Tz-naive expressions will be consider UTC-localized.

    The timestamps are time-zone-aware and are in 'UTC'.

    If, at the moment of the CALS extraction, the fill is not yet dumped,
    the endTime of the fill is assigned to NaT (Not a Time).

    ===Example===

    t1 = pd.Timestamp('2017-10-01')  # interpreted as tz='UTC'
    t2 = pd.Timestamp('2017-10-02', tz='CET')
    df=importData.LHCFillsByTime(t1,t2)

    # To tz-convert a specific column from 'UTC' (standard output) to 'CET'.
    # This practice is not encouraged since 'UTC' time is monotonic along the year
    # (for the moment the leap seconds were always positive).
    summary['startTime']=summary['startTime'].apply(lambda x: x.astimezone('CET'))
    '''

    if t1.tz==None: t1.tz_localize('UTC')
    else: t1=t1.astimezone('CET')

    if t2.tz==None: t2.tz_localize('UTC')
    else: t2=t2.astimezone('CET')

    DATA=cals.getLHCFillsByTime(t1,t2)

    fillNumberList, beamModesList = [], []
    startTimeList, endTimeList = [], []
    FN, ST, ET =[], [], [] #fillNumber, startTime, endTime

    for i in DATA:
        FN.append(i['fillNumber']); ST.append(i['startTime']); ET.append(i['endTime'])
        for j in i['beamModes']:
            fillNumberList.append(i['fillNumber']); beamModesList.append(j['mode'])
            startTimeList.append(j['startTime']); endTimeList.append(j['endTime'])

    auxDataFrame=pd.DataFrame()
    auxDataFrame['mode']=pd.Series(beamModesList, fillNumberList)
    auxDataFrame['startTime']=pd.Series(pd.to_datetime(startTimeList,unit='s'), fillNumberList)
    auxDataFrame['endTime']=pd.Series(pd.to_datetime(endTimeList,unit='s'), fillNumberList)
    auxDataFrame['duration']=auxDataFrame['endTime']-auxDataFrame['startTime']

    aux=pd.DataFrame()
    aux['startTime']=pd.Series(pd.to_datetime(ST,unit='s'), FN)
    aux['endTime']=pd.Series(pd.to_datetime(ET,unit='s'), FN)
    aux['duration']=aux['endTime']-aux['startTime']

 
    aux['startTime']=aux['startTime'].apply(_UTClocalizeMe)
    aux['endTime']=aux['endTime'].apply(_UTClocalizeMe)

    auxDataFrame['startTime']=auxDataFrame['startTime'].apply(_UTClocalizeMe)
    auxDataFrame['endTime']=auxDataFrame['endTime'].apply(_UTClocalizeMe)
    aux['mode']='FILL'
    fillsSummary=aux;
    fillsDetails=auxDataFrame;
    out=pd.DataFrame()
    if len(fillsSummary)>0:
        if (len(fillsSummary)==1) & (str(fillsSummary.iloc[0]['duration'])=='NaT'):
            # If there is only the online FILL (so not yet completed)
            # TODO: very cumbersome casting (first to string, then concatenation, then to timestamp)
            # I am no satisfied [GS]
            if verbose: print('Online FILL...')
            fillsSummary['endTime']='NaT'
            fillsSummary['duration']='NaT'
            fillsDetails['endTime']=fillsDetails['endTime'].astype(str)
            fillsDetails['duration']=fillsDetails['duration'].astype(str)
            out=pd.concat([fillsDetails,fillsSummary],sort=True)
            out=out.sort_values('startTime')[['mode','startTime','endTime','duration']]
            out['endTime']=out['endTime'].apply(pd.Timestamp)
            out['duration']=out['endTime']-out['startTime']
        else:
            out=pd.concat([fillsDetails,fillsSummary], sort=True)
            out=out.sort_values('startTime')[['mode','startTime','endTime','duration']]    
    
    return out

def LHCFillsByNumber(fillList, verbose=False):
    '''
    LHCFillsByNumber(fillList, verbose=False)

    The timestamps are time-zone-aware and by are in 'UTC'.

    ===Example===
    df=importData.LHCFillsByNumber([6400, 5900, 5901])
    '''
    fillsSummary, fillsDetails, aux=pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
    
    # we dilter with unique
    fillList=np.unique(fillList)

    # We iterate in the fills
    for i in fillList:

        if verbose: print(('Fill ' + str(i)))

        DATA=cals.getLHCFillData(np.int(i))

        fillNumberList=[]
        startTimeList=[]
        endTimeList=[]
        beamModesList=[]

        # For each fill we parse the DATA dictionary
        if DATA!=None:

            for j in DATA['beamModes']:
                beamModesList.append(j['mode'])
                fillNumberList.append(DATA['fillNumber'])
                startTimeList.append(j['startTime'])
                endTimeList.append(j['endTime'])

            auxDataFrame=pd.DataFrame()
            auxDataFrame['mode']=pd.Series(beamModesList, fillNumberList)
            auxDataFrame['startTime']=pd.Series(pd.to_datetime(startTimeList,unit='s'), fillNumberList)
            auxDataFrame['endTime']=pd.Series(pd.to_datetime(endTimeList,unit='s'), fillNumberList)
            auxDataFrame['duration']=auxDataFrame['endTime']-auxDataFrame['startTime']

            aux=pd.DataFrame()
            aux['startTime']=pd.Series(pd.to_datetime(DATA['startTime'],unit='s'), [DATA['fillNumber']])
            if DATA['endTime']==None:
                aux['endTime']=pd.Series(pd.to_datetime(endTimeList[-1],unit='s'), [DATA['fillNumber']])
            else:
                aux['endTime']=pd.Series(pd.to_datetime(DATA['endTime'],unit='s'), [DATA['fillNumber']])
            try: 
                aux['duration']=aux['endTime']-aux['startTime']
            except:
                aux['duration']=pd.to_datetime(endTimeList[-1],unit='s')
        else:
            aux, auxDataFrame=pd.DataFrame(),pd.DataFrame()

        # We concatenate the results
        fillsSummary=pd.concat([aux,fillsSummary], sort=True)
        fillsDetails=pd.concat([auxDataFrame,fillsDetails], sort=True)

    # The timestamps are localized and the dataframes are sorted
    if len(fillsSummary):
        fillsSummary['startTime']=fillsSummary['startTime'].apply(_UTClocalizeMe)
        fillsSummary['endTime']=fillsSummary['endTime'].apply(_UTClocalizeMe)
        fillsSummary=fillsSummary.sort_values(['startTime'])

        fillsDetails['startTime']=fillsDetails['startTime'].apply(_UTClocalizeMe)
        fillsDetails['endTime']=fillsDetails['endTime'].apply(_UTClocalizeMe)

        fillsDetails=fillsDetails.sort_values(['startTime'])

    fillsSummary['mode']='FILL'
    # Following two lines important for consecutive fills without modes (e.g., LHCFillsByNumber([6577,6578],verbose=True))
    aux=fillsSummary

    if len(fillsSummary)>0:
        aux=aux.sort_values('startTime')[['mode','startTime','endTime','duration']]    
        if (len(fillsSummary)==1) & (fillsSummary.iloc[0]['duration']==None):
            # If there is only the online FILL (so not yet completed)
            # TODO: very cumbersome casting (first to string, then concatenation, then to timestamp)
            # I am no satisfied [GS]
            if verbose: print('Online FILL...')
            fillsSummary['endTime']='NaT'
            fillsSummary['duration']='NaT'
            fillsDetails['endTime']=fillsDetails['endTime'].astype(str)
            fillsDetails['duration']=fillsDetails['duration'].astype(str)
            aux=pd.concat([fillsDetails,fillsSummary], sort=True)
            aux=aux.sort_values('startTime')[['mode','startTime','endTime','duration']]
            aux['endTime']=aux['endTime'].apply(pd.Timestamp)
            aux['duration']=aux['endTime']-aux['startTime']
        else:
            if len(fillsDetails)>0:
                aux=pd.concat([fillsDetails,fillsSummary], sort=True)
                aux=aux.sort_values('startTime')[['mode','startTime','endTime','duration']]    
    return aux


def massiFile2pd(myFileName, myUnzipPath='/tmp'):
    '''
    Transform a Massi file in form of pandas dataframe.

    ===Example===     
    ATLAS=importData.massiFile2pd('/eos/user/s/sterbini/MD_ANALYSIS/2017/LHC/MD2201/ATLAS_6195.tgz')

    Massi files can be found at /afs/cern.ch/user/l/lpc/w0/
    Documentation about the Massi file format can be found at https://lpc.web.cern.ch/MassiFileDefinition_v2.htm
    '''
    import tarfile
    import os
    import glob

    tar = tarfile.open(myFileName, "r:gz")
    tar.extractall(path=myUnzipPath)
    filename,extension=os.path.splitext(myFileName)
    fillNumber=tar.getnames()[0]
    pdList=[]
    myFiles=glob.glob(os.path.join(myUnzipPath,fillNumber)+'/*')
    for i in myFiles:
        filename,extension=os.path.splitext(i)
        aux=filename.split('_')
        if len(aux)==4:
            MassiFileType=aux[1]
            bunch=int(aux[2])/10
            if MassiFileType=='lumi':
                experiment=aux[3]
                myDF=pd.read_csv(i,sep=' ', header=0,names=['UNIX time UTC',
                                                              'Stable Beam Flag',
                                                              'Luminosity [Hz/ub]',
                                                              'P2P luminosity error [Hz/ub]',
                                                              'Specific luminosity [Hz/ub]',
                                                              'P2P specific luminosity [Hz/ub]'])
                myDF['Bunch']=int(bunch)
                myDF['FILL']=int(fillNumber)
                myDF['Experiment']=experiment
                myDF['Timestamp']=myDF['UNIX time UTC'].apply(lambda x: pd.Timestamp(x,unit='s').tz_localize('UTC'))
                pdList.append(myDF)
            else:
                print('Only lumi file implemented.')
        os.remove(i)
    massiFile=pd.concat(pdList, sort=True)
    massiFile=massiFile.set_index('Timestamp')
    del massiFile.index.name
    os.rmdir(os.path.join(myUnzipPath,fillNumber))
    return massiFile[['FILL','Stable Beam Flag','Experiment','Bunch','Luminosity [Hz/ub]','P2P luminosity error [Hz/ub]',
              'Specific luminosity [Hz/ub]','P2P specific luminosity [Hz/ub]']]

def calsCSV2pd(myFile):
    '''
    Convert cals CVS file in a pd DataFrame.

    The files are of the type in /eos/project/l/lhc-lumimod/
    UTC time is always assumed.
    '''
    # I read the full file once to have the line numbers when a new variable starts, its name and its type
    startLinesList = []
    variableNameList = []
    variableTypeList=[]
    with open(myFile, 'r') as file:
        lines=file.readlines()
        i=0
        for i in range(len(lines)):
            if lines[i][0:8]=='VARIABLE':
                variableName=lines[i].split(': ')[1][0:-1]
                startLinesList.append(i)
                variableNameList.append(variableName)            

            if lines[i][0:9]=='Timestamp':
                variableName=lines[i].split(',')[1][0:-1]
                variableTypeList.append(variableName)

        startLinesList.append(i+1)

    # in the second part I fill for each variable a pd DataFrame and I merge the dataframes.
    # for the moment I assume that only two variable type are used ('Value' and 'Array Values')
    # TODO: relax the assumptions above.
    aux=pd.DataFrame()
    for i in range(len(startLinesList)-1):
        if variableTypeList[i]=='Value':
            # in this case I use the pd.read_csv
            df=pd.read_csv(myFile,skiprows=startLinesList[i]+1, nrows=startLinesList[i+1]-3-startLinesList[i],)
            df=df.set_index('Timestamp (UTC_TIME)')
            df=df.rename(index=str, columns={'Value': variableNameList[i] })
            df.index=pd.DatetimeIndex(df.index)
        if variableTypeList[i]=='Array Values':
            # in this case I use a custom solution
            j=startLinesList[i]+3
            myTime=[]
            myArray=[]
            while j<(startLinesList[i+1]):    
                myReading=lines[j].split(',')
                myTime.append(myReading[0])
                myArray.append(np.double(myReading[1:]))
                j=j+1
            df=pd.DataFrame({'Array Values':myArray,'Timestamp (UTC_TIME)':myTime})
            df=df.set_index('Timestamp (UTC_TIME)')
            df=df.rename(index=str, columns={'Array Values': variableNameList[i] })     
            df.index=pd.DatetimeIndex(df.index)
        # I merge to maintain the index unique
        aux=pd.merge(aux,df, left_index=True, 
                         right_index=True, 
                         how='outer')
    aux.index=aux.index.tz_localize('UTC')
    aux=aux.sort_index()
    del aux.index.name
    return aux 

def mat2dict(myfile):
    '''
    Import a matlab file in a python structure 

    ===Example===     
    aux=importData.mat2dict('/eos/user/s/sterbini/MD_ANALYSIS/2016/MD1780_80b/2016.10.26.22.23.42.135.mat')
    '''
    import scipy.io
    myDataStruct = scipy.io.loadmat(myfile,squeeze_me=True, struct_as_record=False)
    return myDataStruct['myDataStruct']

def mat2pd(variablesList,filesList, verbose=False, matlabFullInfo=False):
    '''
    Return a pandas DataFrame given a variable list and a file list.

    ===Example=== 
    importData.mat2pd(['CPS_BLM.Acquisition.value.lastLosses'],\
    ['/eos/user/s/sterbini/MD_ANALYSIS/2016/MD1780_80b/2016.10.26.22.23.42.135.mat',\
    '/eos/user/s/sterbini/MD_ANALYSIS/2016/MD1780_80b/2016.10.26.22.23.06.147.mat'])
    '''
    import os
    myDataFrame=pd.DataFrame()
    cycleStampList=[]
    matlabObject=[]
    matlabFilePath=[]
    for j in variablesList:
        exec(j.replace('.','_')+'=[]')
    for i in filesList:
        if verbose:
            print(i)
        data=mat2dict(i);
        if matlabFullInfo:
            matlabObject.append(data)
        localCycleStamp=np.max(data.headerCycleStamps);
        cycleStamp=pd.Timestamp(localCycleStamp,unit='ns')
        cycleStampList.append(cycleStamp.tz_localize('UTC'))
        matlabFilePath.append(os.path.abspath(i))
        for j in variablesList:
            if hasattr(data,j.split('.')[0]):
                exec(j.replace('.','_') + '.append(data.' + j + ')')
            else:
                exec(j.replace('.','_') + '.append(np.nan)')
    myDataFrame['matlabFilePath']=pd.Series(matlabFilePath,cycleStampList)
    if matlabFullInfo:
        myDataFrame['matlabFullInfo']=pd.Series(matlabObject,cycleStampList)
    for j in variablesList:
        exec('myDataFrame[\'' + j + '\']=pd.Series(' +j.replace('.','_')+ ',cycleStampList)')   
    return myDataFrame.sort_index(axis=1).sort_index(axis=0)

class _TFS:
    '''
       TFS parameters from MADX TFS output.
       The approach used is mainly inherithed from the class TWISS suggested by H. Bartosik et al.
    '''
           
    def __init__(self, filename): 
        self.indx={}
        self.keys=[]
        alllabels=[]
        #if '.gz' in filename:
        #    f=gzip.open(filename, 'rb')
        #else:
        f=open(filename, 'r')
            
        for line in f:
            if ("@ " not in line and "@" in line): 
                line = replace(line, "@" , "@ ")
            if ("@ " in line and "%" in line and "s" not in line.split()[2]) :
                label=line.split()[1]
                try:
                    exec("self."+label+"= "+str(float((line.replace( '"', '')).split()[3])))
                except:
                    print(("Problem parsing: "+ line))
                    print("Going to be parsed as string")
                    try:
                        exec("self."+label+"= \""+(line.split()[3]).replace( '"', '')+"\"")
                    except:
                        print("Problem persits, let's ignore it!")
            elif ("@ " in line and "s"  in line.split()[2]):
                label=(line.split()[1]).replace(":","")
                exec("self."+label+"= \""+(line.replace('"', '')).split()[3]+"\"")

            if ("* " in line or "*\t" in line) :
                    alllabels=line.split()
                    for j in range(1,len(alllabels)):
                        exec("self."+alllabels[j]+"= []")
                        self.keys.append(alllabels[j])
                            
            if ("$ " in line or "$\t" in line) :
                alltypes=line.split()                

            if ("@" not in line and "*" not in line and "$" not in line) :
                values=line.split()   
                for j in range(0,len(values)):
                    if ("%hd" in alltypes[j+1]):                      
                        exec("self."+alllabels[j+1]+".append("+str(int(values[j]))+")")                 
                    if ("%le" in alltypes[j+1]):                      
                        exec("self."+alllabels[j+1]+".append("+str(float(values[j]))+")")
                    if ("s" in alltypes[j+1]):
                        try:
                            exec("self."+alllabels[j+1]+".append("+values[j]+")")
                        except:
                            exec("self."+alllabels[j+1]+".append(\""+values[j]+"\")") #To allow with or without ""
                        if "NAME"==alllabels[j+1]:
                            self.indx[values[j].replace('"', '')]=len(self.NAME)-1
                            self.indx[values[j].replace('"', '').upper()]=len(self.NAME)-1
                            self.indx[values[j].replace('"', '').lower()]=len(self.NAME)-1
        f.close()
        
        for j in range(1,len(alllabels)):
            if (("%le" in alltypes[j]) | ("%hd" in alltypes[j])  ):  
                exec("self."+alllabels[j]+"= np.array(self."+alllabels[j]+")") 


def _tfs2pd(myFile):
        '''
        Import a MADX TFS file in a pandas dataframe.
        
        ===Example=== 
        aux=importData.TFS2pd('/eos/user/s/sterbini/MD_ANALYSIS/2018/LHC MD Optics/collisionAt25cm_180urad/lhcb1_thick.survey')
        '''
        a=_TFS(myFile);
        aux=[]
        aux1=[]

        for i in dir(a):
            if not i[0]=='_':
                if type(getattr(a,i)) is float:
                    #print(i + ":"+ str(type(getattr(a,i))))
                    aux.append(i)
                    aux1.append(getattr(a,i))
                if type(getattr(a,i)) is str:
                    #print(i + ":"+ str(type(getattr(a,i))))
                    aux.append(i)
                    aux1.append(getattr(a,i))

        myList=[]
        myColumns=[]
        for i in a.keys:
            myContainer=getattr(a, i)
            if len(myContainer)==0:
                print(("The column "+ i + ' is empty.'))
            else:
                myColumns.append(i)
                myList.append(myContainer)
                
        if 'S' in a.keys:
            optics=pd.DataFrame(np.transpose(myList), index=a.S, columns=myColumns)
        else:
            optics=pd.DataFrame(np.transpose(myList), columns=myColumns)
        #optics=pd.DataFrame(np.transpose(myList), index=a.S,columns=myColumns)

        for i in optics.columns:
            aux3= optics.iloc[0][i]
            if type(aux3) is str:
                aux3=str.replace(aux3, '+', '')
                aux3=str.replace(aux3, '-', '')
                aux3=str.replace(aux3, '.', '')
                aux3=str.replace(aux3, 'e', '')
                aux3=str.replace(aux3, 'E', '')


                if aux3.isdigit():
                    optics[i]=optics[i].apply(np.double)

        aux.append('FILE_NAME')
        aux1.append(os.path.abspath(myFile))

        aux.append('TABLE')
        aux1.append(optics)

        globalDF=pd.DataFrame([aux1], columns=aux)
        globalDF=globalDF.set_index('FILE_NAME')
        globalDF.index.name=''
        return globalDF 
    
def tfs2pd(myList):
    '''
        Import a MADX TFS file in a pandas dataframe.
        
        ===Example=== 
        aux=importData.tfs2pd(['/eos/user/s/sterbini/MD_ANALYSIS/2018/LHC MD Optics/collisionAt25cm_180urad/lhcb1_thick.survey',
        '/eos/user/s/sterbini/MD_ANALYSIS/2018/LHC MD Optics/collisionAt25cm_180urad/lhcb1_thick.twiss'])
    '''
    if isinstance(myList, list):
        aux=[]
        for i in np.unique(myList):
            aux.append(_tfs2pd(i))
        return pd.concat(aux, sort=True)
    else:
        return _tfs2pd(myList)
    
def _LHCCals2pd(listOfVariables, fillList ,beamModeList='FILL', split=1, verbose=False):
    '''
    LHCCals2pd(listOfVariables, fillList, beamModeList='FILL', split=1, verbose=False)

    Return the listOfVariables in the fill of the fillList for a given list of beamModeList. 
    
    It can be used in the verbose mode if the corresponding flag is True.
    The data extraction can be done splitting it in several n intervals (split=n). 

    ===Example===     
    importData.LHCCals2pd(['RPHFC.UL14.RQX.L1:I_MEAS'],[6278, 6666],['RAMP','FLATTOP'])
    '''
    if len(listOfVariables)==0:
        return pd.DataFrame()
    
    fillList=np.unique(fillList)
    beamModeList=np.unique(beamModeList)
        
    listDF=[]

    for fill in fillList: 
        if verbose: print(('Fill: '+str(fill)))
        fillDF=LHCFillsByNumber(fill)
        for BM in beamModeList:
            aux=fillDF[fillDF['mode']==BM]
            if verbose: print(('Beam mode: '+BM))

            for index,row in aux.iterrows():
                t1=row.startTime
                t2=row.endTime
                if verbose: print(('Start time: '+str(t1)))
                if verbose: print(('End time: '+str(t2)))
                listDF.append(cals2pd(listOfVariables,t1,t2, split=split, verbose=verbose))
    if listDF==[]:
        return pd.DataFrame()
    else:
        return pd.concat(listDF, sort=True).sort_index()

def LHCInstant(t1,timeSpan_days=1):
    '''
    LHCInstant(t1,timeSpan_days=1)
    
    Return the fill information at the instant t1.
    timeSpan_days is the argument needed to start the search in the period [t1-timeSpan_days,t1].
    If the fill active in t1 has to start in the interval [t1-timeSpan_days,t1]. In most of the cases timeSpan_days=1
    is enough.
    
    ===Example===   
    t1 = pd.Timestamp('2018-05-22 02:10:15', tz='CET')
    importData.LHCInstant(t1)
    # Retrive some of the last fill
    importData.LHCInstant(pd.Timestamp.now('CET')-pd.Timedelta('1d') )
    '''
    if t1.tz==None: t1.tz_localize('UTC')
    else: t1=t1.astimezone('UTC')
    aux=LHCFillsByTime(t1-pd.DateOffset(timeSpan_days) ,t1)
    aux=aux[aux['mode']!='FILL']
    aux['test']=aux.apply(lambda x: x['startTime']<=t1<=x['endTime'] , axis=1)
    aux= aux[aux['test']]
    del aux['test']
    return aux
    '''
    #proposition
    def LHCInstant(t1):
        if t1.tz==None: t1=t1.tz_localize('UTC')
        else: t1=t1.astimezone('UTC')

        aux=cals2pd(['HX:FILLN'],t1,'last')['HX:FILLN'].values
        if len(aux)>0:
            aux=LHCFillsByNumber(np.int(aux[0]))
            aux=aux[aux['mode']!='FILL']
            aux['test']=aux.apply(lambda x: x['startTime']<=t1<=x['endTime'] , axis=1)
            if len(aux)==0:
                return pd.DataFrame();
            aux= aux[aux['test']]
            del aux['test']
            return aux
        else:
            return pd.DataFrame()
    '''


# TEST FUNCTIONS

def _LHCCals2pd_ver1(listOfVariables, fillList ,beamModeList='FILL', split=1, verbose=False,
                     fill_column=False, beamMode_column=False):
    '''
    _LHCCals2pd_ver1(listOfVariables, fillList ,beamModeList='FILL', split=1, verbose=False,
                     fill_column=False, beamMode_column=False)
                     
    Return the listOfVariables in the fill of the fillList for a given list of beamModeList. 

    It can be used in the verbose mode if the corresponding flag is True.
    The data extraction can be done splitting it in several n intervals (split=n).
    If fill_column and beamMode_column are True then also the fill and the mode is included 
    in the df.

    ===Example===     
    importData._LHCCals2pd_ver1(['RPHFC.UL14.RQX.L1:I_MEAS'],[6278, 6666],['RAMP','FLATTOP'])
    '''
    if len(listOfVariables)==0:
        return pd.DataFrame()

    fillList=np.unique(fillList)
    beamModeList=np.unique(beamModeList)

    listDF=[]

    for fill in fillList: 
        if verbose: print(('Fill: '+str(fill)))
        fillDF=LHCFillsByNumber(fill)
        for BM in beamModeList:
            aux=fillDF[fillDF['mode']==BM]
            if verbose: print(('Beam mode: '+BM))

            for index,row in aux.iterrows():
                t1=row.startTime
                t2=row.endTime
                if verbose: print(('Start time: '+str(t1)))
                if verbose: print(('End time: '+str(t2)))
                out=cals2pd(listOfVariables,t1,t2, split=split, verbose=verbose)
                if fill_column:
                    out['fill']=fill
                if beamMode_column:
                    out['mode']=BM
                listDF.append(out)
    if listDF==[]:
        return pd.DataFrame()
    else:
        return pd.concat(listDF, sort=True).sort_index()
    
def LHCCals2pd(listOfVariables, fillList ,beamModeList='FILL', split=1, verbose=False,
                     fill_column=False, beamMode_column=False, flag='', offset=pd.Timedelta(0), duration=pd.Timedelta('5s')):
    '''
    LHCCals2pd(listOfVariables, fillList ,beamModeList='FILL', split=1, verbose=False,
                     fill_column=False, beamMode_column=False, flag='', offset=pd.Timedelta(0), duration=pd.Timedelta('5s')
    Return the listOfVariables in the fill of the fillList for a given list of beamModeList. 
    It can be used in the verbose mode if the corresponding flag is True.
    The data extraction can be done splitting it in several n intervals (split=n).
    If fill_column and beamMode_column are True then also the fill and the mode is included 
    in the df.
    It is possible to add an offset (default is offset=pd.Timedelta(0)): this will offset the the startTime and endTime.
    If flag is 'next' or 'last', the next or last  measurement after or before the startTime (+offset) will be returned.
    if flag is 'duration' the extraction will be between [t1,t2], with t1=(startTime+offset) and t2=(startTime+offset+duration).
    The default value of duration is pd.Timedelta('5s')
    
    ===Example===     
    importData.LHCCals2pd(['RPHFC.UL14.RQX.L1:I_MEAS'],[6278, 6666],['RAMP','FLATTOP'])
    
    importData.LHCCals2pd(['RPHFC.UL14.RQX.L1:I_MEAS'],[6278, 6666,6690],['RAMP','FLATTOP'],flag='duration',fill_column=True, beamMode_column=True, offset=pd.Timedelta('5s'),duration=pd.Timedelta('60s'))
    
    importData.LHCCals2pd(['RPHFC.UL14.RQX.L1:I_MEAS'],[6278, 6666,6690],['RAMP','FLATTOP'],flag='next',fill_column=True, beamMode_column=True,fill_column=True, beamMode_column=True,)
    '''
    if len(listOfVariables)==0:
        return pd.DataFrame()

    fillList=np.unique(fillList)
    beamModeList=np.unique(beamModeList)

    listDF=[]
    
    if flag=='':
        for fill in fillList: 
            if verbose: print(('Fill: '+str(fill)))
            fillDF=LHCFillsByNumber(fill)
            for BM in beamModeList:
                aux=fillDF[fillDF['mode']==BM]
                if verbose: print(('Beam mode: '+BM))

                for index,row in aux.iterrows():
                    t1=row.startTime+offset
                    t2=row.endTime+offset
                    if verbose: print(('Start time: '+str(t1)))
                    if verbose: print(('End time: '+str(t2)))
                    out=cals2pd(listOfVariables,t1,t2, split=split, verbose=verbose)
                    if fill_column:
                        out['fill']=fill
                    if beamMode_column:
                        out['mode']=BM
                    listDF.append(out)
        if listDF==[]:
            return pd.DataFrame()
        else:
            return pd.concat(listDF, sort=True).sort_index()
        
    if (flag=='last') or (flag=='next'):
        for fill in fillList: 
            if verbose: print(('Fill: '+str(fill)))
            fillDF=LHCFillsByNumber(fill)
            for BM in beamModeList:
                aux=fillDF[fillDF['mode']==BM]
                if verbose: print(('Beam mode: '+BM))

                for index,row in aux.iterrows():
                    t1=row.startTime+offset
                    t2=flag
                    if verbose: print(('Start time: '+str(t1)))
                    if verbose: print(('End time: '+str(t2)))
                    out=cals2pd(listOfVariables,t1,t2, split=split, verbose=verbose)
                    if fill_column:
                        out['fill']=fill
                    if beamMode_column:
                        out['mode']=BM
                    listDF.append(out)
        if listDF==[]:
            return pd.DataFrame()
        else:
            return pd.concat(listDF, sort=True).sort_index()
        
    if (flag=='duration'):
        for fill in fillList: 
            if verbose: print(('Fill: '+str(fill)))
            fillDF=LHCFillsByNumber(fill)
            for BM in beamModeList:
                aux=fillDF[fillDF['mode']==BM]
                if verbose: print(('Beam mode: '+BM))

                for index,row in aux.iterrows():
                    t1=row.startTime+offset
                    t2=t1+duration
                    if verbose: print(('Start time: '+str(t1)))
                    if verbose: print(('End time: '+str(t2)))
                    out=cals2pd(listOfVariables,t1,t2, split=split, verbose=verbose)
                    if fill_column:
                        out['fill']=fill
                    if beamMode_column:
                        out['mode']=BM
                    listDF.append(out)
        if listDF==[]:
            return pd.DataFrame()
        else:
            return pd.concat(listDF, sort=True).sort_index()

def LHCFillsAggregation (listOfVariables, fillNos, beamModeList = None, functionList = None, mapInsteadAgg = False, flag = None, offset = None, duration = None):
    '''
    
    For the selected fill numbers, beam modes and list of variables, this function creates 
    a list for each variable on which it applies the coresponding function. The result is 
    returned as output. If function is set to None, than no processing of the data is done.
    If one function is set as input, that one function is applied to all of the variables. 
    If number of functions must is the same as the number of variables, each variable is 
    processed by the coresponding function.
    
    It is possible to add an offset. This will offset the the startTime and endTime.
    If flag is 'next' or 'last', the next or last  measurement after or before the startTime (+offset) will be returned.
    if flag is 'duration' the extraction will be between [t1,t2], with t1=(startTime+offset) and t2=(startTime+offset+duration).
    If some of these parameters are not set, the default ones from the function _LHCCals2pd_ver2 are used.
    
    ===EXAMPLE===
    LHCFillsAggregation(['LHC.BQM.B2:NO_BUNCHES', 'LHC.BQM.B1:NO_BUNCHES'], range(6500, 6800))
    LHCFillsAggregation(['LHC.BQM.B2:NO_BUNCHES', 'LHC.BQM.B1:NO_BUNCHES'], range(6500, 6800), ['INJPHYS','INJPROT'])
    LHCFillsAggregation(['LHC.BQM.B2:NO_BUNCHES', 'LHC.BQM.B1:NO_BUNCHES'], range(6500, 6800), ['INJPHYS','INJPROT'], [pd.Series.mean, pd.Series.max], 'last')
    LHCFillsAggregation(['LHC.BQM.B2:NO_BUNCHES', 'LHC.BQM.B1:NO_BUNCHES'], range(6500, 6800), 'PRERAMP', pd.Series.max, 'last')
    LHCFillsAggregation(['LHC.BCTFR.A6R4.B%:BUNCH_INTENSITY'],6666, ['FLATTOP'],flag='duration',duration=pd.Timedelta('1m'), functionList = np.mean, mapInsteadAgg = True)
    
    '''
    # FOR DEBUGGING 
    # import pdb
    # pdb.set_trace()
    
    # Fetching the default values from the _LHCCals2pd_ver2 function.
    # Doing it like this so in case the default values change, you don't have to modify the function
    # Current look of default values
    # [('beamModeList', 'FILL'),
    # ('split', 1),
    # ('verbose', False),
    # ('fill_column', False),
    # ('beamMode_column', False),
    # ('flag', ''),
    # ('offset', Timedelta('0 days 00:00:00')),
    # ('duration', Timedelta('0 days 00:00:05'))]
    
    a = inspect.getargspec(LHCCals2pd)
    defaultValues = list(zip(a.args[-len(a.defaults):],a.defaults))
    
    defaultBeamModeList = defaultValues[0][1]
    defaultFlag = defaultValues[5][1]
    defaultOffset = defaultValues[6][1]
    defaultDuration = defaultValues[7][1]
    
    ## PROCESSING OF THE INPUT VARIABLES
    
    #listOfVariables
    if isinstance(listOfVariables, str):
        listOfVariables = [listOfVariables]
    
    #fillNos
    if isinstance(fillNos, int):
        fillNos = [fillNos]
        # This is done so that the for loop can work properly
        
    #beamModeList
    if beamModeList == None:
        beamModeList = defaultBeamModeList        
                
    #functionList
    if callable(functionList):
        functionList = [functionList]
        
    #flag
    if flag == None:
        flag = defaultFlag
    
    #offset
    if offset == None:
        offset = defaultOffset
    
    #duration
    if duration == None:
        duration = defaultDuration
                  
    NoOfFills = len(fillNos)
    NoOfModes = len(beamModeList)
    
    resultDF = pd.DataFrame()
    data = LHCCals2pd(listOfVariables, fillNos, beamModeList, fill_column=True, beamMode_column=True, flag = flag, offset = offset, duration = duration)
    
    # In case of regex variables, number of variables have to be counted this way 
    listOfVariables = data.columns.drop('fill').drop('mode')
    NoOfVar = len(listOfVariables)
    
    # Special interactions with the function list
    if functionList == None:
        # No need to do anything to the data expect multindex it so the output is always multi-indexed
        resultDF = data.set_index(['fill', 'mode'])
    
    else:
        NoOfFunctions = len(functionList)
        # This flag is set to 1 if we have a list of functions, it is reset to 0 if it only has one function
        functionFlag = 1
        if NoOfFunctions == 1:
            functionFlag = 0
        elif NoOfFunctions != NoOfVar:
            raise AttributeError("Number of functions not the same size as number of variables.")
            
        if mapInsteadAgg:
            # Apply function on each field
            resultDF = data.set_index(['fill', 'mode'])
            for i in range(0, NoOfVar):
                resultDF[listOfVariables[i]] = resultDF[listOfVariables[i]].map(functionList[i * functionFlag])

        else:    
            grupedData = data.groupby(['fill', 'mode'])
            for i in range(0, NoOfVar):
                resultDF[listOfVariables[i]] = grupedData[listOfVariables[i]].agg(functionList[i * functionFlag])
        
    #Fetching of the time data
    timeData = LHCFillsByNumber(fillNos)
    timeData['fill'] = timeData.index
    timeData = timeData.set_index(['fill', 'mode'])            

    return resultDF.join(timeData)

def LHCFillsMappingAggregation (listOfVariables, fillNos, beamModeList = None, mapFunctionList = [], aggFunctionList = [], flag = None, offset = None, duration = None):
    '''
    
    For the selected fill numbers, beam modes and list of variables, this function creates 
    a list for each variable on which it applies the coresponding function. The result is 
    returned as output. If function is set to None, than no processing of the data is done.
    If one function is set as input, that one function is applied to all of the variables. 
    If number of functions must is the same as the number of variables, each variable is 
    processed by the coresponding function.
    
    It is possible to add an offset. This will offset the the startTime and endTime.
    If flag is 'next' or 'last', the next or last  measurement after or before the startTime (+offset) will be returned.
    if flag is 'duration' the extraction will be between [t1,t2], with t1=(startTime+offset) and t2=(startTime+offset+duration).
    If some of these parameters are not set, the default ones from the function _LHCCals2pd_ver2 are used.
    
    ===EXAMPLE===
    importData.LHCFillsMappingAggregation(['LHC.BCTFR.A6R4.B%:BUNCH_INTENSITY'],6666, ['FLATTOP'],flag='duration',duration=pd.Timedelta('1m'), aggFunctionList = np.mean, mapFunctionList = np.mean)
    importData.LHCFillsMappingAggregation(['LHC.BCTFR.A6R4.B%:BUNCH_INTENSITY'],6666, ['FLATTOP'], aggFunctionList = np.mean, mapFunctionList = np.mean)
    importData.LHCFillsMappingAggregation(['LHC.BCTFR.A6R4.B%:BUNCH_FILL_PATTERN'],6666, ['FLATTOP'], mapFunctionList = np.mean)
    
    '''
    # FOR DEBUGGING 
    # import pdb
    # pdb.set_trace()
    
    # Fetching the default values from the _LHCCals2pd_ver2 function.
    # Doing it like this so in case the default values change, you don't have to modify the function
    # Current look of default values
    # [('beamModeList', 'FILL'),
    # ('split', 1),
    # ('verbose', False),
    # ('fill_column', False),
    # ('beamMode_column', False),
    # ('flag', ''),
    # ('offset', Timedelta('0 days 00:00:00')),
    # ('duration', Timedelta('0 days 00:00:05'))]
    
    a = inspect.getargspec(LHCCals2pd)
    defaultValues = list(zip(a.args[-len(a.defaults):],a.defaults))
    
    defaultBeamModeList = defaultValues[0][1]
    defaultFlag = defaultValues[5][1]
    defaultOffset = defaultValues[6][1]
    defaultDuration = defaultValues[7][1]
    
    ## PROCESSING OF THE INPUT VARIABLES
    
    #listOfVariables
    if isinstance(listOfVariables, str):
        listOfVariables = [listOfVariables]
    
    #fillNos
    if isinstance(fillNos, int):
        fillNos = [fillNos]
        # This is done so that the for loop can work properly
        
    #beamModeList
    if beamModeList == None:
        beamModeList = defaultBeamModeList        
                
    #aggFunctionList
    if callable(aggFunctionList):
        aggFunctionList = [aggFunctionList]
        
    #mapFunctionList
    if callable(mapFunctionList):
        mapFunctionList = [mapFunctionList]
        
    #flag
    if flag == None:
        flag = defaultFlag
    
    #offset
    if offset == None:
        offset = defaultOffset
    
    #duration
    if duration == None:
        duration = defaultDuration
                  
    NoOfFills = len(fillNos)
    NoOfModes = len(beamModeList)
    
    resultDF = pd.DataFrame()
    data = LHCCals2pd(listOfVariables, fillNos, beamModeList, fill_column=True, beamMode_column=True, flag = flag, offset = offset, duration = duration)
    
    # In case of regex variables, number of variables have to be counted this way 
    listOfVariables = data.columns.drop('fill').drop('mode')
    NoOfVar = len(listOfVariables)    
    
    NoOfAggFunctions = len(aggFunctionList)
    NoOfMapFunctions = len(mapFunctionList)
    # This flag is set to 1 if we have a list of functions, it is reset to 0 if it only has one function
    aggFunctionFlag = 1
    mapFunctionFlag = 1

    # Number of functions must be the same as number of variables
    if NoOfAggFunctions == 1 or NoOfAggFunctions == 0:
        aggFunctionFlag = 0
    elif NoOfAggFunctions != NoOfVar:
        raise AttributeError("Number of aggregate functions not the same size as number of variables or equal to 1.")

    if NoOfMapFunctions == 1 or NoOfMapFunctions == 0:
        mapFunctionFlag = 0
    elif NoOfMapFunctions != NoOfVar:
        raise AttributeError("Number of maping functions not the same size as number of variables or equal to 1.")

    resultDF = data.set_index(['fill', 'mode'])

    if NoOfMapFunctions != 0:
        # Apply function on each field            
        for i in range(0, NoOfVar):
            resultDF[listOfVariables[i]] = resultDF[listOfVariables[i]].map(mapFunctionList[i * mapFunctionFlag])

    if NoOfAggFunctions != 0:
        temp_resultDF = pd.DataFrame()
        grupedData = resultDF.groupby(['fill', 'mode'])
        for i in range(0, NoOfVar):
            temp_resultDF[listOfVariables[i]] = grupedData[listOfVariables[i]].agg(aggFunctionList[i * aggFunctionFlag])
        resultDF = temp_resultDF

        
    #Fetching of the time data
    timeData = LHCFillsByNumber(fillNos)
    timeData['fill'] = timeData.index
    timeData = timeData.set_index(['fill', 'mode'])            

    return resultDF.join(timeData)

def LHCFillsMappingAggregation_v2 (listOfVariables, fillNos, beamModeList = None, mapFunctionList = [], aggFunctionList = [], flag = None, offset = None, duration = None):
    '''
    
    For the selected fill numbers, beam modes and list of variables, this function creates 
    a list for each variable on which it applies the coresponding function. The result is 
    returned as output. If function is set to None, than no processing of the data is done.
    If one function is set as input, that one function is applied to all of the variables. 
    If number of functions must is the same as the number of variables, each variable is 
    processed by the coresponding function.
    
    It is possible to add an offset. This will offset the the startTime and endTime.
    If flag is 'next' or 'last', the next or last  measurement after or before the startTime (+offset) will be returned.
    if flag is 'duration' the extraction will be between [t1,t2], with t1=(startTime+offset) and t2=(startTime+offset+duration).
    If some of these parameters are not set, the default ones from the function _LHCCals2pd_ver2 are used.
    
    ===EXAMPLE===
    importData.LHCFillsMappingAggregation(['LHC.BCTFR.A6R4.B%:BUNCH_INTENSITY'],6666, ['FLATTOP'],flag='duration',duration=pd.Timedelta('1m'), aggFunctionList = np.mean, mapFunctionList = np.mean)
    importData.LHCFillsMappingAggregation(['LHC.BCTFR.A6R4.B%:BUNCH_INTENSITY'],6666, ['FLATTOP'], aggFunctionList = np.mean, mapFunctionList = np.mean)
    importData.LHCFillsMappingAggregation(['LHC.BCTFR.A6R4.B%:BUNCH_FILL_PATTERN'],6666, ['FLATTOP'], mapFunctionList = np.mean)
    
    '''
    # FOR DEBUGGING 
    # import pdb
    # pdb.set_trace()
    
    # Fetching the default values from the _LHCCals2pd_ver2 function.
    # Doing it like this so in case the default values change, you don't have to modify the function
    # Current look of default values
    # [('beamModeList', 'FILL'),
    # ('split', 1),
    # ('verbose', False),
    # ('fill_column', False),
    # ('beamMode_column', False),
    # ('flag', ''),
    # ('offset', Timedelta('0 days 00:00:00')),
    # ('duration', Timedelta('0 days 00:00:05'))]
    
    a = inspect.getargspec(LHCCals2pd)
    defaultValues = list(zip(a.args[-len(a.defaults):],a.defaults))
    
    defaultBeamModeList = defaultValues[0][1]
    defaultFlag = defaultValues[5][1]
    defaultOffset = defaultValues[6][1]
    defaultDuration = defaultValues[7][1]
    
    ## PROCESSING OF THE INPUT VARIABLES
    
    #listOfVariables
    if isinstance(listOfVariables, str):
        listOfVariables = [listOfVariables]
    
    #fillNos
    if isinstance(fillNos, int):
        fillNos = [fillNos]
        # This is done so that the for loop can work properly
        
    #beamModeList
    if beamModeList == None:
        beamModeList = defaultBeamModeList        
                
    #aggFunctionList
    if callable(aggFunctionList):
        aggFunctionList = [aggFunctionList]
        
    #mapFunctionList
    if callable(mapFunctionList):
        mapFunctionList = [mapFunctionList]
        
    #flag
    if flag == None:
        flag = defaultFlag
    
    #offset
    if offset == None:
        offset = defaultOffset
    
    #duration
    if duration == None:
        duration = defaultDuration
                  
    NoOfFills = len(fillNos)
    NoOfModes = len(beamModeList)
    
    resultDF = pd.DataFrame()
    data = LHCCals2pd(listOfVariables, fillNos, beamModeList, fill_column=True, beamMode_column=True, flag = flag, offset = offset, duration = duration)
    
    # In case of regex variables, number of variables have to be counted this way 
    listOfVariables = data.columns.drop('fill').drop('mode')
    NoOfVar = len(listOfVariables)    
    
    NoOfAggFunctions = len(aggFunctionList)
    NoOfMapFunctions = len(mapFunctionList)
    # This flag is set to 1 if we have a list of functions, it is reset to 0 if it only has one function
    aggFunctionFlag = 1
    mapFunctionFlag = 1

    # Number of functions must be the same as number of variables
    if NoOfAggFunctions == 1 or NoOfAggFunctions == 0:
        aggFunctionFlag = 0
    elif NoOfAggFunctions != NoOfVar:
        raise AttributeError("Number of aggregate functions not the same size as number of variables or equal to 1.")

    if NoOfMapFunctions == 1 or NoOfMapFunctions == 0:
        mapFunctionFlag = 0
    elif NoOfMapFunctions != NoOfVar:
        raise AttributeError("Number of maping functions not the same size as number of variables or equal to 1.")

    resultDF = data.set_index(['fill', 'mode'])

    if NoOfMapFunctions != 0:
        # Apply function on each field            
        for i in range(0, NoOfVar):
            resultDF[listOfVariables[i]] = resultDF[listOfVariables[i]].map(mapFunctionList[i * mapFunctionFlag])

    if NoOfAggFunctions != 0:
        temp_resultDF = pd.DataFrame()
        grupedData = resultDF.groupby(['fill', 'mode'])
        for i in range(0, NoOfVar):
            temp_resultDF[listOfVariables[i]] = grupedData[listOfVariables[i]].agg(aggFunctionList[i * aggFunctionFlag])
        resultDF = temp_resultDF

    return resultDF.reset_index().set_index('fill')

def LHCInjectionTree (fill_no, beam_mode = ['INJPROT', 'INJPHYS']):
    '''
    For a given fill number, this function constructs its injection tree. Treshold number might have to be adjusted.
    It represents the smallest jump in beam intensity that is the result of the injections.
    
    ========EXAMPLE========
    tree = importData.injectionTree(6666)
    
    for SPS, i in zip(tree.beam1.atSPS, range(len(tree.beam1.atSPS))):
        print('SPS '+str(i) + ': '+ str(SPS.atTime))
        for PS, j in zip(SPS.atPS, range(len(SPS.atPS))):
            print('\tPS '+str(i) + '.' + str(j) +': '+ str(PS.atTime))    
            for PSB, k in zip(PS.atPSB, range(len(PS.atPSB))):
                print('\t\tPSB '+str(i) + '.' + str(j) +'.'+str(k)+': '+ str(PSB.atTime))
    '''   
    patern1_var = 'LHC.BCTFR.A6R4.B1:BUNCH_FILL_PATTERN'
    patern2_var = 'LHC.BCTFR.A6R4.B2:BUNCH_FILL_PATTERN'

    # Parameters for injection data extractions
    all_injection_vars = ['%.TGM:BATCH', '%PS%.TGM:%DEST%']
    sps_destination_var = 'SPS.TGM:DDEST'
    cps_destination_var = 'CPS.TGM:DEST'
    psb_destination_var = 'PSB.TGM:DEST_G'

    cps_batch_var = 'CPS.TGM:BATCH'
    psb_batch_var = 'PSB.TGM:BATCH'

    sps_destination_beam1 = 'LHC1_TI2'
    sps_destination_beam2 = 'LHC2_TI8'
    cps_destination = 'LHC'
    psb_destination = 'LHC'

    sps_t_delta = pd.Timedelta('30s')
    ps_t_begin = pd.Timedelta('635ms') + pd.Timedelta('1200ms') * 3
    ps_t_end = - pd.Timedelta('635ms') + pd.Timedelta('1200ms') * 7
    psb_t_begin = pd.Timedelta('635ms')
    psb_t_end = pd.Timedelta('565ms')

    # This function can be used to construct an injection three in beam 1 and 2.
    # First the BEAM intensity data is extracted as it is the only reliable
    # source of information for the final level (SPS) injections to the beams
    paternDF = LHCCals2pd([patern1_var, patern2_var],fill_no, beam_mode)

    patern1DF = pd.DataFrame(paternDF['LHC.BCTFR.A6R4.B1:BUNCH_FILL_PATTERN'].map(np.array))
    patern2DF = pd.DataFrame(paternDF['LHC.BCTFR.A6R4.B2:BUNCH_FILL_PATTERN'].map(np.array))

    diff1DF = patern1DF.diff().dropna()
    bunches_added_b1 = pd.DataFrame(diff1DF['LHC.BCTFR.A6R4.B1:BUNCH_FILL_PATTERN'].map(lambda x : np.where(x == 1.0)[0]))
    bunches_added_b1['change in B1'] = (bunches_added_b1['LHC.BCTFR.A6R4.B1:BUNCH_FILL_PATTERN'].map(lambda x : x.size is not 0))

    diff2DF = patern2DF.diff().dropna()
    bunches_added_b2 = pd.DataFrame(diff2DF['LHC.BCTFR.A6R4.B2:BUNCH_FILL_PATTERN'].map(lambda x : np.where(x == 1.0)[0]))
    bunches_added_b2['change in B2'] = (bunches_added_b2['LHC.BCTFR.A6R4.B2:BUNCH_FILL_PATTERN'].map(lambda x : x.size is not 0))


    # In the end, all maxima that are lower than some treshold are discarded
    only_max_b1 = bunches_added_b1[bunches_added_b1['change in B1'] == True]
    only_max_b2 = bunches_added_b2[bunches_added_b2['change in B2'] == True]

    only_max = [only_max_b1, only_max_b2]
    # To get exact moments of injections, it is required to get all of the injection data
    injection_data = LHCCals2pd(all_injection_vars, fill_no, beam_mode)

    spsDF_b1 = injection_data[injection_data[sps_destination_var]== sps_destination_beam1][[sps_destination_var]]
    spsDF_b2 = injection_data[injection_data[sps_destination_var]== sps_destination_beam2][[sps_destination_var]]
    psDF = injection_data[injection_data[cps_destination_var] == cps_destination][[cps_batch_var]]
    psbDF = injection_data[injection_data[psb_destination_var] == psb_destination][[psb_batch_var]]

    # You have to extract only those injections that made it to the beams.
    # That is why the maximum extraction method is used.
    
    sps_injections_b1 = pd.DataFrame()
    sps_injections_b2 = pd.DataFrame()

    for t2 in only_max_b1.index:
        t1 = t2 - sps_t_delta
        new_injection = spsDF_b1[(spsDF_b1.index > t1) & (spsDF_b1.index < t2)]
        if not new_injection.index.empty and new_injection.index[0] not in sps_injections_b1.index:
            sps_injections_b1 = sps_injections_b1.append(new_injection)
        else:
            only_max_b1.drop(t2)

    for t2 in only_max_b2.index:
        t1 = t2 - sps_t_delta
        new_injection = spsDF_b2[(spsDF_b2.index > t1) & (spsDF_b2.index < t2)]
        if not new_injection.index.empty and new_injection.index[0] not in sps_injections_b2.index:
            sps_injections_b2 = sps_injections_b2.append(new_injection)
        else:
            only_max_b2.drop(t2)

    # These lists are related to the dotdictonary that will contain all of the other injections
    tree = dotdict()
    sps_list = [[], []]
    
    # This list containts the two sps injection dataframes needed for the creation of the tree
    sps_injections = [sps_injections_b1, sps_injections_b2]

    # First we iterate through beam numbers (b)
    for b in range(0, 2):
        
        #Then we iterate through all the sps injectios in particular beam 
        for i in range(0, len(sps_injections[b].index)):


            t_sps = sps_injections[b].index[i]
            sps_injections_dict = dotdict({"atTime":t_sps})
            sps_injections_dict.update({"atTimeBCT":only_max[b].index[i]})

            ps_injections = psDF[(psDF.index >= t_sps - ps_t_begin) & (psDF.index <= t_sps + ps_t_end)]

            ps_list = []
            
            #Then we iterate through all the ps injectios in particular sps injection
            for j in range(0, len(ps_injections.index)):

                t_ps = ps_injections.index[j]
                ps_injections_dict = dotdict({"atTime":t_ps, "atBatch" : ps_injections[cps_batch_var][j]})

                psb_injections = psbDF[(psbDF.index >= t_ps - psb_t_begin) & (psbDF.index <= t_ps + psb_t_end)]
                psb_list = []
                
                #Then we iterate through all the psb injectios in particular ps injection
                for k in range(0, len(psb_injections.index)):
                    t_psb = psb_injections.index[k]
                    psb_injections_dict = dotdict({"atTime":t_psb})
                    psb_list.append(psb_injections_dict)

                ps_injections_dict.update(dotdict({"atPSB" : psb_list}))
                ps_list.append(ps_injections_dict)

            sps_injections_dict.update({"atPS": ps_list})
            sps_injections_dict.update({"atBunches": only_max[b].iloc[i, 0]})
            sps_list[b].append(sps_injections_dict)

    tree["beam1"] = dotdict({"atSPS":sps_list[0]})
    tree["beam2"] = dotdict({"atSPS":sps_list[1]})

    # DETECTION OF DUMPS


    bunches_removed_b1 = pd.DataFrame(diff1DF['LHC.BCTFR.A6R4.B1:BUNCH_FILL_PATTERN'].map(lambda x : np.where(x == -1.0)[0]))
    bunches_removed_b1['change in B1'] = (bunches_removed_b1['LHC.BCTFR.A6R4.B1:BUNCH_FILL_PATTERN'].map(lambda x : x.size is not 0))
    bunches_removed_b1['empty'] = patern1DF['LHC.BCTFR.A6R4.B1:BUNCH_FILL_PATTERN'].map(lambda x : np.sum(x) == 0.0)

    bunches_removed_b2 = pd.DataFrame(diff2DF['LHC.BCTFR.A6R4.B2:BUNCH_FILL_PATTERN'].map(lambda x : np.where(x == -1.0)[0]))
    bunches_removed_b2['change in B2'] = (bunches_removed_b2['LHC.BCTFR.A6R4.B2:BUNCH_FILL_PATTERN'].map(lambda x : x.size is not 0))
    bunches_removed_b2['empty'] = patern2DF['LHC.BCTFR.A6R4.B2:BUNCH_FILL_PATTERN'].map(lambda x : np.sum(x) == 0.0)
    
    dump_b1 = bunches_removed_b1[(bunches_removed_b1['change in B1'] == True) & (bunches_removed_b1['empty'] == True)]
    dump_b2 = bunches_removed_b2[(bunches_removed_b2['change in B2'] == True) & (bunches_removed_b2['empty'] == True)]    
    
    dump_list = [[], []]
    dump_bunches = [dump_b1, dump_b2]
    
    for b in range(0, 2):
        for i in range(0, len(dump_bunches[b].index)):
            dump_dict = dotdict({"atTime":dump_bunches[b].index[i]})
            dump_dict.update({"atBunches":dump_bunches[b].iloc[i, 0]})
            dump_list[b].append(dump_dict)
    
    tree["beam1"].update({"atDump":dump_list[0]})      
    tree["beam2"].update({"atDump":dump_list[1]})
    
    lost_b1 = bunches_removed_b1[(bunches_removed_b1['change in B1'] == True) & (bunches_removed_b1['empty'] == False)]
    lost_b2 = bunches_removed_b2[(bunches_removed_b2['change in B2'] == True) & (bunches_removed_b2['empty'] == False)]    
    
    lost_list = [[], []]
    lost_bunches = [lost_b1, lost_b2]
    
    for b in range(0, 2):
        for i in range(0, len(lost_bunches[b].index)):
            lost_dict = dotdict({"atTime":lost_bunches[b].index[i]})
            lost_dict.update({"atBunches":lost_bunches[b].iloc[i, 0]})
            lost_list[b].append(lost_dict)
    
    tree["beam1"].update({"atLost":lost_list[0]})      
    tree["beam2"].update({"atLost":lost_list[1]})
            
    return tree

def dBLM2pd(fileName, bunchList,rollInterval,t1=None,t2=None):
    '''
    It returns a pd dataframe with the list of bunches. 
    
    The fileName is the hdf5 file to read.
        The dBLM folder is at
        /eos/project/dblm/TZ76
        so for instance you can find at 
        /eos/project/dblm/TZ76/TCP_18_B2/hist_BOX2_0724-195110_f6972_ADJUST.hdf5
        some the adjust of FILL 6972.
        
    The bunchList is the list of the bunches to consider in the pd dataframe.
    
    The rollInterval is delaying correctly the signal for proper gating
        +++ IMPORTANT +++
        Use rollInterval=20631 for Beam 1 and TZ76.
        Use rollInterval=13332 for Beam 2 and TZ76.
        For checking the delay have a look to the exa ple below.
    
    t1 and t2 are the timestamps to consider to windowing the analysis. 
    
    
    Thanks to A. Gorzawski and A. Poyet for providing the insight and the original code.

    === EXAMPLE ===
    myFile='/eos/project/dblm/TZ76/TCP_18_B2/hist_BOX2_0724-195110_f6972_ADJUST.hdf5'
    bunchList = np.array([10,390])
    t1 = pd.Timestamp('2018-07-24 19:51:10.443826',tz='UTC')
    t2 = pd.Timestamp('2018-07-25 20:51:10.443826',tz='CET')
    aux=importData.dBLM2pd(myFile,bunchList,rollInterval=13332,t1=t1,t2=t2)
    plt.plot(aux.resample('20s').mean())
    plt.ylim(0,30)
    
    # checks the delay of B1
    # in this fill we have two bunches in B1 in slot 10 and 50, 100 [start of the 12b],
    # 200 [start of the 48b], 283 [start of the 48b] and 366 [start of the 48b] >> the first bunch slot available is 0 and not 1!
    myFile='/eos/project/dblm/TZ76/TCP_18_B1/hist_BOX1_0724-195120_f6972_ADJUST.hdf5'
    a = h5py.File(myFile,'r')
    b = a['data']
    index=b.keys()[0]
    y=np.roll(b[index],20631,axis=0)
    x=np.linspace(0,3564,len(b[index]))
    a=plt.plot(x,y)
    plt.xlim(365,366+49)# bunch 10 shuld ne between position 10 and 11.
    
    # checks the delay of B2
    # in this fill we have two bunches in B2 in slot 10 and 390 >> the first bunch slot available is 0 and not 1!
    myFile='/eos/project/dblm/TZ76/TCP_18_B2/hist_BOX2_0724-195110_f6972_ADJUST.hdf5'
    a = h5py.File(myFile,'r')
    b = a['data']
    index=b.keys()[0]
    y=np.roll(b[index],13332,axis=0)
    x=np.linspace(0,3564,len(b[index]))
    a=plt.plot(x,y)
    plt.xlim(10,11)# bunch 10 shuld ne between position 10 and 11.
    '''

    '''
    === ORIGINAL CODE FROM AXEL ===
    # I preferred to use pandas systematically
    final_DF = pd.DataFrame()
    a = h5py.File(File,'r')
    b = a['data']
    keys  = b.keys()
    interestingKeys = []
    myInterestingKeys = []
    for i in range(len(keys)):
        if (datetime.datetime.strptime(keys[i],'%Y-%m-%d %H:%M:%S.%f')>t1) & (datetime.datetime.strptime(keys[i],'%Y-%m-%d %H:%M:%S.%f')<t2):
            interestingKeys.append(keys[i])
            myInterestingKeys.append(datetime.datetime.strptime(keys[i],'%Y-%m-%d %H:%M:%S.%f'))
    aux = []
    for i in interestingKeys:
        aux.append(np.roll(b[i].value,13322,axis=0))
    myDF = pd.DataFrame(np.stack(aux),index = myInterestingKeys)
    bunchCenters = np.zeros(len(fill))
    for i in range(len(fill)):
        bunchCenters[i] = int(fill[i]/3564.*55578)
        final_DF['bunch_'+str(fill[i])] = myDF.ix[:,(bunchCenters[i]-nbBins/2):(bunchCenters[i]+nbBins/2)].sum(axis=1).diff().resample(str(secondOfResampling)+'s').sum()/secondOfResampling
    return final_DF
    '''
    a = h5py.File(fileName,'r')
    b = a['data']
    
    myDF=pd.DataFrame()
    
    aux=pd.DataFrame(list(b.keys()),index=list(map(pd.Timestamp,list(b.keys()))),columns=['KEY'] )
    aux.index=aux.index.tz_localize('CET').tz_convert('UTC')
    if t1==None: t1=aux.index[0]
    if t2==None: t2=aux.index[-1]
    aux=aux[t1:t2].copy()
    # the rollInterval depends on the electric delay of the acquisition device wrt the bunch 0
    aux['VALUE']=aux['KEY'].apply(lambda x:np.roll(b[x],rollInterval,axis=0)) 
    for i in bunchList:
        # Integrating between 5 and 95% of the bunch slot and differentiating
        myDF['bunch_'+str(i)]=aux['VALUE'].apply(lambda x:np.sum(x[int((i+0.05)/3564.*55578):int((i+0.95)/3564.*55578)])).diff()
    return myDF

def LHCBunchLifeTimeInSquezee (noOfFill, resample_second = 60, duration_of_stable = pd.Timedelta('0 days 00:10:00')):
    '''
    
    This function returns the bunch lifetime in the squezee and optionaly in stable (default first 10 minutes) mode for the requested fill
    
    ===EXAMPLE===
    beam1DF, beam2DF = importData.LHCBunchLifeTimeInSquezee (6778)
    beam1DF, beam2DF = importData.LHCBunchLifeTimeInSquezee (6778, resample_second = 60, duration_of_stable = pd.Timedelta('0 days 00:10:00'))
    
    '''
    
    bunch_intensity = LHCCals2pd(['LHC.BCTFR.A6R4.B%:BUNCH_INTENSITY'], noOfFill, ['SQUEEZE'])#, flag='duration', duration=pd.Timedelta('0 days 00:05:00'))
    bunch_intensity = bunch_intensity.append(LHCCals2pd(['LHC.BCTFR.A6R4.B%:BUNCH_INTENSITY'], noOfFill, ['STABLE'], flag='duration', duration = duration_of_stable))
    
    noOfBunch = len(bunch_intensity['LHC.BCTFR.A6R4.B1:BUNCH_INTENSITY'].iloc[0])

    beam1DF=pd.DataFrame()
    beam2DF=pd.DataFrame()

    for i in range(0, noOfBunch):
        a1 = bunch_intensity['LHC.BCTFR.A6R4.B1:BUNCH_INTENSITY'].dropna().apply(lambda x: x[i]).resample(str(resample_second)+'s').mean()
        b1 = a1.diff()/resample_second
        beam1DF['lifetime of bunch ' + str(i)+ ' [h]'] = - ((a1/b1).dropna())/3600

        a2 = bunch_intensity['LHC.BCTFR.A6R4.B2:BUNCH_INTENSITY'].dropna().apply(lambda x: x[i]).resample(str(resample_second)+'s').mean()
        b2 = a2.diff()/resample_second
        beam2DF['lifetime of bunch ' + str(i)+ ' [h]'] = - ((a2/b2).dropna())/3600
    
    return beam1DF, beam2DF

def bunch2SPSInjection (tree, noBunch):
    '''
    This function identifies in which SPS injection of a paricular tree a bunch is located.
    ===EXAMPLE===
    fillNo = 6666
    bunchNo = 522
    tree = importData.LHCInjectionTree(fillNo)
    noOfSPS = importData.bunch2SPSInjection (tree, noBunch)
    # Last time bunchNo was injected in beam 1
    noOfSPS = noOfSPS[0][-1]
    '''
    noBunch = 522
    noOfSPS = [[], []]

    beam = [tree.beam1, tree.beam2]

    for b in range(0, 2):
        for i in range(len(beam[b].atSPS)):
            if noBunch in beam[b].atSPS[i].atBunches:
                noOfSPS[b].append(i)
                
    return noOfSPS

def _fillBeamModes(fillDF):
    auxNoFill=fillDF[fillDF['mode']!='FILL']
    if len(auxNoFill)>1:
        myDF=pd.DataFrame({'endTime':auxNoFill.iloc[1:].startTime.values, 'startTime':auxNoFill.iloc[0:-1].endTime.values,'mode':'NONE'},index=auxNoFill.iloc[1:].index)
        myDF['duration']=myDF['endTime']-myDF['startTime']
        myDF['startTime']=myDF['startTime'].apply(lambda x: x.tz_localize('UTC'))
        myDF['endTime']=myDF['endTime'].apply(lambda x: x.tz_localize('UTC'))
    else:
        myDF=pd.DataFrame()
    smallDF=pd.DataFrame({'mode':['NONE'], 'startTime':[fillDF.iloc[0].startTime], 'endTime': [fillDF.iloc[1].startTime]},index=[fillDF.index[0]])
    smallDF['duration']=smallDF['endTime']-smallDF['startTime']
    return (pd.concat([fillDF,myDF,smallDF], sort=True)[['mode','startTime','endTime','duration']]).sort_values(by=['startTime'])

def _LHCInstant(t1):
    '''
    LHCInstant(t1)
    
    Return the fill information at the instant t1.
    
    ===Example===   
    t1 = pd.Timestamp('2018-05-22 02:10:15', tz='CET')
    importData._LHCInstant(t1)
    '''
    if t1.tz==None: t1=t1.tz_localize('UTC')
    else: t1=t1.astimezone('UTC')
    aux=cals2pd(['HX:FILLN'],t1,'last')['HX:FILLN'].values
    if len(aux)>0:
        aux=LHCFillsByNumber(np.int(aux[0]))
        aux=_fillBeamModes(aux)
        aux=aux[aux['mode']!='FILL']
        aux['test']=aux.apply(lambda x: x['startTime']<=t1<x['endTime'] , axis=1)
        if len(aux)==0:
            return pd.DataFrame();
        aux= aux[aux['test']]
        del aux['test']
        return aux
    else:
        return pd.DataFrame()
