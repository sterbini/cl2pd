import matplotlib.pyplot as plt

def setSourcePlot(gca, pltDescription,x=0.99,y=0.01,horizontalalignment='right',\
                  color='lightgray',verticalalignment='bottom',rotation=0,fontsize=7):
    plt.text(x,y,pltDescription, 
             horizontalalignment=horizontalalignment, 
             color=color,
             verticalalignment=verticalalignment, 
             transform=gca.transAxes,rotation=rotation, fontsize=fontsize);
