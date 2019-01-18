import subprocess
import pandas
import fcntl
import os
import datetime
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from collections import OrderedDict

def _tfsFormat(myValue, myFormat):
    if 'd' in myFormat:
        myValue=int(myValue)
    if 'l' in myFormat:
        myValue=float(myValue)
    if 's' in myFormat:
        myValue=myValue.replace('"','')
    return myValue

def _tfs2pd(file_name):
    myDictionaryComment=OrderedDict()
    myDictionaryTableFieldName=[]
    myDictionaryTableFieldFormat=[]
    myDictionaryTable=OrderedDict()
    f = open(file_name, "r")
    for line in f: 
        # This is a comment line
        if line[0]=='@':
            aux=line.split()
            value=" ".join(str(x) for x in aux[3:])
            myDictionaryComment[aux[1]]=_tfsFormat(value, aux[2])

        # This is the field name
        if line[0]=='*':
            aux=line.split()
            for i in aux[1:]:
                myDictionaryTableFieldName.append(i)

            for i in range(len(myDictionaryTableFieldName)):
                myDictionaryTable[myDictionaryTableFieldName[i]]=[]

        if line[0]=='$':
            aux=line.split()
            for i in aux[1:]:
                myDictionaryTableFieldFormat.append(i)

        if line[0]==' ':
            aux=line.split()
            for i in range(len(myDictionaryTableFieldName)):
                myDictionaryTable[myDictionaryTableFieldName[i]].append(_tfsFormat(aux[i], myDictionaryTableFieldFormat[i]))

    f.close()
    aux=pd.DataFrame([myDictionaryComment])
    aux['TABLE']=[pd.DataFrame(myDictionaryTable)]
    aux['FILE_NAME']=file_name
    aux=aux.set_index('FILE_NAME')
    aux.index.name=''
    return aux

def tfs2pd(listOfFile):
    '''
        Import a MADX TFS file in a pandas dataframe.
        
        ===Example=== 
        aux=importData.tfs2pd(['/eos/user/s/sterbini/MD_ANALYSIS/2018/LHC MD Optics/collisionAt25cm_180urad/lhcb1_thick.survey',
        '/eos/user/s/sterbini/MD_ANALYSIS/2018/LHC MD Optics/collisionAt25cm_180urad/lhcb1_thick.twiss'])
    '''
    if isinstance(listOfFile,str):
        return _tfs2pd(listOfFile)
    else:
        aux=[]
        for i in listOfFile:
            aux.append(tfs2pd(i))
        return pd.concat(aux)
    
class MadX:
    '''Simple MAD-X wrapper written with the fundamental help of E. Laface (thanks a lot!).
       It is using pipes for communicate with MAD-X (tested on MAC and UNIX).
    '''
    def __init__(self, executable, verbose=True, preamble_script='option, echo, warn,info;\n'):
        self.executable = executable
        self.header=None
        self.table=None
        self.result=[]
        self.log=[]
        self.preamble_script=preamble_script
        self.start_section='!!************************************************START************************************************\n! '
        self.end_section='!!*************************************************END*************************************************\n\n'

        self.p = subprocess.Popen([self.executable], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        fd = self.p.stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        
        self.log+=['! >>> START: '+datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S.%f UTC %Y\n")]
        self.result+=['init']
        while self.result[-1]!='X:> ':
            self.result+=[i.decode() for i in self.p.stdout.readlines()]
        self.result=self.result[1:-1]
        self._clearResult()
        self.log+=self.result
        self.log+=['! <<< STOP: '+datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S.%f UTC %Y\n\n")]
        if verbose==True:
            for i in self.result:
                        print(i[0:-1])
            print('\n')
        self._preamble()
    
    def _preamble(self):
        self.input(self.preamble_script)
    
    def input(self, script, verbose=True):
        try:
            script+="print,text='1G2U3I4D0';\n"
            self.p.stdin.write(script.encode())
            self.p.stdin.flush()
            self.result=[]
            self.log+=['! >>> START: '+datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S.%f UTC %Y\n")]
            self.log+=[script];
            
            while True:
                aux=[i.decode() for i in self.p.stdout.readlines()];
                self.result+=aux
                if (any('1G2U3I4D0\n' in mystring for mystring in aux)) | (self.p.poll()==0):
                    break
            
            self.log+=self.result
            self.log+=['! <<< STOP: '+datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S.%f UTC %Y\n\n")]
            
            self._clearResult()
            if verbose==True:
                self._clearResult()
                for i in self.result:
                            print(i[0:-1])
        except:
            print('ERROR WITH THE EXECUTION, PLEASE CHECK IT.')
            return   
        
    def print_log(self):
        for i in self.log:
            print(i[:-1])
            
    def _clearResult(self):
        for string in ["print,text='1G2U3I4D0';\n",'X:>\n','X:> ','X:> \n','X:> X:> ','X:> X:> \n','1G2U3I4D0\n','\n']:
            while string in self.result: self.result.remove(string)    
        
        for i in range(len(self.result)):
            self.result[i]=str.replace(self.result[i],'X:> ','')
            if self.result[i]==self.end_section[0:-1]:
                self.result[i]=self.end_section
            
    def close(self):
        self.p.kill()
 
    def buildInput(self,myInputDictionary, myInputList, verbose=True):
        aux=''
        for i in myInputList:
            #if i=='HEADER':
            #    aux='option, echo, warn,info;\n'+aux
            if verbose: 
                aux=aux+self.start_section+i+''
            aux=aux+myInputDictionary[i]
            if verbose: 
                aux=aux+self.end_section
        return aux
    
    def buildFileFromDictionary(self,myInputDictionary,myFile="input.txt"):
        text_file = open(myFile, "w")
        text_file.write(self.buildInput(myInputDictionary,myInputDictionary.keys()))
        text_file.close()
   
    def buildDictionaryFromFile(self,myFile="input.txt"):
        myInputDictionaryFromFile=OrderedDict()
        text_file = open(myFile, "r")
        a=text_file.read()
        text_file.close()

        myInputDictionaryFromFile=OrderedDict()
        myList=a.splitlines()
        aux=[i for i, j in enumerate(myList) if j == self.start_section[0:-3]]

        for i in range(len(aux)):
            myAux=aux.copy()
            myAux.append(len(myList))
            j=myAux[i]
            k=myAux[i+1]

            myString="""
            {}""".format("\n".join(myList[(j+2):(k-2)]))
            myString=myString+'\n'
            while '\n ' in myString:
                myString=myString.replace('\n ', '\n')
            myInputDictionaryFromFile[myList[j+1][2:]]=myString
        return myInputDictionaryFromFile
