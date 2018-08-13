'''
This package will help you in launching parametric studies that uses ASCII file as inputs.
The main idea is starting with a generig ASCII input file (maskedInput file) containing a generic setup of your simulation. We call it 'mask' since the parameters are 'masked',
that is they are placeholders without a value attached.

They are, by convention, string starting with 'MASKED_' .
Depending of the number of masked paramters combination that the user wants to cover, the set and number of the simulations are defined (parameter space of the simulation).

In practice the user has to prapare first of all the maskedInput file.
Given a maskedInput file, the number ot masked parameters can be obtained with the menthod getMaskedParameterList.
At that points the user populated a pandas DF starting from a list of dictionaries, containing the parameter space of the simulation and the auxilaries columns.
The auxiliaries columns can contain for example 
- the working folder (for each pandas DF row a folder with the index of the simulation is created)
- the address of file to log the standard out of the simulation
- the address of the maskedInput file
- the command to launch the simulation (for MADX you can use writeMADXCommand)

One can use the method writeUnmaskedInput to write the unmasked input.

The one can launch the simulations (via runCommand) and retrieve and postprocess the output.

=== EXAMPLE ===
import cl2pd # do "pip install --user git+https://github.com/sterbini/cl2pd.git" to install
from cl2pd import importData
from cl2pd import plotFunctions
from cl2pd import dotdict
from cl2pd import parametricSimulations
import os
import itertools
dotdict=dotdict.dotdict
pd=importData.pd     # is the pandas package
np=importData.np     # is the numpy package

import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
%config InlineBackend.figure_format = 'retina' # retina display
#mySource='string with full notebook address used to comment plots'


MASKED_input='/eos/user/s/sterbini/MD_ANALYSIS/MADX/example/maskedInput.madx'
parametricSimulations.getMaskedParameterList('/eos/user/s/sterbini/MD_ANALYSIS/MADX/example/maskedInput.madx',printLine=True)

# Definition of the parameter space

myWorkingRootFolder='/eos/user/s/sterbini/MD_ANALYSIS/MADX/example' #this folder has to exist
myList=[]
parameter_klwire_list=np.linspace(0,.0004,10)
myIndex=np.arange(len(parameter_klwire_list))


for parameter_klwire, i in zip(parameter_klwire_list,myIndex):
    workingFolder=myWorkingRootFolder+ '/simulation_'+format(i,'04d')
    if not os.path.exists(workingFolder):
        os.makedirs(workingFolder)
    myList.append({'MASKED_klwire': parameter_klwire, 
                   'MASKED_fileName':'\''+workingFolder+'/output.twiss\'',
                   'standardOut':workingFolder+'/standard.out', 
                   'workingFolder':workingFolder,
                  })

myParameterSpace=pd.DataFrame(myList)
myParameterSpace['maskedInput']=MASKED_input

# producing the unmasked inputs
myParameterSpace['unmaskedInput']=myParameterSpace.apply(lambda x: parametricSimulations.writeUnmaskedInput(x,MASKED_input), axis=1)

# preparing the command string
myParameterSpace['command']=myParameterSpace.apply(parametricSimulations.writeMADXCommand, axis=1)

# running the simulations
myParameterSpace.apply(parametricSimulations.runCommand, axis=1)

# importing the data
outDF=importData.tfs2pd(list(myParameterSpace.apply(lambda x: x['workingFolder']+'/output.twiss',axis=1).values))

#Example for plotting
plt.plot(myParameterSpace.MASKED_klwire*10000,outDF.Q1-62,'o-b')
plt.plot(myParameterSpace.MASKED_klwire*10000,outDF.Q2-60,'s-r')
'''

import re
import numpy as np
import os

def getMaskedParameterList(myFile, tag='MASKED_', printLine=False):
    '''
    It returns the words strarting with tag='MASKED_' in myFile.
    If printLine then the full line contained a masked parameters is printed.
    '''
    searchfile = open(myFile, "r")
    myList=[]
    for line in searchfile:
        aux=re.findall('\\'+ tag + '\w+', line)
        for i in (aux):
            if printLine: print(line)
            myList.append(i)
    searchfile.close()
    return np.unique(myList);

def writeUnmaskedInput(df,maskFile):
    myList=getMaskedParameterList(maskFile)
    if len(np.intersect1d(myList,df.index))==len(myList):
        searchfile = open(maskFile, "r")
        myFile=''
        for line in searchfile:
            for parameter in df.index:
                line=line.replace(parameter, str(df[parameter]));
            myFile=myFile+line;
        text_file = open(df.workingFolder+'/unmaskedInput.madx', "w")
        text_file.write(myFile)
        text_file.close()
        return df.workingFolder+'/unmaskedInput.madx'
    else:
        print('Some masked parameters are not defined.')
        
def writeMADXCommand(df,executable='/eos/user/s/sterbini/MD_ANALYSIS/MADX/madx-linux64-gnu'):
    return executable + ' < ' + str.replace(df.unmaskedInput,' ','\ ') + ' > ' +  str.replace(df.standardOut,' ','\ ')

def runCommand(df):
    os.system(df.command)
    return df.command
