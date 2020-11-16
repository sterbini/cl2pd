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

def setArrowLabel(ax, label='myLabel',arrowPosition=(0,0),labelPosition=(0,0), myColor='k', arrowArc_rad=-0.2, textSize=10):
    return ax.annotate(label,
                  xy=arrowPosition, xycoords='data',
                  xytext=labelPosition, textcoords='data',
                  size=textSize, color=myColor,va="center", ha="center",
                  bbox=dict(boxstyle="round4", fc="w",color=myColor,lw=2),
                  arrowprops=dict(arrowstyle="-|>",
                                  connectionstyle="arc3,rad="+str(arrowArc_rad),
                                  fc="w", color=myColor,lw=2), 
                  )
  
def setShadedRegion(ax,color='g' ,xLimit=[0,1], yLimit='FullRange',alpha=.1):
    """
    setShadedRegion(ax,color='g' ,xLimit=[0,1],alpha=.1)
    ax: plot axis to use
    color: color of the shaded region
    xLimit: vector with two scalars, the start and the end point
    alpha: transparency settings
    yLimit: if set to "FullRange" shaded the entire plot in the y direction
    If you want to specify an intervall, please enter a two scalar vector as xLimit
    """
    if yLimit=='FullRange':
        aux=ax.get_ylim()
        plt.gca().fill_between(xLimit, [aux[0],aux[0]],  [aux[1],aux[1]],color=color, alpha=alpha)
        ax.set_ylim(aux)
    else:
        plt.gca().fill_between(xLimit, 
                    [yLimit[0],yLimit[0]],  [yLimit[1],yLimit[1]],color=color, alpha=alpha)
    
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

def LHCPlotLossRateAtSqueeze(fillNo, whichIP = 1, first = 1, last = 3564, resample_second = 60, beam1DF = None, beam2DF = None, fig = None, ax = None):    
    '''    
    Plots inverse function of lifetime for a single bunch in the time moment where beta functions is lowest for
    chosen IP.
    
    ===EXAMPLE===
    fig, ax = plt.subplots(1, 1)
    beam1DF, beam2DF = importData.LHCBunchLifeTimeInSquezee (6778, resample_second = 60, duration_of_stable = pd.Timedelta('0 days 00:10:00'))
    plotFunctions.LHCPlotLossRateAtSqueeze(6778, first = 500, last = 800, beam1DF = beam1DF, beam2DF = beam2DF, fig = fig, ax = ax)    
    '''    
    if beam1DF is None or beam2DF is None:        
        beam1DF, beam2DF = importData.LHCBunchLifeTimeInSquezee (fillNo, resample_second = 60)
        
    if fig is None or ax is None:
        fig, ax = plt.subplots(1, 1)
        
    last_bunch = importData.LHCCals2pd(['HX:BETASTAR_IP1'], fillNo, 'STABLE', flag = 'last')
    values = beam1DF.loc[last_bunch.index.floor('min')].values
    ax.plot(np.arange(first - 1, last - 1), 100/values[0, first - 1:last - 1], 'b')
    
    values = beam2DF.loc[last_bunch.index.floor('min')].values
    ax.plot(np.arange(first - 1, last - 1), 100/values[0, first - 1:last - 1], 'r')
    
    ax.set(xlabel = 'Bunch number', ylabel = 'Loss rate [%]')
    ax.legend(['Beam 1', 'Beam 2'])

    return fig, ax

