import matplotlib.pyplot as plt
import datetime 
import pandas as pd
import numpy as np

def setSourcePlot(gca, pltDescription,x=0.99,y=0.01,horizontalalignment='right',\
                  color='k',verticalalignment='bottom',rotation=0,fontsize=7):
  '''
  Comment the plot adding for instance the source script.
   
  It requires an axis (gca) and a string (pltDescription).
   
  ===EXAMPLE===
  plt.plot([1,2,3,])
  setSourcePlot(plt.gca(), pltDescription,x=0.99,y=0.01,horizontalalignment='right',\
                  color='k',verticalalignment='bottom',rotation=0,fontsize=7)
  '''
  plt.text(x,y,pltDescription, 
             horizontalalignment=horizontalalignment, 
             color=color,
             verticalalignment=verticalalignment, 
             transform=gca.transAxes,rotation=rotation, fontsize=fontsize);
  
def setXDateTicks(ax, hours=1., myFormat='%H:%M', startDatetime=datetime.datetime.utcfromtimestamp(0)):
    """
    setXDateTicks(ax=plt.gca(), hours=1., myFormat='%H:%M', startDatetime=datetime.datetime.utcfromtimestamp(0))
    ax: specify the axis
    hours: specify the interval 
    myFormat: specify the format
    startDatetime: specify the starting time (to have round captions)
    """
    aux=ax.get_xlim()
    serial = aux[0]
    if startDatetime ==datetime.datetime.utcfromtimestamp(0):
        seconds = (serial - 719163.0) * 86400.0
        startDatetime=datetime.datetime.utcfromtimestamp(seconds)
    serial = aux[1]
    seconds = (serial - 719163.0) * 86400.0
    date_end=datetime.datetime.utcfromtimestamp(seconds)
    t = np.arange(startDatetime, date_end, datetime.timedelta(hours=hours)).astype(datetime.datetime)
    ax.set_xticks(t);
    myFmt =mdates.DateFormatter(myFormat)
    ax.xaxis.set_major_formatter(myFmt);
    return startDatetime

def setArrowLabel(ax, label='myLabel',arrowPosition=(0,0),labelPosition=(0,0), myColor='k', arrowArc_rad=-0.2):
    return ax.annotate(label,
                  xy=arrowPosition, xycoords='data',
                  xytext=labelPosition, textcoords='data',
                  size=10, color=myColor,va="center", ha="center",
                  bbox=dict(boxstyle="round4", fc="w",color=myColor,lw=2),
                  arrowprops=dict(arrowstyle="-|>",
                                  connectionstyle="arc3,rad="+str(arrowArc_rad),
                                  fc="w", color=myColor,lw=2), 
                  )
  
def setShadedRegion(ax,color='g' ,xLimit=[0,1],alpha=.1):
    """
    setShadedRegion(ax,color='g' ,xLimit=[0,1],alpha=.1)
    ax: plot axis to use
    color: color of the shaded region
    xLimit: vector with two scalars, the start and the end point
    alpha: transparency settings
    """
    aux=ax.get_ylim()
    plt.gca().fill_between(xLimit, 
                       [aux[0],aux[0]],  [aux[1],aux[1]],color=color, alpha=alpha)
    ax.set_ylim(aux)
    
