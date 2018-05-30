import pandas as pd 
import numpy as np
import os
# Fundamental contribution by R. De Maria et al.
import pytimber

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
        if verbose: print('t1 is UTC localized: ' + str(t1))

    # pyTimber needs CET as internal variable
    t1=t1.astimezone('CET')

    if not isinstance(t2, str):
        if t2.tz==None:
            t2=t2.tz_localize('UTC')
            if verbose: print('t2 is UTC localized: '+ str(t2))
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
            if verbose: print('Elaborating variable: '+ i)
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
            if verbose: print('Time window: '+str(i+1)) 
            aux=_noSplitcals2pd(listOfVariables,times[i],times[i+1], fundamental=fundamental, verbose=verbose)
            myDF=pd.concat([myDF,aux])
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
            out=pd.concat([fillsDetails,fillsSummary])
            out=out.sort_values('startTime')[['mode','startTime','endTime','duration']]
            out['endTime']=out['endTime'].apply(pd.Timestamp)
            out['duration']=out['endTime']-out['startTime']
        else:
            out=pd.concat([fillsDetails,fillsSummary])
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

        if verbose: print('Fill ' + str(i))

        DATA=cals.getLHCFillData(i)

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
        fillsSummary=pd.concat([aux,fillsSummary])
        fillsDetails=pd.concat([auxDataFrame,fillsDetails])

    # The timestamps are localized and the dataframes are sorted
    if len(fillsSummary):
        fillsSummary['startTime']=fillsSummary['startTime'].apply(_UTClocalizeMe)
        fillsSummary['endTime']=fillsSummary['endTime'].apply(_UTClocalizeMe)
        fillsSummary=fillsSummary.sort_values(['startTime'])

        fillsDetails['startTime']=fillsDetails['startTime'].apply(_UTClocalizeMe)
        fillsDetails['endTime']=fillsDetails['endTime'].apply(_UTClocalizeMe)

        fillsDetails=fillsDetails.sort_values(['startTime'])

    fillsSummary['mode']='FILL'
    
    if len(fillsSummary)>0:
        if (len(fillsSummary)==1) & (fillsSummary.iloc[0]['duration']==None):
            # If there is only the online FILL (so not yet completed)
            # TODO: very cumbersome casting (first to string, then concatenation, then to timestamp)
            # I am no satisfied [GS]
            if verbose: print('Online FILL...')
            fillsSummary['endTime']='NaT'
            fillsSummary['duration']='NaT'
            fillsDetails['endTime']=fillsDetails['endTime'].astype(str)
            fillsDetails['duration']=fillsDetails['duration'].astype(str)
            aux=pd.concat([fillsDetails,fillsSummary])
            aux=aux.sort_values('startTime')[['mode','startTime','endTime','duration']]
            aux['endTime']=aux['endTime'].apply(pd.Timestamp)
            aux['duration']=aux['endTime']-aux['startTime']
        else:
            aux=pd.concat([fillsDetails,fillsSummary])
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
    massiFile=pd.concat(pdList)
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
                    print("Problem parsing: "+ line)
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
        aux=TFS2pd('/eos/user/s/sterbini/MD_ANALYSIS/2018/LHC MD Optics/collisionAt25cm_180urad/lhcb1_thick.survey')
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
                print("The column "+ i + ' is empty.')
            else:
                myColumns.append(i)
                myList.append(myContainer)
                
        optics=pd.DataFrame(np.transpose(myList), index=a.S,columns=myColumns)

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
        aux=tfs2pd(['/eos/user/s/sterbini/MD_ANALYSIS/2018/LHC MD Optics/collisionAt25cm_180urad/lhcb1_thick.survey',
        '/eos/user/s/sterbini/MD_ANALYSIS/2018/LHC MD Optics/collisionAt25cm_180urad/lhcb1_thick.twiss'])
    '''
    if isinstance(myList, list):
        aux=[]
        for i in np.unique(myList):
            aux.append(_tfs2pd(i))
        return pd.concat(aux)
    else:
        return _tfs2pd(myList)