def LHCPlotBunchPartnerIntensity(fillNo, bunchNo, scheduleDF = None, intensityDF = None, fig = None, ax = None):
    '''
    This function plots intensities of bunches in beam two that interact with bunchNo 
    from beam one. 
    
    scheduleDF represents the Beam one collision schedule 
    intensityDF represents the intensities of bunches in the 4 IPs
    
    ===EXAMPLE===
    fillNo = 6776
    
    beam1DF, beam2DF = importData.LHCBunchLifeTimeInSquezee (fillNo, resample_second = 60, duration_of_stable = pd.Timedelta('0 days 00:10:00'))
    fillingSchemeDF=importData.LHCFillsAggregation(['LHC.BCTFR.A6R4.B%:BUNCH_FILL_PATTERN'], fillNo, ['FLATTOP'],flag='next')
    
    B1_bunches = fillingSchemeDF['LHC.BCTFR.A6R4.B1:BUNCH_FILL_PATTERN'].dropna().iloc[0]
    B2_bunches = fillingSchemeDF['LHC.BCTFR.A6R4.B2:BUNCH_FILL_PATTERN'].dropna().iloc[0]
    
    scheduleDF = bbFunctions.B1CollisionScheduleDF(B1_bunches, B2_bunches, 25)
    intensityDF = importData.LHCFillsAggregation(['LHC.BCTFR.A6R4.B2:BUNCH_INTENSITY'], fillNo, ['STABLE'],flag='last')
    
    fig, ax = plt.subplots(2, 3, figsize = (20, 10))

    selected_bunches = [941, 997, 1050]

    plotFunctions.LHCPlotLossRateAtSqueeze(fillNo, whichIP=1, first=800, last=1500, resample_second=60, beam1DF=beam1DF, beam2DF=beam2DF, fig = fig, ax = ax[0][0])
    plotFunctions.LHCPlotLossRateAtSqueeze(fillNo, whichIP=1, first=800, last=1500, resample_second=60, beam1DF=beam1DF, beam2DF=beam2DF, fig = fig, ax = ax[0][1])
    plotFunctions.LHCPlotLossRateAtSqueeze(fillNo, whichIP=1, first=800, last=1500, resample_second=60, beam1DF=beam1DF, beam2DF=beam2DF, fig = fig, ax = ax[0][2])

    plotFunctions.LHCPlotBunchPartnerIntensity(fillNo, selected_bunches[0], scheduleDF = scheduleDF, intensityDF = intensityDF, fig = fig, ax = ax[1][0])
    plotFunctions.LHCPlotBunchPartnerIntensity(fillNo, selected_bunches[1], scheduleDF = scheduleDF, intensityDF = intensityDF, fig = fig, ax = ax[1][1])
    plotFunctions.LHCPlotBunchPartnerIntensity(fillNo, selected_bunches[2], scheduleDF = scheduleDF, intensityDF = intensityDF, fig = fig, ax = ax[1][2])

    bunches = ax[0][0].lines[0].get_xydata()[:, 0]
    loss_rate = ax[0][0].lines[0].get_xydata()[:, 1]

    ax[0][0].plot(selected_bunches[0], loss_rate[bunches == selected_bunches[0]], 'yo')
    ax[0][1].plot(selected_bunches[1], loss_rate[bunches == selected_bunches[1]], 'yo')
    ax[0][2].plot(selected_bunches[2], loss_rate[bunches == selected_bunches[2]], 'yo')    
    '''
    
    #=========IMPORTING OF DATA
    if scheduleDF is None:
        fillingSchemeDF = importData.LHCFillsAggregation(['LHC.BCTFR.A6R4.B%:BUNCH_FILL_PATTERN'], fillNo, ['FLATTOP'],flag='next')
        B1_bunches = fillingSchemeDF['LHC.BCTFR.A6R4.B1:BUNCH_FILL_PATTERN'].dropna().iloc[0]
        B2_bunches = fillingSchemeDF['LHC.BCTFR.A6R4.B2:BUNCH_FILL_PATTERN'].dropna().iloc[0]
        scheduleDF = bbFunctions.B1CollisionScheduleDF(B1_bunches, B2_bunches, 25)

    if intensityDF is None:
        intensityDF = importData.LHCFillsAggregation(['LHC.BCTFR.A6R4.B2:BUNCH_INTENSITY'], fillNo, ['STABLE'],flag='last')
    #=========
    
    if fig is None or ax is None:
        fig, ax = plt.subplots(1, 1)
    
    position_ALICE = scheduleDF.loc[bunchNo]['Positions in ALICE']
    partner_ALICE = scheduleDF.loc[bunchNo]['BB partners in ALICE'].astype(int)

    position_ATLAS = scheduleDF.loc[bunchNo]['Positions in ATLAS/CMS']
    partner_ATLAS = scheduleDF.loc[bunchNo]['BB partners in ATLAS/CMS'].astype(int)

    position_LHCB = scheduleDF.loc[bunchNo]['Positions in LHCB']
    partner_LHCB = scheduleDF.loc[bunchNo]['BB partners in LHCB'].astype(int)


    y_ALICE = np.array([1]*len(position_ALICE))
    y_ATLAS = np.array([0]*len(position_ATLAS))
    y_LHCB = np.array([-1]*len(position_LHCB))

    intensity = intensityDF['LHC.BCTFR.A6R4.B2:BUNCH_INTENSITY']
    intensity = np.array(intensity.iloc[0])
    
    if len(position_ALICE) is not 0:
        ax.scatter(position_ALICE, y_ALICE, alpha=1, cmap='jet', c= intensity[partner_ALICE], vmin = 0.9e11, vmax = 1.25e11)
        setArrowLabel(ax, label=str(partner_ALICE[0]), arrowPosition=(position_ALICE[0], y_ALICE[0]), labelPosition=(position_ALICE[0], y_ALICE[0]-.5), myColor='r', arrowArc_rad=0.2)
        setArrowLabel(ax, label=str(partner_ALICE[-1]), arrowPosition=(position_ALICE[-1], y_ALICE[-1]), labelPosition=(position_ALICE[-1], y_ALICE[0]-.5), myColor='r', arrowArc_rad=-0.2)
    if len(position_ATLAS) is not 0:
        ax.scatter(position_ATLAS, y_ATLAS, alpha=1, cmap='jet', c = intensity[partner_ATLAS], vmin = 0.9e11, vmax = 1.25e11)
        setArrowLabel(ax, label=str(partner_ATLAS[0]), arrowPosition=(position_ATLAS[0], y_ATLAS[0]), labelPosition=(position_ATLAS[0], y_ATLAS[0]-.5), myColor='r', arrowArc_rad=0.2)
        setArrowLabel(ax, label=str(partner_ATLAS[-1]), arrowPosition=(position_ATLAS[-1], y_ATLAS[-1]), labelPosition=(position_ATLAS[-1], y_ATLAS[0]-.5), myColor='r', arrowArc_rad=-0.2)
    if len(position_LHCB) is not 0:
        paths = ax.scatter(position_LHCB, y_LHCB, alpha=1, cmap='jet', c= intensity[partner_LHCB], vmin = 0.9e11, vmax = 1.25e11)
        setArrowLabel(ax, label=str(partner_LHCB[0]), arrowPosition=(position_LHCB[0], y_LHCB[0]), labelPosition=(position_LHCB[0], y_LHCB[0]-.5), myColor='r', arrowArc_rad=0.2)
        setArrowLabel(ax, label=str(partner_LHCB[-1]), arrowPosition=(position_LHCB[-1], y_LHCB[-1]), labelPosition=(position_LHCB[-1], y_LHCB[0]-.5), myColor='r', arrowArc_rad=-0.2)

    ax.set(yticks = [1, 0, -1], yticklabels = ['ALICE', 'ATLAS/CMS', 'LHCB'], ylim = [-1.8, 1.8], xlim = [-26, 26], xlabel = 'Bunch partner in B2')
    colorbar_handle = fig.colorbar(paths, ax = ax)
    colorbar_handle.set_label('Bunch intensity')
    ax.axvline(x=0)
    
    return fig, ax
