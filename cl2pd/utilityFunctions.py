def fuseDF(df1,df2):
    myDF=pd.DataFrame()
    for i in sorted(np.unique(list(df1.columns)+list(df2.columns))):
        if (i in df1) & (i in df2):
            myDF=pd.concat([myDF,pd.DataFrame(df1[i].dropna()),pd.DataFrame(df2[i].dropna())])
        else:
            if (i in df1):
                myDF=pd.concat([myDF,pd.DataFrame(df1[i].dropna())])
            else:
                myDF=pd.concat([myDF,pd.DataFrame(df2[i].dropna())])
    myDF=myDF.groupby(myDF.index).first()
    return myDF.sort_index()


def getDataFrameSize_MB(myDF):
    '''
    Compute the size of a pandas dataframe in MB.
    '''
    return myDF.memory_usage(deep='True').sum()/1024./1024.

def mergeDF(df1,df2):
    """
    It returns a new dataframe obtained by merging df1 and df2 with no duplicated columns.
    """

    return pd.merge(df1,df2[df2.columns.difference(df1.columns)],
                 left_index=True, 
                 right_index=True, 
                 how='outer')

def concatDF(df1,df2):
    """
    It returns a new dataframe that is the concatation of df1 and df2.
    """      
    aux=pd.concat([df1,df2]).sort_index()
    return aux.groupby(aux.index).first()
