
import importData
import pjlsa

pd=importData.pd     # is the pandas package
lsa = pjlsa.LSAClient()

def LHClsa2pd(parameterList,beamprocessList,t1,t2):
    if t1.tz==None:
        t1=t1.tz_localize('UTC')
        if verbose: print('t1 is UTC localized: ' + str(t1))

    # LSA needs CET as internal variable
    t1=t1.astimezone('CET')

    if t2.tz==None:
        t2=t2.tz_localize('UTC')
        if verbose: print('t2 is UTC localized: '+ str(t2))
   
    # LSA needs CET as internal variable
    t2=t2.astimezone('CET')
    
    if isinstance(parameterList,str):
        parameterList=[parameterList]
    
    if isinstance(beamprocessList,str):
        beamprocessList=[beamprocessList]
    
    beamprocessDFList=[]
    for j in beamprocessList:
        a=pd.DataFrame()
        for i in parameterList:
            trims = lsa.getTrims(beamprocess=j,
                             parameter=i,
                             start=t1, end=t2)
            if len(trims):
                a=pd.merge(a,pd.DataFrame(index=pd.to_datetime(trims[i].time,unit='s'),data=trims[i].data, columns=[i]), how='outer',left_index=True,right_index=True)

        beamprocessDFList.append(a);
    
    # We assume non-overlapping beam process
    beamprocessDF=pd.concat(beamprocessDFList)
    if len(beamprocessDF):
        beamprocessDF.index=beamprocessDF.index.tz_localize('UTC')
    return beamprocessDF
