import matplotlib.pyplot as plt
import datetime 

def setSourcePlot(gca, pltDescription,x=0.99,y=0.01,horizontalalignment='right',\
                  color='lightgray',verticalalignment='bottom',rotation=0,fontsize=7):
  '''
  Comment the plot adding for instance the source script.
   
  It requires an axis (gca) and a string (pltDescription).
   
  ===EXAMPLE===
  plt.plot([1,2,3,])
  setSourcePlot(plt.gca(), pltDescription,x=0.99,y=0.01,horizontalalignment='right',\
                  color='lightgray',verticalalignment='bottom',rotation=0,fontsize=7)
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