def plotLHCFill(myFill,myTitle,startTime):
    """
    It returns the plot of the beam modes of the pd DF.

    ===Example===
    myFill=importData.LHCFillsByNumber([6797,6798,6799])
    plotFunctions.plotLHCFill(myFill,myTitle="This is my title",startTime=pd.Timestamp('2018-06-14 19:39:39.435000'))
    """ 
    aux=myFill[myFill['mode']=='FILL']
    b=myFill[myFill['mode']!='FILL']
    def colorMe(i):
        if np.mod(i,2):
            return "m"
        else:
            return "c"

    for i in aux.index:
        plt.gca().fill_between([pd.Timestamp(aux[aux.index==i]['startTime'].values[0]).to_pydatetime(),
                                pd.Timestamp(aux[aux.index==i]['endTime'].values[0]).to_pydatetime()], [0,0], [2.1,2.1],color=colorMe(i), alpha=.1)

        bb=b[b.index==i]
        bbb=bb[bb['mode']=='NOBEAM']
        if len(bbb): 
            plt.gca().fill_between([pd.Timestamp(bbb['startTime'].values[0]).to_pydatetime(),
                                    pd.Timestamp(bbb['endTime'].values[0]).to_pydatetime()], [.8,.8], [.9,.9],color='r')

        bb=b[b.index==i]
        bbb=bb[bb['mode']=='CYCLING']
        if len(bbb): 
            plt.gca().fill_between([pd.Timestamp(bbb['startTime'].values[0]).to_pydatetime(),
                                    pd.Timestamp(bbb['endTime'].values[0]).to_pydatetime()], [.9,.9], [1,1],color='r')

        bb=b[b.index==i]
        bbb=bb[bb['mode']=='SETUP']
        if len(bbb): 
            plt.gca().fill_between([pd.Timestamp(bbb['startTime'].values[0]).to_pydatetime(),
                                    pd.Timestamp(bbb['endTime'].values[0]).to_pydatetime()], [1,1], [1.1,1.1],color='r')

        bb=b[b.index==i]
        bbb=bb[bb['mode']=='INJPROT']
        if len(bbb): 
            plt.gca().fill_between([pd.Timestamp(bbb['startTime'].values[0]).to_pydatetime(),
                                    pd.Timestamp(bbb['endTime'].values[0]).to_pydatetime()], [1.1,1.1], [1.2,1.2],color='k')
        bb=b[b.index==i]
        bbb=bb[bb['mode']=='INJPHYS']
        if len(bbb): 
            plt.gca().fill_between([pd.Timestamp(bbb['startTime'].values[0]).to_pydatetime(),
                                    pd.Timestamp(bbb['endTime'].values[0]).to_pydatetime()], [1.2,1.2], [1.3,1.3],color='orange')

        bb=b[b.index==i]
        bbb=bb[bb['mode']=='PRERAMP']
        if len(bbb): 
            plt.gca().fill_between([pd.Timestamp(bbb['startTime'].values[0]).to_pydatetime(),
                                    pd.Timestamp(bbb['endTime'].values[0]).to_pydatetime()], [1.3,1.3], [1.4,1.4],color='b')

        bb=b[b.index==i]
        bbb=bb[bb['mode']=='RAMP']
        if len(bbb): 
            plt.gca().fill_between([pd.Timestamp(bbb['startTime'].values[0]).to_pydatetime(),
                                    pd.Timestamp(bbb['endTime'].values[0]).to_pydatetime()], [1.4,1.4], [1.5,1.5],color='b')

        bb=b[b.index==i]
        bbb=bb[bb['mode']=='FLATTOP']
        if len(bbb): 
            plt.gca().fill_between([pd.Timestamp(bbb['startTime'].values[0]).to_pydatetime(),
                                    pd.Timestamp(bbb['endTime'].values[0]).to_pydatetime()], [1.5,1.5], [1.6,1.6],color='b')

        bb=b[b.index==i]
        bbb=bb[bb['mode']=='SQUEEZE']
        if len(bbb): 
            plt.gca().fill_between([pd.Timestamp(bbb['startTime'].values[0]).to_pydatetime(),
                                    pd.Timestamp(bbb['endTime'].values[0]).to_pydatetime()], [1.6,1.6], [1.7,1.7],color='g')

        bb=b[b.index==i]
        bbb=bb[bb['mode']=='ADJUST']
        if len(bbb): 
            plt.gca().fill_between([pd.Timestamp(bbb['startTime'].values[0]).to_pydatetime(),
                                    pd.Timestamp(bbb['endTime'].values[0]).to_pydatetime()], [1.7,1.7], [1.8,1.8],color='g')

        bb=b[b.index==i]
        bbb=bb[bb['mode']=='STABLE']
        if len(bbb): 
            plt.gca().fill_between([pd.Timestamp(bbb['startTime'].values[0]).to_pydatetime(),
                                    pd.Timestamp(bbb['endTime'].values[0]).to_pydatetime()], [1.8,1.8], [1.9,1.9],color='g')

        bb=b[b.index==i]
        bbb=bb[bb['mode']=='BEAMDUMP']
        if len(bbb): 
            plt.gca().fill_between([pd.Timestamp(bbb['startTime'].values[0]).to_pydatetime(),
                                    pd.Timestamp(bbb['endTime'].values[0]).to_pydatetime()], [1.9,1.9], [2,2],color='k')
            plt.plot(pd.Timestamp(bbb['startTime'].values[0]).to_pydatetime(),1.95,'vr',ms=12)

        bb=b[b.index==i]
        bbb=bb[bb['mode']=='RAMPDOWN']
        if len(bbb): 
            plt.gca().fill_between([pd.Timestamp(bbb['startTime'].values[0]).to_pydatetime(),
                                    pd.Timestamp(bbb['endTime'].values[0]).to_pydatetime()], [2,2], [2.1,2.1],color='k')


        myTest=aux[aux.index==i]['duration']> pd.Timedelta(hours=.3)
        if myTest.values[0]:
            myDiff=(pd.to_datetime(aux[aux.index==i]['endTime'].values[0])-pd.to_datetime(aux[aux.index==i]['startTime'].values[0]))/2
            myTime=pd.to_datetime(aux[aux.index==i]['startTime'].values[0])+myDiff
            plt.text(myTime,.6 ,str(i), bbox=dict(facecolor='w', alpha=1),horizontalalignment='center',verticalalignment='center', rotation=90)
    plt.yticks([.85, .95, 1.05, 1.15, 1.25, 1.35, 1.45, 1.55, 1.65, 1.75, 1.85, 1.95, 2.05],
               ['NOBEAM','CYCLING','SETUP','INJPROT','INJPHYS',
                'PRERAMP','RAMP','FLATTOP','SQUEEZE','ADJUST','STABLE','BEAMDUMP','RAMPDOWN']);
    plt.ylim(0.4,2.1);
    plt.title(myTitle)
    plt.xticks(rotation=45)
    plt.xlabel('UTC time [month-day hh]');
    return plt.gca()

def shadedDF(gca, df, color='g', alpha=0.5):
    '''
    It colors with a fill_between a plot using the information from a pd df
    that has the 'startTime' and 'endTime'.
    
    ===EXAMPLE===
    fillDF=importData.LHCFillsByNumber([6797,6798,6799])
    plotFunctions.shadedDF(plt.gca(), fillDF[fillDF['mode']=='INJPHYS'], color='y',alpha=.3)
    plt.xticks(rotation=45);
    plt.xlabel('UTC time [month-day hh]');
    '''
    myYlim=gca.get_ylim()
    for i in df.iterrows():
        st=pd.Timestamp(i[1]['startTime']).to_pydatetime()
        et=pd.Timestamp(i[1]['endTime']).to_pydatetime()
        gca.fill_between([st, et], [myYlim[0],myYlim[0]], [myYlim[1],myYlim[1]],color=color, alpha=alpha)
    gca.set_ylim(myYlim)    

def plot_BBMatrix(BBMatrixLHC, B1_bunches, B2_bunches,alpha=.2, width=1):
    """
    It plots a beam-beam matrix.

    ===Example===
    from cl2pd import importData
    from cl2pd import bbFunctions
    from cl2pd import plotFunctions
    np=plotFunctions.np
    pd=plotFunctions.pd

    myMatrix=bbFunctions.computeBBMatrix(numberOfLRToConsider=20)
    fillingSchemeDF=importData.cals2pd(['LHC.BCTFR.A6R4.B%:BUNCH_FILL_PATTERN'],
                               pd.Timestamp('2017-09-13 18:00',tz='CET'),
                               pd.Timestamp('2017-09-13 18:01',tz='CET'))
    B1_bunches=np.where(fillingSchemeDF.iloc[0]['LHC.BCTFR.A6R4.B1:BUNCH_FILL_PATTERN'])[0]
    B2_bunches=np.where(fillingSchemeDF.iloc[0]['LHC.BCTFR.A6R4.B2:BUNCH_FILL_PATTERN'])[0]

    plotFunctions.plot_BBMatrix(BBMatrixLHC, B1_bunches, B2_bunches)
    """ 
    plt.figure(figsize=(10,10))
    plt.jet()
    plt.imshow(BBMatrixLHC,interpolation='none')
    plt.axis('tight')
    plt.xlabel('BEAM 2')
    plt.ylabel('BEAM 1')
    plt.axis('equal')
    plt.axis('tight');
    plt.tick_params(direction='inout')
    for i in B2_bunches:
        setShadedRegion(plt.gca(), xLimit=[i-width+1, i+width],alpha=alpha,color='w')

    for i in B1_bunches:
        plt.gca().fill_between([0,3564], [i-width+1,i-width+1],  [i+width,i+width],color='w', alpha=alpha)

    setArrowLabel(ax=plt.gca(),label='IP1/5',labelPosition=(2000,2000), arrowPosition=(2000,2000), myColor='k')
    setArrowLabel(ax=plt.gca(),label='IP2',labelPosition=(2000,1100), arrowPosition=(2000,1100), myColor='k')
    setArrowLabel(ax=plt.gca(),label='IP8',labelPosition=(2000,2900), arrowPosition=(2000,2900), myColor='k')
    setArrowLabel(ax=plt.gca(),label='IP8',labelPosition=(3130,3564-3130), arrowPosition=(3130,3564-3130), myColor='k')
    setArrowLabel(ax=plt.gca(),label='IP2',labelPosition=(3564-3130,3130), arrowPosition=(3564-3130,3130), myColor='k');
    return plt.gca()

def plotBBEncounterSchedule(BBEncounterSchedule,beam,bunch,exp):
    '''
    Plot the encounter schedule for a specific beam, bunch, and experiment.
    
    ===EXAMPLE===
    B1_bunches=np.array([0,1,2])
    B2_bunches=np.array([0,1,2])
    myMatrix=bbFunctions.computeBBMatrix(numberOfLRToConsider=25)
    results=bbFunctions.BBEncounterSchedule(B1_bunches, B2_bunches, myMatrix)
    plotFunctions.plotBBEncounterSchedule(results,beam='atB1',exp='atCMS',bunch=0)
    '''
    bunch_aux=bunch
    bunch='at'+format(bunch,'04d')
    x=BBEncounterSchedule[beam][bunch][exp]['atPositions']
    y=[1]*len(x)
    plt.plot(x,y,'ok')
    plt.xlim(-25,25)
    plt.ylim(.94, 1.06)

    plt.yticks([])
    plt.xlabel('BBLR encounter position')
    plt.title(beam[2:]+ ', ' + exp[2:] + ', bunch=' + str(bunch_aux))

    if len(x)>0:
        encounters=BBEncounterSchedule[beam][bunch][exp]['atEncounters']
        if beam=='B1':
            setArrowLabel(plt.gca(), label=str(encounters[0]), arrowPosition=(x[0], y[0]), labelPosition=(x[0]-5, y[0]+.01), myColor='b', arrowArc_rad=0.2)
            setArrowLabel(plt.gca(), label=str(encounters[-1]), arrowPosition=(x[-1], y[-1]), labelPosition=(x[-1]+5, y[-1]-.01), myColor='r', arrowArc_rad=0.2)
        else:
            setArrowLabel(plt.gca(), label=str(encounters[0]), arrowPosition=(x[0], y[0]), labelPosition=(x[0]-5, y[0]+.01), myColor='b', arrowArc_rad=-0.2)
            setArrowLabel(plt.gca(), label=str(encounters[-1]), arrowPosition=(x[-1], y[-1]), labelPosition=(x[-1]+5, y[-1]-.01), myColor='r', arrowArc_rad=-0.2)
    plt.grid(ls=':')
    return plt.gca()
